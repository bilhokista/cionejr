"""Drawing helpers and the woodland cast, constructed from edited flat forms.

Each animal function draws one character in a shared 1000 x 1250 design space at
3x supersampling; render.py cuts them out and places them in the scene.
"""
import math
import random
import numpy as np
from PIL import Image, ImageDraw

S=3
SIZE=(1000,1250)

def offset(commands,dx,dy):
    return [(kind,*[(x+dx,y+dy) for x,y in coords]) for kind,*coords in commands]


DEER_HEAD_SHIFT=(-4,10)  # the head dips toward the basket
FOX_BODY=[('M',(318,716)),('C',(280,716),(262,745),(257,790)),
          ('C',(250,840),(226,885),(238,925)),('C',(250,957),(300,964),(345,952)),
          ('C',(372,944),(381,925),(378,895)),('C',(376,850),(373,820),(371,790)),
          ('C',(369,750),(352,720),(318,716))]
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
DEER_NECK=[('M',(526,598)),('C',(514,630),(508,660),(530,690)),
           ('C',(540,706),(562,714),(592,708)),('L',(630,668)),('L',(598,630)),
           ('C',(584,628),(570,622),(564,606)),('L',(526,598))]
DEER_CHEST=[('M',(518,610)),('C',(522,636),(516,662),(536,690)),
            ('C',(546,702),(556,709),(566,713)),('C',(560,692),(546,668),(544,642)),
            ('C',(543,626),(546,614),(548,606)),('L',(518,610))]
DEER_LEGS=[([(572,684),(570,735),(566,774)],'#aa9066',11),
           ([(598,696),(598,742),(592,786)],'#c1a879',12),
           ([(640,700),(640,738),(654,755),(660,781)],'#aa9066',11),
           ([(662,692),(660,735),(676,752),(686,778)],'#c1a879',12)]
DEER_HEAD_RAW=[('M',(505,523)),('C',(519,502),(551,502),(565,523)),
           ('C',(578,545),(569,575),(550,600)),('C',(536,615),(526,610),(513,595)),
           ('C',(496,574),(493,544),(505,523))]
DEER_EARS_RAW=[ [('M',(511,535)),('C',(480,526),(456,507),(463,486)),
            ('C',(484,482),(506,503),(523,528)),('L',(511,535))],
            [('M',(555,527)),('C',(559,500),(577,474),(596,477)),
             ('C',(607,497),(584,522),(565,538)),('L',(555,527))] ]
DEER_HEAD=offset(DEER_HEAD_RAW,*DEER_HEAD_SHIFT)
DEER_EARS=[offset(ear,*DEER_HEAD_SHIFT) for ear in DEER_EARS_RAW]
SQUIRREL_TAIL=[('M',(845,587)),('C',(932,560),(946,459),(890,439)),
               ('C',(834,418),(802,479),(837,517)),('C',(854,535),(894,501),(899,487)),
               ('C',(917,526),(887,558),(848,548)),('L',(845,587))]
SQUIRREL_BODY=[('M',(790,557)),('C',(774,579),(779,606),(814,622)),
               ('C',(849,635),(863,598),(848,569)),('C',(835,549),(811,548),(790,557))]
SQUIRREL_HEAD=[('M',(752,526)),('C',(764,506),(799,501),(815,520)),
               ('C',(830,544),(811,564),(784,563)),('C',(765,562),(748,553),(737,546)),
               ('C',(743,537),(747,532),(752,526))]


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


def eye(im,x,y,r=4,color='#314c43',gaze=(0,0),lid=None):
    gx,gy=gaze
    ellipse(im,x+gx*.4,y+gy*.4,r,r*1.08,color)
    ellipse(im,x+1+gx,y-1+gy,max(.75,r*.22),max(.75,r*.22),'#f6e7bf')
    if lid:
        path(im,[('M',(x-r*1.25,y-r*.45)),('C',(x-r*.5,y-r*1.15),(x+r*.5,y-r*1.15),(x+r*1.25,y-r*.45))],
             stroke=lid,width=1.6)


def on_branch(branch,t):
    """Point at parameter t on a single-cubic branch, so foliage can start on the wood."""
    (_,start),(_,a,b,end)=branch
    return tuple((1-t)**3*start[j]+3*(1-t)**2*t*a[j]+3*(1-t)*t*t*b[j]+t**3*end[j] for j in (0,1))


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


def deer(im):
    hx,hy=DEER_HEAD_SHIFT
    hp=lambda commands,**kw:path(im,offset(commands,hx,hy),**kw)
    ellipse(im,624,786,97,12,'#a9b184')
    for pts,col,width in DEER_LEGS:
        line(im,pts,col,width)
        x,y=pts[-1]
        ellipse(im,x+2,y+5,8,4.5,'#5a614d')
    path(im,DEER_BODY,fill='#c2a578')
    path(im,[('M',(580,702)),('C',(608,716),(649,716),(675,685)),
             ('C',(671,724),(619,742),(582,716)),('L',(580,702))],fill='#ad946c')
    path(im,DEER_NECK,fill='#c2a578')
    path(im,DEER_CHEST,fill='#dbc394')
    for ear in DEER_EARS:path(im,ear,fill='#c2a578')
    hp([('M',(505,520)),('C',(482,515),(473,504),(474,496)),('C',(490,497),(504,510),(505,520))],fill='#957b60')
    hp([('M',(565,519)),('C',(570,500),(582,489),(590,489)),('C',(594,501),(580,516),(565,519))],fill='#957b60')
    path(im,DEER_HEAD,fill='#c9ae7f')
    hp([('M',(521,570)),('C',(532,564),(546,563),(559,574)),
        ('C',(553,604),(532,616),(521,595)),('L',(521,570))],fill='#e5d2a8')
    # The deer lowers its gaze to the basket, so attention runs fox, basket, rabbit and deer.
    eye(im,515+hx,556+hy,3.7,gaze=(.6,1.7),lid='#8d7455')
    eye(im,552+hx,554+hy,3.7,gaze=(.6,1.7),lid='#8d7455')
    ellipse(im,539+hx,594+hy,7,4,'#475747')
    hp([('M',(539,598)),('C',(536,603),(532,603),(529,601))],stroke='#7f7d5c',width=1)
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


def fox(im):
    ellipse(im,293,945,85,17,'#aab185')
    path(im,FOX_TAIL,fill='#bb7149')
    path(im,[('M',(134,923)),('C',(97,962),(132,1003),(210,1009)),
             ('C',(186,989),(174,973),(174,951)),('L',(153,963)),('L',(163,942)),('L',(145,950)),('L',(134,923))],fill='#e8d8ae')
    path(im,FOX_BODY,fill='#cb8051')
    ellipse(im,322,733,48,24,'#cb8051')
    path(im,[('M',(258,860)),('C',(240,892),(254,934),(300,948)),('C',(274,918),(268,886),(258,860))],fill='#b9703f')
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
    ellipse(im,356,784,19,24,'#cb8051')
    path(im,[('M',(350,764)),('C',(373,768),(384,790),(399,801)),('L',(442,807)),
             ('C',(454,818),(453,833),(439,837)),('L',(391,828)),
             ('C',(367,819),(347,806),(342,780)),('C',(342,772),(345,766),(350,764))],fill='#d08657')
    path(im,[('M',(421,805)),('L',(442,807)),('C',(454,818),(453,833),(439,837)),
             ('L',(418,831)),('L',(421,805))],fill='#e9cea0')
    for x in (433,439):path(im,[('M',(x,817)),('L',(x+3,827))],stroke='#b99a70',width=1)


def rabbit(im):
    ellipse(im,718,925,83,13,'#aab286')
    ellipse(im,780,859,24,24,'#ebdfbf')
    path(im,RABBIT_BODY,fill='#eee2bf')
    ellipse(im,702,782,44,26,'#eee2bf')
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


def pigment(im):
    # Light, print-like grain keeps the silhouette crisp; no global blur/filter rescue.
    rng=np.random.default_rng(103)
    arr=np.asarray(im).astype(np.int16)
    noise=rng.normal(0,1.12,arr.shape[:2]).astype(np.int16)
    arr=np.clip(arr+noise[:,:,None],0,255).astype(np.uint8)
    im.paste(Image.fromarray(arr))
