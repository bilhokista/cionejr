"""Original digital storybook scene, constructed from edited flat forms."""
from functools import lru_cache
from pathlib import Path
import math
import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT=Path(__file__).parent
S=3
SIZE=(1000,1250)

FOX_BODY=[('M',(308,718)),('C',(268,716),(245,759),(245,813)),
          ('C',(238,866),(264,922),(305,940)),('C',(335,957),(366,949),(371,917)),
          ('L',(371,794)),('C',(377,753),(352,727),(308,718))]
FOX_HEAD=[('M',(261,622)),('L',(241,528)),('C',(273,537),(295,562),(318,583)),
          ('C',(335,574),(355,573),(375,588)),('L',(390,535)),
          ('C',(414,558),(426,610),(420,647)),('C',(439,652),(451,665),(466,682)),
          ('C',(447,699),(425,711),(400,713)),('C',(380,739),(344,750),(315,733)),
          ('C',(286,721),(269,682),(261,622))]
FOX_TAIL=[('M',(278,844)),('C',(208,843),(163,882),(134,923)),
          ('C',(97,962),(132,1003),(210,1009)),('C',(258,1016),(322,970),(313,928)),
          ('L',(278,844))]
RABBIT_BODY=[('M',(702,764)),('C',(742,749),(768,785),(769,825)),
             ('C',(793,853),(791,897),(754,922)),('C',(723,942),(671,931),(658,899)),
             ('C',(648,867),(657,800),(681,779)),('C',(687,773),(694,768),(702,764))]
RABBIT_HEAD=[('M',(660,680)),('C',(679,659),(715,655),(737,675)),
             ('C',(750,690),(749,730),(731,750)),('C',(713,771),(672,768),(644,752)),
             ('L',(620,736)),('C',(631,725),(641,715),(647,699)),
             ('C',(651,690),(656,684),(660,680))]
RABBIT_EARS=[ [('M',(677,683)),('C',(660,621),(639,554),(647,514)),
              ('C',(648,497),(660,493),(667,510)),('C',(687,548),(697,614),(700,678)),('L',(677,683))],
              [('M',(707,684)),('C',(714,615),(721,551),(744,522)),
               ('C',(762,500),(768,518),(762,545)),('C',(759,583),(742,650),(730,688)),('L',(707,684))] ]
DEER_BODY=[('M',(555,630)),('C',(583,606),(638,627),(665,651)),
           ('C',(699,681),(683,719),(648,728)),('C',(607,738),(563,712),(552,679)),('L',(555,630))]
DEER_NECK=[('M',(516,573)),('C',(520,616),(511,648),(539,682)),
           ('L',(584,683)),('C',(563,652),(569,610),(565,568)),('L',(516,573))]
DEER_HEAD=[('M',(505,523)),('C',(519,502),(551,502),(565,523)),
           ('C',(578,545),(569,575),(550,600)),('C',(536,615),(526,610),(513,595)),
           ('C',(496,574),(493,544),(505,523))]
DEER_EARS=[ [('M',(511,535)),('C',(480,526),(456,507),(463,486)),
            ('C',(484,482),(506,503),(523,528)),('L',(511,535))],
            [('M',(555,527)),('C',(559,500),(577,474),(596,477)),
             ('C',(607,497),(584,522),(565,538)),('L',(555,527))] ]
SQUIRREL_TAIL=[('M',(845,587)),('C',(932,560),(946,459),(890,439)),
               ('C',(834,418),(802,479),(837,517)),('C',(854,535),(894,501),(899,487)),
               ('C',(917,526),(887,558),(848,548)),('L',(845,587))]
SQUIRREL_BODY=[('M',(790,557)),('C',(774,579),(779,606),(814,622)),
               ('C',(849,635),(863,598),(848,569)),('C',(835,549),(811,548),(790,557))]
SQUIRREL_HEAD=[('M',(752,526)),('C',(764,506),(799,501),(815,520)),
               ('C',(830,544),(811,564),(784,563)),('C',(765,562),(748,553),(737,546)),
               ('C',(743,537),(747,532),(752,526))]
CLEARING=[('M',(394,707)),('C',(534,685),(693,704),(783,788)),
          ('C',(867,866),(875,932),(827,1008)),('C',(788,1108),(766,1201),(787,1250)),
          ('L',(184,1250)),('C',(290,1165),(330,1100),(315,1010)),
          ('C',(268,924),(238,856),(292,791)),('C',(320,753),(349,724),(394,707))]


def rgb(c):
    return tuple(bytes.fromhex(c.strip('#'))) if isinstance(c,str) else tuple(c)


def sample(commands):
    result=[]
    current=None
    for kind,*vals in commands:
        if kind in ('M','L'):
            current=vals[0]
            result.append(current)
        elif kind=='C':
            a,b,c=vals
            origin=current
            for i in range(1,37):
                t=i/36
                result.append(tuple((1-t)**3*origin[j]+3*(1-t)**2*t*a[j]
                                    +3*(1-t)*t*t*b[j]+t**3*c[j] for j in (0,1)))
            current=c
        else:
            raise ValueError(kind)
    return result


def path(im,commands,fill=None,stroke=None,width=1):
    pts=[(round(x*S),round(y*S)) for x,y in sample(commands)]
    d=ImageDraw.Draw(im)
    if fill is not None:
        d.polygon(pts,fill=rgb(fill))
    if stroke is not None:
        d.line(pts,fill=rgb(stroke),width=max(1,round(width*S)),joint='curve')


def ellipse(im,x,y,rx,ry,color,outline=None,width=1):
    ImageDraw.Draw(im).ellipse(((x-rx)*S,(y-ry)*S,(x+rx)*S,(y+ry)*S),
                              fill=rgb(color) if color else None,
                              outline=rgb(outline) if outline else None,width=max(1,round(width*S)))


def line(im,points,color,width=1):
    ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in points],
                           fill=rgb(color),width=max(1,round(width*S)),joint='curve')


def mask(commands):
    im=Image.new('L',(3000,3750))
    ImageDraw.Draw(im).polygon([(round(x*S),round(y*S)) for x,y in sample(commands)],fill=255)
    return im


def leaf(im,root,tip,width,color,vein=None):
    dx,dy=tip[0]-root[0],tip[1]-root[1]
    length=math.hypot(dx,dy)
    nx,ny=-dy/length,dx/length
    shape=[('M',root),('C',(root[0]+dx*.18+nx*width,root[1]+dy*.18+ny*width),
           (root[0]+dx*.7+nx*width*.5,root[1]+dy*.7+ny*width*.5),tip),
           ('C',(root[0]+dx*.7-nx*width*.55,root[1]+dy*.7-ny*width*.55),
            (root[0]+dx*.17-nx*width*.65,root[1]+dy*.17-ny*width*.65),root)]
    path(im,shape,fill=color)
    if vein:
        line(im,[root,(root[0]+dx*.83,root[1]+dy*.83)],vein,.8)


def layout():
    im=Image.new('RGB',(3000,3750),rgb('#8eaa8d'))
    path(im,CLEARING,fill='#d6d5ac')
    for x,w in [(85,130),(208,50),(842,70),(954,160)]:
        path(im,[('M',(x-w/2,0)),('L',(x+w/2,0)),('L',(x+w/2,1100)),('L',(x-w/2,1100))],fill='#42665b')
    path(im,[('M',(128,450)),('C',(260,476),(369,451),(532,462))],stroke='#42665b',width=12)
    path(im,[('M',(734,643)),('C',(790,626),(863,621),(950,613))],stroke='#42665b',width=14)
    for leg in [[(570,680),(564,780)],[(595,696),(592,791)],[(642,696),(659,789)],[(660,689),(687,781)]]:
        line(im,leg,'#a48b66',13)
    path(im,DEER_BODY,fill='#c6ae7b')
    path(im,DEER_NECK,fill='#c6ae7b')
    for ear in DEER_EARS:path(im,ear,fill='#c6ae7b')
    path(im,DEER_HEAD,fill='#c6ae7b')
    ellipse(im,524,566,4,4,'#354e40')
    ellipse(im,554,563,4,4,'#354e40')
    path(im,SQUIRREL_TAIL,fill='#ab754e')
    path(im,SQUIRREL_BODY,fill='#ab754e')
    path(im,SQUIRREL_HEAD,fill='#ab754e')
    line(im,[(801,596),(790,628)],'#ab754e',13)
    path(im,FOX_TAIL,fill='#cc794e')
    path(im,FOX_BODY,fill='#cc794e')
    path(im,FOX_HEAD,fill='#cc794e')
    line(im,[(356,786),(397,813),(442,819)],'#e5bc91',21)
    path(im,RABBIT_BODY,fill='#eee3c5')
    for ear in RABBIT_EARS:path(im,ear,fill='#eee3c5')
    path(im,RABBIT_HEAD,fill='#eee3c5')
    line(im,[(694,797),(650,805),(623,819)],'#eee3c5',19)
    ellipse(im,308,941,35,12,'#eee3c5')
    ellipse(im,709,922,53,15,'#eee3c5')
    path(im,[('M',(431,825)),('L',(446,958)),('L',(596,958)),('L',(619,825))],fill='#9b7960')
    ellipse(im,525,826,95,27,'#d2b98b')
    ellipse(im,520,805,49,18,'#c49059')
    ellipse(im,447,799,14,16,'#ba6750')
    ellipse(im,504,790,13,13,'#ba6750')
    ellipse(im,522,784,13,15,'#dca869')
    ellipse(im,539,791,11,12,'#ba6750')
    ellipse(im,514,1050,99,74,'#7f7158')
    path(im,[('M',(552,1018)),('C',(588,1028),(625,1053),(645,1077)),
             ('C',(647,1084),(604,1097),(573,1096)),('C',(520,1097),(515,1076),(539,1045)),('L',(552,1018))],fill='#d8c7a2')
    ellipse(im,650,1096,10,10,'#ba6750')
    ellipse(im,504,412,27,19,'#e6d8b3')
    ellipse(im,524,391,15,15,'#9c7552')
    line(im,[(504,427),(509,461)],'#685844',2)
    line(im,[(518,425),(523,461)],'#685844',2)
    im.resize((1000,1250),Image.Resampling.LANCZOS).save(ROOT/'composition.png')
    print('Saved composition.png')


def offset(commands,dx,dy):
    return [(kind,*[(x+dx,y+dy) for x,y in coords]) for kind,*coords in commands]


def eye(im,x,y,r=4,color='#314c43',gaze=(0,0),lid=None):
    gx,gy=gaze
    ellipse(im,x+gx*.4,y+gy*.4,r,r*1.08,color)
    ellipse(im,x+1+gx,y-1+gy,max(.75,r*.22),max(.75,r*.22),'#f6e7bf')
    if lid:
        path(im,[('M',(x-r*1.25,y-r*.45)),('C',(x-r*.5,y-r*1.15),(x+r*.5,y-r*1.15),(x+r*1.25,y-r*.45))],
             stroke=lid,width=1.6)


def jitter(color,rng,amount=9):
    return tuple(max(0,min(255,c+rng.randint(-amount,amount))) for c in rgb(color))


def sprig(im,base,tip,count,color,stemcolor,seed=0,leafwidth=10,kind='frond'):
    rng=random.Random(seed)
    dx,dy=tip[0]-base[0],tip[1]-base[1]
    length=math.hypot(dx,dy)
    nx,ny=-dy/length,dx/length
    path(im,[('M',base),('C',(base[0]+dx*.3,base[1]+dy*.3),
         (base[0]+dx*.75,base[1]+dy*.75),tip)],stroke=stemcolor,width=1.4)
    for i in range(1,count+1):
        t=i/(count+1)
        root=(base[0]+dx*t,base[1]+dy*t)
        if kind=='broad':
            # Broad leaves alternate along the stem and swing wider than fronds do.
            side=1 if i%2 else -1
            reach=rng.uniform(26,40)*(1-t*.3)
            end=(root[0]+nx*reach*side+dx*.2,root[1]+ny*reach*side+dy*.2)
            leaf(im,root,end,leafwidth*rng.uniform(1.25,1.7),jitter(color,rng),stemcolor)
            continue
        for side in (-1,1):
            reach=rng.uniform(21,42)*(1-t*.4)
            end=(root[0]+nx*reach*side+dx*.11,root[1]+ny*reach*side+dy*.11)
            leaf(im,root,end,leafwidth*rng.uniform(.65,1.15),jitter(color,rng,6),stemcolor)
    leaf(im,(base[0]+dx*.85,base[1]+dy*.85),tip,leafwidth*(1.1 if kind=='broad' else .65),color)


def forest(im):
    # Soft distant light, with the active area warmer than the forest margins.
    yy,xx=np.mgrid[0:3750,0:3000]
    x,y=xx/S,yy/S
    light=np.exp(-((x-520)/345)**2-((y-370)/540)**2)
    dark=np.array(rgb('#537d70'),dtype=np.float32)
    warm=np.array(rgb('#d7d8a6'),dtype=np.float32)
    arr=dark[None,None,:]+light[:,:,None]*(warm-dark)[None,None,:]
    im.paste(Image.fromarray(arr.astype(np.uint8)))
    # Distant trunks are narrow and lower contrast, with actual connected branches.
    for j,(x,w,lean) in enumerate([(243,22,26),(318,17,-36),(404,19,32),(604,21,-28),(698,22,35),(766,24,-25)]):
        col=['#9ab28d','#a7bc92','#91ad8a'][j%3]
        path(im,[('M',(x-w,0)),('L',(x+w,0)),('C',(x+lean+w,310),(x+lean+w,597),(x+lean+w,831)),
                 ('L',(x+lean-w,835)),('C',(x+lean-w,590),(x+lean-w,315),(x-w,0))],fill=col)
        for h,side in [(249,1),(401,-1),(560,1)]:
            path(im,[('M',(x+lean*.6,h+48)),('C',(x+side*41,h+18),(x+side*71,h-27),(x+side*83,h-80))],stroke=col,width=8)
    # Layered undergrowth, not an inset poster background.
    path(im,[('M',(0,815)),('C',(198,642),(338,681),(465,737)),('C',(624,674),(809,664),(1000,774)),
             ('L',(1000,1250)),('L',(0,1250))],fill='#709277')
    path(im,[('M',(0,911)),('C',(179,838),(304,830),(394,821)),('C',(555,823),(793,755),(1000,869)),
             ('L',(1000,1250)),('L',(0,1250))],fill='#7e9b76')
    path(im,CLEARING,fill='#c5c895')
    path(im,[('M',(416,752)),('C',(575,734),(715,766),(763,845)),
             ('C',(773,891),(725,933),(720,978)),('C',(679,1098),(702,1203),(733,1250)),
             ('L',(382,1250)),('C',(428,1132),(413,1046),(385,979)),
             ('C',(352,895),(337,800),(416,752))],fill='#d9d3a3')
    # Broken forest shadows lie on the ground, away from the faces.
    for p in [ [('M',(216,992)),('C',(322,970),(384,975),(431,1001)),('L',(380,1021)),('L',(216,992))],
               [('M',(667,943)),('C',(755,895),(810,913),(849,951)),('L',(803,990)),('L',(667,943))],
               [('M',(397,1165)),('C',(507,1140),(678,1171),(715,1204)),('L',(581,1208)),('L',(397,1165))] ]:
        path(im,p,fill='#babf8e')
    # Near trunks taper and split into branches rather than rectangular columns.
    left=[('M',(-65,0)),('L',(181,0)),('C',(183,203),(151,390),(152,613)),
          ('C',(158,790),(191,954),(194,1041)),('L',(227,1103)),('L',(144,1083)),
          ('L',(75,1131)),('L',(-45,1109)),('L',(-65,0))]
    right=[('M',(864,-10)),('L',(1047,-10)),('L',(1050,1151)),('L',(935,1120)),
           ('L',(831,1114)),('L',(872,1051)),('C',(874,837),(873,689),(880,504)),
           ('C',(885,309),(872,160),(864,-10))]
    path(im,left,fill='#284f49')
    path(im,right,fill='#31574c')
    path(im,[('M',(63,0)),('C',(75,259),(77,712),(114,1051)),('L',(143,1091)),
             ('C',(104,753),(112,414),(126,0)),('L',(63,0))],fill='#3d6657')
    path(im,[('M',(915,0)),('C',(936,355),(906,630),(927,1007)),('L',(956,1096)),
             ('C',(934,744),(956,399),(955,0)),('L',(915,0))],fill='#456950')
    # Branches frame an arch, with a smaller perch on each side.
    for branch,width in [([('M',(115,317)),('C',(270,251),(343,136),(421,78))],31),
                         ([('M',(903,281)),('C',(745,198),(650,124),(614,21))],31),
                         ([('M',(112,447)),('C',(261,476),(370,451),(538,462))],12),
                         (offset([('M',(734,643)),('C',(790,626),(863,621),(950,613))],18,-65),14)]:
        path(im,branch,stroke='#31584c',width=width)
    # Deliberate bark grooves, sparse where animals overlap.
    for x,y,ex,ey in [(29,147,36,349),(74,493,85,735),(111,830,131,990),
                      (931,139,934,349),(904,700,905,881),(962,488,951,637)]:
        path(im,[('M',(x,y)),('C',(x-6,y+52),(ex+7,ey-55),(ex,ey))],stroke='#52755c',width=2)
    # Canopy lobes and connected leaf sprays preserve a central window of light.
    path(im,[('M',(0,0)),('L',(1000,0)),('L',(1000,235)),
             ('C',(947,220),(947,166),(899,172)),('C',(839,163),(835,112),(790,127)),
             ('C',(730,147),(728,69),(672,89)),('C',(602,108),(598,38),(548,64)),
             ('C',(497,93),(468,27),(415,70)),('C',(368,116),(336,80),(293,128)),
             ('C',(238,180),(191,126),(150,204)),('C',(120,254),(49,221),(0,294)),('L',(0,0))],fill='#254f47')
    sprays=[((143,321),(334,153),7,'#4c775a',10),((182,267),(360,274),6,'#659164',11),
            ((855,253),(688,171),6,'#527c59',12),((918,365),(756,332),6,'#7b9a64',13),
            ((65,351),(73,159),7,'#719067',14),((959,422),(925,230),7,'#5e835c',15),
            ((261,132),(390,54),5,'#66865d',16),((737,115),(635,36),5,'#809460',17),
            ((189,455),(278,373),5,'#7fa378',18),((861,544),(937,456),4,'#89a46c',19)]
    broad={16,18,19}
    for base,tip,n,color,seed in sprays:
        sprig(im,base,tip,n,color,'#91ae76',seed,12,'broad' if seed in broad else 'frond')
    # Individual larger leaves keep the canopy from becoming identical small fronds.
    for root,tip,width,color in [((195,238),(237,113),35,'#3c6852'),((264,213),(311,106),30,'#4f7756'),
                                ((814,195),(751,104),32,'#648259'),((866,331),(841,223),27,'#688c5e'),
                                ((133,419),(86,362),25,'#83a16a'),((949,516),(899,442),23,'#587f58')]:
        leaf(im,root,tip,width,color,'#8eab73')
    # A faint shaft of sunlight is part of the clearing, not a halo around a character.
    for x,y,rx,ry in [(458,270,7,11),(640,409,5,7),(352,508,4,6),(709,320,3,5)]:
        ellipse(im,x,y,rx,ry,'#d4d9a5')


def deer(im):
    ellipse(im,624,786,97,12,'#a9b184')
    for pp,col in [([(570,680),(564,771)],'#aa9066'),([(642,696),(659,780)],'#aa9066'),
                   ([(595,696),(592,787)],'#c1a879'),([(660,689),(687,776)],'#c1a879')]:
        line(im,pp,col,12)
        x,y=pp[-1]
        ellipse(im,x+2,y+6,8,5,'#5a614d')
    path(im,DEER_BODY,fill='#c2a578')
    path(im,[('M',(563,681)),('C',(600,713),(649,716),(675,685)),
             ('C',(671,724),(619,742),(580,714)),('L',(563,681))],fill='#ad946c')
    path(im,DEER_NECK,fill='#c2a578')
    path(im,[('M',(516,583)),('C',(526,618),(521,652),(543,677)),('L',(556,671)),
             ('C',(539,639),(543,608),(545,594)),('L',(516,583))],fill='#dbc394')
    for ear in DEER_EARS:path(im,ear,fill='#c2a578')
    path(im,[('M',(505,520)),('C',(482,515),(473,504),(474,496)),('C',(490,497),(504,510),(505,520))],fill='#957b60')
    path(im,[('M',(565,519)),('C',(570,500),(582,489),(590,489)),('C',(594,501),(580,516),(565,519))],fill='#957b60')
    path(im,DEER_HEAD,fill='#c9ae7f')
    path(im,[('M',(521,570)),('C',(532,564),(546,563),(559,574)),
             ('C',(553,604),(532,616),(521,595)),('L',(521,570))],fill='#e5d2a8')
    # The deer lowers its gaze to the basket, so attention runs fox, basket, rabbit and deer.
    eye(im,515,556,3.7,gaze=(.6,1.7),lid='#8d7455')
    eye(im,552,554,3.7,gaze=(.6,1.7),lid='#8d7455')
    ellipse(im,539,594,7,4,'#475747')
    path(im,[('M',(539,598)),('C',(536,603),(532,603),(529,601))],stroke='#7f7d5c',width=1)
    for x,y,rx,ry in [(588,652,5,3),(610,647,5,3),(629,657,5,3),
                      (593,666,5,3),(616,669,5,3),(641,678,4,3)]:
        ellipse(im,x,y,rx,ry,'#ecdbb4')


def squirrel(im):
    dx,dy=18,-65
    p=lambda commands,**kw:path(im,offset(commands,dx,dy),**kw)
    e=lambda x,y,rx,ry,col:ellipse(im,x+dx,y+dy,rx,ry,col)
    p(SQUIRREL_TAIL,fill='#b17a4e')
    p([('M',(850,553)),('C',(913,532),(921,461),(879,458)),
       ('C',(843,454),(833,491),(855,509))],stroke='#d1a16d',width=8)
    p(SQUIRREL_BODY,fill='#b88456')
    p([('M',(784,570)),('C',(800,567),(829,590),(827,615)),
       ('C',(804,616),(791,596),(784,570))],fill='#ddbd8a')
    p([('M',(793,515)),('C',(780,498),(785,486),(799,483)),
       ('C',(815,488),(816,508),(808,518)),('L',(793,515))],fill='#b88456')
    p([('M',(795,508)),('C',(788,500),(790,493),(798,492)),('L',(805,510)),('L',(795,508))],fill='#815e45')
    p(SQUIRREL_HEAD,fill='#bf8b5a')
    p([('M',(742,545)),('C',(755,541),(774,548),(788,557)),
       ('C',(769,562),(748,554),(742,545))],fill='#dfc498')
    p([('M',(801,592)),('C',(802,608),(795,616),(789,628))],stroke='#b88456',width=10)
    e(790,628,12,3,'#86694d')
    p([('M',(829,610)),('C',(835,619),(829,625),(819,627))],stroke='#b88456',width=11)
    e(817,627,13,3,'#9e764f')
    eye(im,765+dx,528+dy,3.7)
    e(738,546,4,3,'#384d40')
    p([('M',(750,550)),('C',(756,553),(762,553),(767,551))],stroke='#735d44',width=1)
    # Small paws hold an acorn, bringing the side character into the same gathering.
    p([('M',(780,575)),('C',(765,580),(763,590),(775,597))],stroke='#bf8b5a',width=9)
    e(765,591,7,9,'#c5a174')
    e(765,586,8,3,'#775c43')


def sparrow(im):
    bird=[('M',(449,445)),('C',(462,434),(472,422),(482,416)),
          ('C',(481,402),(493,393),(507,394)),('C',(511,378),(528,375),(535,389)),
          ('L',(549,398)),('L',(535,404)),('C',(537,420),(528,432),(516,435)),
          ('C',(503,441),(491,436),(481,433)),('L',(449,445))]
    p=lambda commands,**kw:path(im,offset(commands,0,17),**kw)
    path(im,[('M',(507,449)),('L',(510,461)),('L',(516,462))],stroke='#5c5743',width=1.7)
    path(im,[('M',(520,449)),('L',(525,462)),('L',(531,462))],stroke='#5c5743',width=1.7)
    p(bird,fill='#e3d0a3')
    p([('M',(481,416)),('C',(497,397),(515,402),(515,416)),
       ('C',(506,428),(488,431),(472,431)),('L',(481,416))],fill='#8f7851')
    p([('M',(511,394)),('C',(511,379),(528,376),(535,389)),
       ('L',(534,396)),('C',(522,389),(520,391),(511,394))],fill='#98674b')
    p([('M',(533,394)),('L',(549,398)),('L',(535,404)),('L',(533,394))],fill='#364f42')
    ellipse(im,520,424,3.3,4.4,'#374e40')
    eye(im,529,409,2.5)
    p([('M',(484,416)),('C',(493,418),(500,416),(505,411))],stroke='#e7d6a7',width=2)


def fox(im):
    ellipse(im,293,945,85,17,'#aab185')
    path(im,FOX_TAIL,fill='#bb7149')
    path(im,[('M',(134,923)),('C',(97,962),(132,1003),(210,1009)),
             ('C',(186,989),(174,973),(174,951)),('L',(153,963)),('L',(163,942)),('L',(145,950)),('L',(134,923))],fill='#e8d8ae')
    path(im,FOX_BODY,fill='#cb8051')
    path(im,[('M',(319,747)),('C',(351,749),(365,778),(359,824)),
             ('L',(354,901)),('C',(340,921),(314,913),(309,890)),
             ('C',(298,832),(304,784),(319,747))],fill='#f1ddae')
    path(im,[('M',(262,863)),('C',(276,892),(282,921),(309,937))],stroke='#aa623f',width=3)
    ellipse(im,307,939,36,13,'#d4a277')
    ellipse(im,321,938,25,11,'#eddbb5')
    for x in (325,332):path(im,[('M',(x,936)),('L',(x+1,943))],stroke='#ad8d67',width=1.1)
    path(im,FOX_HEAD,fill='#ce8252')
    path(im,[('M',(252,551)),('L',(267,612)),('L',(299,601)),('C',(285,580),(270,561),(252,551))],fill='#825740')
    path(im,[('M',(392,558)),('C',(404,578),(410,605),(408,627)),('L',(383,600)),('L',(392,558))],fill='#88573f')
    path(im,[('M',(282,661)),('C',(314,647),(345,646),(375,653)),
             ('C',(395,665),(411,673),(454,680)),('C',(432,700),(406,711),(393,708)),
             ('C',(367,732),(323,724),(297,702)),('C',(289,688),(285,674),(282,661))],fill='#f0deb4')
    path(im,[('M',(333,664)),('C',(342,672),(351,677),(356,681))],stroke='#dcc498',width=2)
    eye(im,388,643,4.8)
    path(im,[('M',(376,633)),('C',(382,628),(389,629),(393,632))],stroke='#9f653f',width=1.5)
    ellipse(im,461,681,7.3,4.8,'#344e43')
    path(im,[('M',(443,692)),('C',(430,699),(416,699),(407,695))],stroke='#927956',width=1.5)
    # The foreleg reaches the shared table, with a distinct paw supporting the apple.
    path(im,[('M',(352,772)),('C',(373,773),(384,790),(399,801)),('L',(442,807)),
             ('C',(454,818),(453,833),(439,837)),('L',(391,828)),
             ('C',(367,819),(350,801),(352,772))],fill='#d59663')
    path(im,[('M',(421,805)),('L',(442,807)),('C',(454,818),(453,833),(439,837)),
             ('L',(418,831)),('L',(421,805))],fill='#e9cea0')
    for x in (433,439):path(im,[('M',(x,817)),('L',(x+3,827))],stroke='#b99a70',width=1)


def rabbit(im):
    ellipse(im,718,925,83,13,'#aab286')
    ellipse(im,780,859,24,24,'#ebdfbf')
    path(im,RABBIT_BODY,fill='#eee2bf')
    path(im,[('M',(735,791)),('C',(777,808),(790,885),(755,914)),
             ('C',(731,932),(686,923),(676,904)),('C',(734,909),(761,862),(735,791))],fill='#d5cdae')
    for ear in RABBIT_EARS:path(im,ear,fill='#eee2bf')
    path(im,[('M',(681,662)),('C',(661,605),(649,545),(654,520)),
             ('C',(671,550),(682,611),(686,661)),('L',(681,662))],fill='#d8b294')
    path(im,[('M',(719,666)),('C',(725,608),(740,556),(753,532)),
             ('C',(753,577),(735,635),(724,669)),('L',(719,666))],fill='#d8b294')
    path(im,RABBIT_HEAD,fill='#f2e6c9')
    path(im,[('M',(733,689)),('C',(749,716),(732,753),(694,760)),
             ('C',(678,763),(661,756),(649,750)),('C',(700,746),(731,727),(733,689))],fill='#e5d7b7')
    eye(im,667,710,4.6)
    ellipse(im,623,735,5.1,3.6,'#a97b63')
    path(im,[('M',(627,739)),('C',(633,745),(642,746),(648,742))],stroke='#9e9475',width=1.2)
    ellipse(im,661,733,9,5,'#e4c9a6')
    path(im,[('M',(694,785)),('C',(673,787),(650,794),(623,807)),
             ('C',(613,812),(615,824),(627,826)),('C',(663,813),(686,813),(703,805)),('L',(694,785))],fill='#eee2bf')
    path(im,[('M',(675,807)),('C',(658,810),(645,815),(638,818))],stroke='#c9c1a2',width=1.2)
    ellipse(im,713,921,53,15,'#eee2bf')
    for x in (680,689):path(im,[('M',(x,919)),('L',(x,928))],stroke='#b8b698',width=1.1)
    path(im,[('M',(692,847)),('C',(674,860),(672,882),(686,900))],stroke='#c7c3a2',width=1.8)


def apple(im,x,y,r,color):
    ellipse(im,x-r*.34,y,r*.72,r,color)
    ellipse(im,x+r*.34,y,r*.72,r,color)
    ellipse(im,x-r*.3,y-r*.15,r*.2,r*.4,'#d79668')
    path(im,[('M',(x,y-r*.82)),('C',(x+2,y-r-2),(x,y-r-6),(x+3,y-r-8))],stroke='#66714d',width=1.8)
    leaf(im,(x+1,y-r-3),(x+12,y-r-7),4,'#738553')


def table(im):
    ellipse(im,526,961,108,16,'#a4ad80')
    path(im,[('M',(431,825)),('C',(434,878),(435,934),(448,960)),
             ('C',(492,975),(554,973),(596,958)),('C',(606,923),(612,866),(619,825)),('L',(431,825))],fill='#9d7953')
    path(im,[('M',(462,840)),('C',(465,883),(462,942),(475,966)),
             ('L',(517,971)),('C',(510,923),(521,878),(514,840)),('L',(462,840))],fill='#ad8a5b')
    for x,y,ex,ey in [(448,866,458,945),(480,884,480,951),(534,856,530,938),
                      (565,872,558,955),(596,857,589,930)]:
        path(im,[('M',(x,y)),('C',(x+5,y+26),(ex-4,ey-20),(ex,ey))],stroke='#7e664c',width=2)
    ellipse(im,525,826,95,27,'#dfc49a')
    ellipse(im,526,825,75,18,None,'#b5966d',1.3)
    ellipse(im,526,825,53,12,None,'#b5966d',1)
    ellipse(im,530,825,23,6,None,'#b5966d',1)
    ellipse(im,521,833,52,8,'#b39868')
    # Basket bottom lies on the stump surface; the fruit sits inside the rim.
    path(im,[('M',(474,794)),('C',(478,813),(482,824),(494,828)),
             ('C',(511,835),(542,832),(555,825)),('L',(566,795)),('L',(474,794))],fill='#bc955f')
    for y in (806,816,824):
        path(im,[('M',(484,y)),('C',(507,y+5),(535,y+5),(556,y-1))],stroke='#d7b980',width=1.8)
    for x in (493,507,523,539):line(im,[(x,800),(x+3,827)],'#95794e',1.2)
    ellipse(im,520,795,48,13,'#796b46')
    apple(im,501,788,13,'#b9624e')
    apple(im,542,789,11,'#bb7555')
    path(im,[('M',(517,787)),('C',(510,777),(518,774),(521,764)),
             ('C',(530,766),(532,777),(537,783)),('C',(545,803),(517,806),(517,787))],fill='#c0b768')
    path(im,[('M',(522,766)),('L',(524,757))],stroke='#6e7751',width=1.6)
    for x,y in [(510,803),(526,802),(542,803),(550,797)]:
        ellipse(im,x,y,4,4,'#765465')
    path(im,[('M',(474,794)),('C',(493,809),(547,809),(566,795))],stroke='#dfbc7f',width=5)


def hedgehog(im):
    ellipse(im,531,1104,103,13,'#a8af80')
    ellipse(im,481,1099,12,8,'#90754f')
    ellipse(im,561,1101,12,7,'#90754f')
    # Quills belong to the dorsal mass; the face and belly stay unspiked.
    pp=[]
    for i in range(45):
        angle=math.pi+i/44*math.pi
        radius=1.04 if i%2 else .97
        pp.append((514+99*math.cos(angle)*radius,1051+77*math.sin(angle)*radius))
    pp.extend([(612,1073),(586,1102),(460,1105),(424,1085),pp[0]])
    ImageDraw.Draw(im).polygon([(x*S,y*S) for x,y in pp],fill=rgb('#796a50'))
    rng=random.Random(49)
    for _ in range(92):
        x=rng.uniform(434,597)
        y=rng.uniform(984,1081)
        if ((x-514)/93)**2+((y-1051)/70)**2>1:
            continue
        dx,dy=(x-514)/8,(y-1077)/9
        line(im,[(x,y),(x+dx,y+dy)],rng.choice(['#a08b61','#c1a877','#b09a6c']),1.4)
    face=[('M',(552,1018)),('C',(588,1028),(625,1053),(645,1077)),
          ('C',(647,1084),(604,1097),(573,1096)),('C',(520,1097),(515,1076),(539,1045)),('L',(552,1018))]
    path(im,face,fill='#d9c7a0')
    ellipse(im,559,1035,12,14,'#c2ac85')
    ellipse(im,560,1036,7,9,'#a88e6c')
    eye(im,604,1062,4.3)
    ellipse(im,644,1079,5,3.8,'#3c4f40')
    path(im,[('M',(630,1087)),('C',(622,1090),(614,1090),(608,1087))],stroke='#a78e68',width=1)
    apple(im,665,1097,10,'#b36450')


def mushroom(im,x,y,r,color):
    path(im,[('M',(x-r*.15,y-r*.15)),('L',(x-r*.19,y+r*.9)),
             ('C',(x-r*.05,y+r),(x+r*.19,y+r),(x+r*.22,y+r*.82)),('L',(x+r*.15,y-r*.15))],fill='#dfd2a8')
    path(im,[('M',(x-r,y)),('C',(x-r,y-r*.75),(x-r*.32,y-r),(x,y-r*.8)),
             ('C',(x+r*.58,y-r*.9),(x+r*.91,y-r*.5),(x+r,y)),
             ('C',(x+r*.45,y+r*.14),(x-r*.44,y+r*.12),(x-r,y))],fill=color)
    ellipse(im,x-r*.34,y-r*.45,r*.14,r*.08,'#e8d5ab')
    ellipse(im,x+r*.26,y-r*.49,r*.11,r*.07,'#e8d5ab')


PROTECT_MARGIN=12
PROTECTED_SHAPES=[FOX_TAIL,FOX_BODY,FOX_HEAD,
                  RABBIT_BODY,RABBIT_HEAD,*RABBIT_EARS,
                  DEER_BODY,DEER_NECK,DEER_HEAD,*DEER_EARS,
                  SQUIRREL_TAIL,SQUIRREL_BODY,SQUIRREL_HEAD,
                  [('M',(431,825)),('L',(446,958)),('L',(596,958)),('L',(619,825))],
                  [('M',(352,772)),('L',(399,801)),('L',(454,818)),('L',(439,837)),('L',(391,828))]]
PROTECTED_ELLIPSES=[(525,826,95,27),(514,1050,103,78),(644,1079,10,8),(665,1097,12,12),
                    (308,941,40,14),(709,922,55,16)]
PROTECTED_LEGS=[((570,680),(564,780)),((595,696),(592,791)),((642,696),(659,789)),((660,689),(687,781))]


@lru_cache(maxsize=1)
def protection_mask():
    """Silhouettes of the animals and props, grown by PROTECT_MARGIN, at page scale."""
    im=Image.new('L',SIZE)
    d=ImageDraw.Draw(im)
    for shape in PROTECTED_SHAPES:
        d.polygon(sample(shape),fill=255)
    for x,y,rx,ry in PROTECTED_ELLIPSES:
        d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
    for a,b in PROTECTED_LEGS:
        d.line([a,b],fill=255,width=14)
    return im.filter(ImageFilter.MaxFilter(PROTECT_MARGIN*2+1))


def grass_allowed(x,y):
    width,height=SIZE
    if not (0<=x<width and 0<=y<height):
        return False
    return protection_mask().getpixel((int(x),int(y)))==0


def floor_detail(im):
    rng=random.Random(73)
    # Small clustered grasses hug the ground and stay outside the character faces.
    for _ in range(115):
        x=rng.uniform(180,844)
        y=rng.uniform(745,1233)
        if not grass_allowed(x,y):
            continue
        col=rng.choice(['#7f9465','#9caa74','#a6b27d'])
        for j in (-1,0,1):
            line(im,[(x,y),(x+j*5,y-rng.uniform(6,14))],col,1.1)
    for x,y in [(331,1043),(705,1025),(398,1141),(747,1130),(254,1087),(811,976)]:
        sprig(im,(x,y),(x+14,y-52),3,'#90a272','#70845b',int(x+y),5)
    for x,y,r,col in [(193,1077,22,'#b07755'),(227,1098,14,'#c39365'),
                      (825,1021,20,'#b47554'),(853,1040,13,'#c39667')]:
        mushroom(im,x,y,r,col)
    # Foreground leaves create the full-bleed frame; no principal face is covered.
    path(im,[('M',(0,1063)),('C',(69,1002),(151,1072),(156,1135)),
             ('C',(250,1090),(263,1204),(310,1250)),('L',(0,1250))],fill='#234c42')
    path(im,[('M',(1000,1019)),('C',(946,998),(889,1042),(898,1117)),
             ('C',(817,1072),(788,1204),(735,1250)),('L',(1000,1250))],fill='#244e43')
    foreground=[((6,1236),(168,1095),6,'#557c55',1,14),((87,1247),(215,1165),5,'#7b925b',2,12),
                ((989,1234),(814,1080),7,'#5b8055',3,13),((959,1237),(774,1210),5,'#809461',4,12)]
    for b,t,n,col,seed,width in foreground:
        sprig(im,b,t,n,col,'#93a66b',seed,width,'broad' if seed in (2,4) else 'frond')
    for root,tip,width,color in [((0,1168),(81,1054),37,'#486f4f'),((64,1230),(118,1111),36,'#597e52'),
                                ((972,1212),(917,1059),37,'#618352'),((1000,1138),(955,1038),30,'#4f7550')]:
        leaf(im,root,tip,width,color,'#8ca067')
    # A handful of flowers, attached to stems instead of scattered decoration.
    for x,y in [(215,1181),(249,1218),(801,1185),(840,1157),(282,1090)]:
        line(im,[(x,y),(x-2,y+26)],'#7b9460',1.2)
        for a in range(5):
            angle=a/5*math.tau
            ellipse(im,x+math.cos(angle)*4.5,y+math.sin(angle)*4.5,3.7,3.7,'#e5ce98')
        ellipse(im,x,y,2.5,2.5,'#bf9959')


def pigment(im):
    # Light, print-like grain keeps the silhouette crisp; no global blur/filter rescue.
    rng=np.random.default_rng(103)
    arr=np.asarray(im).astype(np.int16)
    noise=rng.normal(0,1.12,arr.shape[:2]).astype(np.int16)
    arr=np.clip(arr+noise[:,:,None],0,255).astype(np.uint8)
    im.paste(Image.fromarray(arr))


def full_scene():
    im=Image.new('RGB',(3000,3750))
    forest(im)
    deer(im)
    squirrel(im)
    sparrow(im)
    fox(im)
    rabbit(im)
    table(im)
    # Foreground paws remain in front of the stump, not hidden by its rim.
    path(im,[('M',(421,805)),('L',(442,807)),('C',(454,818),(453,833),(439,837)),
             ('L',(418,831)),('L',(421,805))],fill='#e9cea0')
    for x in (433,439):
        path(im,[('M',(x,817)),('L',(x+3,827))],stroke='#b99a70',width=1)
    # The fox pushes an apple across the stump top; its shadow lies on the wood, inside the rim.
    ellipse(im,457,834,13,3.6,'#a98c63')
    apple(im,456,821,12,'#bb6550')
    path(im,[('M',(623,807)),('C',(613,812),(615,824),(627,826)),('L',(634,823)),('L',(631,806)),('L',(623,807))],fill='#eee2bf')
    hedgehog(im)
    floor_detail(im)
    pigment(im)
    return im


if __name__=='__main__':
    if '--layout' in sys.argv:
        layout()
    else:
        image=full_scene().resize((2400,3000),Image.Resampling.LANCZOS)
        image.save(ROOT/'forest-gathering.png',dpi=(300,300))
        image.resize((600,750),Image.Resampling.LANCZOS).save(ROOT/'preview.png')
        print('Saved forest-gathering.png and preview.png')
