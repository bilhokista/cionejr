"""Three authored digital styles, not physical print/paint or a model benchmark."""
from pathlib import Path
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops

ROOT = Path(__file__).parent
S = 3
W,H = 900,760
PAPER = '#f4efe3'

BODY = [('M',(125,584)),('C',(192,530),(255,478),(322,443)),
        ('C',(370,384),(423,335),(487,301)),
        ('C',(512,286),(535,274),(555,260)),
        ('C',(557,212),(580,163),(629,150)),
        ('C',(669,136),(713,165),(733,201)),
        ('L',(800,236)),('C',(780,246),(759,250),(741,250)),
        ('C',(742,300),(724,383),(700,433)),
        ('C',(667,498),(598,541),(530,549)),
        ('C',(484,557),(444,538),(411,514)),
        ('C',(390,499),(364,490),(342,479)),
        ('C',(266,524),(191,564),(125,584))]
WING = [('M',(547,287)),('C',(488,298),(437,335),(396,381)),
        ('C',(361,420),(339,440),(318,459)),
        ('C',(392,463),(468,445),(517,408)),
        ('C',(558,375),(579,325),(562,302)),
        ('C',(558,294),(552,289),(547,287))]
TAIL = [('M',(353,440)),('C',(265,482),(191,535),(125,584)),
        ('C',(203,563),(274,525),(352,480)),('L',(388,461)),('L',(353,440))]
CROWN = [('M',(555,260)),('C',(557,212),(580,163),(629,150)),
         ('C',(669,136),(713,165),(733,201)),('L',(735,216)),
         ('C',(693,193),(645,203),(601,225)),
         ('C',(587,242),(577,256),(574,272)),('L',(555,260))]
CHEEK = [('M',(601,225)),('C',(633,201),(683,204),(717,230)),
         ('C',(742,256),(731,299),(709,326)),
         ('C',(671,334),(615,303),(585,274)),
         ('C',(588,252),(592,236),(601,225))]
EAR = [('M',(634,246)),('C',(650,242),(654,254),(667,264)),
       ('C',(678,276),(675,292),(665,299)),
       ('C',(647,298),(627,283),(622,268)),
       ('C',(620,257),(625,249),(634,246))]
MASK = [('M',(677,208)),('C',(695,204),(716,206),(735,210)),
        ('L',(741,240)),('L',(716,266)),
        ('C',(703,250),(691,241),(679,240)),
        ('C',(673,230),(672,217),(677,208))]
BIB = [('M',(724,238)),('L',(742,248)),
       ('C',(744,287),(730,338),(720,351)),
       ('C',(703,332),(705,317),(710,287)),
       ('C',(719,265),(720,250),(724,238))]
BELLY_SHADOW = [('M',(393,455)),('C',(442,496),(522,509),(591,490)),
                ('C',(644,475),(680,448),(702,425)),
                ('C',(665,506),(594,543),(530,549)),
                ('C',(478,557),(429,528),(411,514)),('L',(393,455))]
BACK = [('M',(322,443)),('C',(389,363),(482,295),(555,260)),
        ('L',(584,288)),('C',(568,332),(487,385),(440,407)),
        ('L',(322,443))]
SCAPULAR = [('M',(545,294)),('C',(504,300),(464,324),(436,354)),
            ('C',(459,374),(494,378),(520,359)),
            ('C',(545,341),(556,307),(545,294))]
FLIGHTS = [
    [('M',(522,340)),('C',(470,357),(403,410),(341,446)),
     ('C',(398,440),(461,414),(526,368)),('C',(531,358),(530,347),(522,340))],
    [('M',(541,361)),('C',(496,386),(432,426),(375,448)),
     ('C',(439,447),(504,418),(550,383)),('L',(541,361))],
    [('M',(552,335)),('C',(545,365),(522,390),(499,405)),
     ('C',(531,398),(558,372),(566,343)),('L',(552,335))],
]
BRANCH = [('M',(113,661)),('C',(339,642),(595,630),(814,616)),
          ('L',(825,628)),('C',(575,648),(334,662),(120,675)),('L',(113,661))]
LEGS = [ [('M',(532,538)),('C',(523,562),(527,573),(538,596)),('L',(552,635))],
         [('M',(582,523)),('C',(573,550),(573,566),(586,584)),('L',(613,632))] ]
TOES = [ [('M',(552,635)),('C',(537,632),(522,635),(513,646))],
         [('M',(552,635)),('C',(563,633),(574,633),(584,640))],
         [('M',(552,635)),('C',(550,643),(541,648),(538,647))],
         [('M',(613,632)),('C',(628,626),(643,629),(651,638)),('C',(654,643),(651,646),(648,646))],
         [('M',(613,632)),('C',(630,635),(637,641),(635,648))],
         [('M',(613,632)),('C',(600,631),(590,637),(587,643))] ]


def rgb(color):
    if isinstance(color,str):
        return tuple(bytes.fromhex(color.lstrip('#')))
    return tuple(color)


def points(commands):
    result=[]
    current=None
    for kind,*coords in commands:
        if kind in ('M','L'):
            current=coords[0]
            result.append(current)
        elif kind=='C':
            a,b,c=coords
            origin=current
            for i in range(1,51):
                t=i/50
                result.append(tuple((1-t)**3*origin[j]+3*(1-t)**2*t*a[j]
                                    +3*(1-t)*t*t*b[j]+t**3*c[j] for j in (0,1)))
            current=c
        else:
            raise ValueError(kind)
    return result


def drawpath(image,commands,fill=None,stroke=None,width=1):
    pp=[(round(x*S),round(y*S)) for x,y in points(commands)]
    d=ImageDraw.Draw(image)
    if fill is not None:
        d.polygon(pp,fill=rgb(fill))
    if stroke is not None:
        d.line(pp,fill=rgb(stroke),width=max(1,round(width*S)),joint='curve')


def line(image,pp,color,width=1):
    ImageDraw.Draw(image).line([(round(x*S),round(y*S)) for x,y in pp],
                              fill=rgb(color),width=max(1,round(width*S)),joint='curve')


def shape_mask(commands):
    result=Image.new('L',(W*S,H*S))
    ImageDraw.Draw(result).polygon([(round(x*S),round(y*S)) for x,y in points(commands)],fill=255)
    return result


def clipped(image,mask,paint):
    result=image.copy()
    paint(result)
    image.paste(result,(0,0),mask)


def disk(image,x,y,r,color):
    ImageDraw.Draw(image).ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=rgb(color))


def supports(image,ink,branch,painter=False):
    drawpath(image,BRANCH,fill=branch)
    if painter:
        drawpath(image,[('M',(137,668)),('C',(360,648),(632,638),(805,623))],stroke='#867c60',width=2.7)
        drawpath(image,[('M',(265,653)),('C',(427,646),(574,638),(690,633))],stroke='#ab9b72',width=1.4)
    for leg in LEGS:
        drawpath(image,leg,stroke=ink,width=4.8 if painter else 4)
    for toe in TOES:
        drawpath(image,toe,stroke=ink,width=3.4 if painter else 3)
    if painter:
        for leg in LEGS:
            pp=[(x-1,y-1) for x,y in points(leg)]
            line(image,pp,'#d8ae89',1.4)
        for toe in TOES:
            pp=[(x,y-1) for x,y in points(toe)]
            line(image,pp,'#d8ad84',1)


def face(image,dark,cheek,crown,painting=False):
    drawpath(image,CROWN,fill=crown)
    drawpath(image,CHEEK,fill=cheek)
    drawpath(image,MASK,fill=dark)
    drawpath(image,EAR,fill=dark)
    drawpath(image,BIB,fill=dark)
    drawpath(image,[('M',(733,201)),('L',(800,236)),('L',(741,239)),('L',(733,201))],fill='#4b5048' if painting else dark)
    drawpath(image,[('M',(741,239)),('L',(800,236)),('L',(741,250)),('L',(741,239))],fill=dark)
    if painting:
        drawpath(image,[('M',(744,216)),('C',(759,222),(773,229),(790,234))],stroke='#7b8072',width=2)
    disk(image,697,220,10 if painting else 8.5,cheek if not painting else '#797967')
    disk(image,697,220,7.7 if painting else 7,dark)
    disk(image,699.5,217,2.1,'#fff8dd')


def geometric():
    image=Image.new('RGB',(W*S,H*S),rgb(PAPER))
    supports(image,'#725947','#a4aa8c')
    drawpath(image,BODY,fill='#ddd2b4')
    drawpath(image,BELLY_SHADOW,fill='#b7b89b')
    drawpath(image,TAIL,fill='#5b6658')
    drawpath(image,BACK,fill='#bc774d')
    drawpath(image,WING,fill='#745c45')
    drawpath(image,FLIGHTS[0],fill='#c69a65')
    drawpath(image,FLIGHTS[1],fill='#3e554b')
    drawpath(image,FLIGHTS[2],fill='#a67c51')
    drawpath(image,SCAPULAR,fill='#c58955')
    drawpath(image,[('M',(444,355)),('C',(465,365),(494,364),(512,351))],stroke='#f2e5c4',width=6)
    drawpath(image,[('M',(458,384)),('C',(476,381),(495,371),(510,363))],stroke='#e8d8b6',width=3.5)
    face(image,'#2e433b','#f3e9ce','#a56140')
    # Optical adjustments replace rigid perfect-circle head construction.
    return image


def lino():
    paper=PAPER
    ink='#4e392f'
    image=Image.new('RGB',(W*S,H*S),rgb(paper))
    supports(image,ink,ink)
    drawpath(image,BODY,fill=ink)
    # The cheek is a carved white shape; other light areas are directional cuts.
    drawpath(image,CHEEK,fill=paper)
    drawpath(image,EAR,fill=ink)
    bodymask=shape_mask(BODY)
    # Flank: long curved gouges fanning along the belly, not surface tiles.
    def cuts(layer):
        for i in range(26):
            t=i/25
            sx=397+208*t
            sy=429-37*t
            ex=442+214*t
            ey=517-30*t
            drawpath(layer,[('M',(sx,sy)),('C',(sx+3,sy+29),(ex-17,ey-12),(ex,ey))],
                     stroke=paper,width=1.3+(.55 if i%4==0 else 0))
        for i in range(10):
            drawpath(layer,[('M',(644+i*6,331+i*2)),
                            ('C',(650+i*6,357+i*3),(644+i*6,385+i*3),(632+i*6,411+i*3))],
                     stroke=paper,width=1.3)
    clipped(image,bodymask,cuts)
    # Folded wing has a different cut grammar from the flank.
    drawpath(image,WING,fill=ink)
    drawpath(image,WING,stroke=paper,width=2.2)
    wingmask=shape_mask(WING)
    def wingcuts(layer):
        for i in range(9):
            sx=350+i*16
            sy=449-i*2.4
            ex=512+i*5
            ey=336+i*5
            drawpath(layer,[('M',(sx,sy)),('C',(sx+59,sy-21),(ex-36,ey+48),(ex,ey))],
                     stroke=paper,width=1.8 if i%3 else 2.6)
        for x,y,dx,dy in [(433,350,35,-28),(459,337,28,-25),(486,323,22,-15),(516,310,20,-11)]:
            drawpath(layer,[('M',(x,y)),('C',(x+7,y-6),(x+dx-8,y+dy-3),(x+dx,y+dy))],stroke=paper,width=2.5)
        drawpath(layer,[('M',(427,366)),('C',(452,379),(480,371),(503,353))],stroke=paper,width=5)
        drawpath(layer,[('M',(443,390)),('C',(463,389),(491,374),(511,363))],stroke=paper,width=3.2)
    clipped(image,wingmask,wingcuts)
    # Crown gouges follow the crown arc and leave a solid boundary at the brow.
    crownmask=shape_mask(CROWN)
    def crowncuts(layer):
        for i in range(17):
            x=571+i*7.3
            drawpath(layer,[('M',(x,239-i*.7)),
                            ('C',(x+1,213-i*.6),(x+14,185-i*.2),(x+36,172+i*.65))],
                     stroke=paper,width=1.45)
    clipped(image,crownmask,crowncuts)
    # Tail grain and narrow collar have long cuts instead of feather stamping.
    for i in range(5):
        drawpath(image,[('M',(148+i*4,574-i*3)),('C',(214,536-i*3),(277,502-i*4),(342,468-i*4))],
                 stroke=paper,width=1.4)
    drawpath(image,[('M',(571,270)),('C',(581,282),(600,298),(621,308))],stroke=paper,width=4)
    drawpath(image,MASK,fill=ink)
    drawpath(image,BIB,fill=ink)
    drawpath(image,[('M',(735,210)),('L',(800,236)),('L',(741,250)),('L',(735,210))],fill=ink)
    drawpath(image,[('M',(748,233)),('L',(785,237))],stroke=paper,width=1.3)
    # Carve toe separators so the feet do not disappear into the same-colour perch.
    drawpath(image,[('M',(542,640)),('C',(541,644),(539,646),(537,647))],stroke=paper,width=1.6)
    drawpath(image,[('M',(630,637)),('C',(633,640),(633,644),(632,646))],stroke=paper,width=1.8)
    drawpath(image,[('M',(646,636)),('C',(649,640),(649,644),(647,647))],stroke=paper,width=1.5)
    disk(image,697,220,9.6,paper)
    disk(image,697,220,6.5,ink)
    disk(image,699,217,1.5,paper)
    # Sparse print imperfections are clipped to ink, not a decorative full-image filter.
    arr=np.array(image)
    rng=np.random.default_rng(41)
    select=(rng.random(arr.shape[:2])<.003)&(arr[:,:,0]<110)
    arr[select]=rgb(paper)
    return Image.fromarray(arr)


def painted_field(image,commands,color,seed,variation=6,softness=.65,parent=None):
    mask=shape_mask(commands)
    if softness:
        mask=mask.filter(ImageFilter.GaussianBlur(softness*S))
    if parent is not None:
        mask=ImageChops.multiply(mask,parent)
    box=mask.getbbox()
    x0,y0,x1,y1=box
    rng=np.random.default_rng(seed)
    height,width=y1-y0,x1-x0
    # Low-frequency pigment and fine paper grain, both local to the paint layer.
    low=Image.fromarray(rng.integers(95,160,(max(2,height//42),max(2,width//42)),dtype=np.uint8))
    low=np.asarray(low.resize((width,height),Image.Resampling.BICUBIC),dtype=np.float32)-128
    grain=rng.normal(0,1.7,(height,width))
    # Opaque paint keeps discrete pigment variations rather than smooth airbrush shading.
    pigment=np.round(low/5)*5
    yy,xx=np.mgrid[0:height,0:width]
    bristle=np.sin((xx*.32+yy*.11))*1.05
    base=np.array(rgb(color),dtype=np.float32)
    tex=base[None,None,:]+(pigment*variation/24+grain+bristle)[:,:,None]
    patch=Image.fromarray(np.clip(tex,0,255).astype(np.uint8))
    image.paste(patch,(x0,y0),mask.crop(box))


def gouache():
    image=Image.new('RGB',(W*S,H*S),rgb(PAPER))
    supports(image,'#9b7160','#687f6c',True)
    bodymask=shape_mask(BODY)
    painted_field(image,BODY,'#d5c29d',51,8,softness=1.15)
    painted_field(image,BELLY_SHADOW,'#a2aa90',52,8,softness=5,parent=bodymask)
    # Light and shade are painted masses, softened locally rather than a global filter.
    light=[('M',(586,314)),('C',(622,310),(672,324),(699,353)),
           ('C',(700,407),(644,463),(587,483)),
           ('C',(550,461),(552,379),(586,314))]
    painted_field(image,light,'#e4d5b2',76,7,softness=8,parent=bodymask)
    painted_field(image,TAIL,'#606559',53,7,softness=.8,parent=bodymask)
    painted_field(image,BACK,'#b18450',54,12,softness=2,parent=bodymask)
    painted_field(image,WING,'#65523b',55,10,softness=1.8,parent=bodymask)
    painted_field(image,FLIGHTS[0],'#ac986b',56,8,softness=1.3)
    painted_field(image,FLIGHTS[1],'#4e5d4d',57,7,softness=1.25)
    painted_field(image,FLIGHTS[2],'#94815a',58,9,softness=1.4)
    painted_field(image,SCAPULAR,'#a17045',59,12,softness=4)
    # Broad shadow and light strokes describe coverts without a repeated petal motif.
    strokes=[(506,308,481,334,'#6b4e35',7),(534,310,517,335,'#704d35',9),
             (478,332,460,349,'#c7a163',6),(520,342,500,352,'#c3a16c',7),
             (473,361,443,374,'#d4c6a0',5),(502,356,480,369,'#e2d0a5',4),
             (504,382,470,399,'#d4bf87',3),(456,406,430,418,'#cdbb8b',2.8),
             (466,327,445,341,'#6d563d',4),(432,355,418,367,'#e0bf82',4)]
    def wingpaint(layer):
        for x,y,ex,ey,col,width in strokes:
            drawpath(layer,[('M',(x,y)),('C',((x+ex)/2+2,y+3),(ex+4,ey-2),(ex,ey))],stroke=col,width=width)
        for i in range(7):
            drawpath(layer,[('M',(352+i*18,449-i*2)),
                            ('C',(412+i*12,420-i*2),(480+i*6,380),(522+i*3,349+i*4))],
                     stroke='#baa273',width=1.15)
    clipped(image,shape_mask(WING),wingpaint)
    painted_field(image,CROWN,'#986140',60,13,softness=1.4,parent=bodymask)
    painted_field(image,CHEEK,'#eee1bf',61,6,softness=2.2,parent=bodymask)
    painted_field(image,MASK,'#3f493c',62,6,softness=1.2,parent=bodymask)
    painted_field(image,EAR,'#454b3c',63,7,softness=1.7)
    painted_field(image,BIB,'#3e5141',64,8,softness=1.5,parent=bodymask)
    # A few grouped, differently oriented strokes describe the short plumage.
    rng=random.Random(65)
    bodymask=shape_mask(BODY)
    excluded=ImageChops.lighter(shape_mask(WING),shape_mask(CROWN))
    excluded=ImageChops.lighter(excluded,shape_mask(CHEEK))
    excluded=ImageChops.lighter(excluded,shape_mask(BIB))
    allowed=ImageChops.subtract(bodymask,excluded)
    def plumage(layer):
        # Broken opaque brush passes are part of the form, not uniform surface noise.
        broad=[(618,340,636,390,'#e8d9b7',7),(608,383,619,422,'#e3d4af',6),
               (575,426,588,462,'#dacaab',5),(542,463,555,490,'#cfc5a4',5),
               (515,483,521,514,'#b6b79a',6),(581,491,588,520,'#b1b599',5),
               (644,427,635,454,'#d6cfac',5),(669,389,661,418,'#e5d8b4',5)]
        for x,y,ex,ey,tone,width in broad:
            drawpath(layer,[('M',(x,y)),('C',(x-1,y+8),(ex+3,ey-7),(ex,ey))],stroke=tone,width=width)
        for _ in range(130):
            x=rng.uniform(388,711)
            y=rng.uniform(300,538)
            angle=.55+1.1*(y-320)/250
            length=rng.uniform(5,16)
            ex=x+math.cos(angle)*length
            ey=y+math.sin(angle)*length
            tone=rng.choice(['#cec3a2','#ddd0ae','#beb89b','#dfcfaa'])
            drawpath(layer,[('M',(x,y)),('C',(x+1,y+length*.3),(ex-2,ey-2),(ex,ey))],
                     stroke=tone,width=rng.uniform(.7,2.3))
    clipped(image,allowed,plumage)
    # Crown brush marks follow its curved mass, not the flank's mark recipe.
    def crownpaint(layer):
        rng=random.Random(83)
        for _ in range(70):
            x=rng.uniform(570,728)
            y=rng.uniform(160,269)
            length=rng.uniform(5,19)
            angle=-.65+(x-635)*.007
            dx,dy=length*math.cos(angle),length*math.sin(angle)
            drawpath(layer,[('M',(x,y)),('C',(x+dx*.4,y+dy*.3),(x+dx*.8,y+dy),(x+dx,y+dy))],
                     stroke=rng.choice(['#aa724b','#a66b44','#b67d50','#8d593b']),width=rng.uniform(.8,2.8))
    clipped(image,shape_mask(CROWN),crownpaint)
    # Dark cheek patch and bib retain painted edges, no hard vector outline.
    for p,col in [(EAR,'#535440'),(BIB,'#53614b')]:
        def darkpaint(layer, col=col):
            rr=random.Random(94)
            for _ in range(65):
                x=rr.uniform(620,747)
                y=rr.uniform(245,351)
                line(layer,[(x,y),(x+1,y+5)],col,.6)
        clipped(image,shape_mask(p),darkpaint)
    drawpath(image,[('M',(736,209)),('C',(758,216),(780,226),(800,236)),
                    ('C',(780,246),(759,251),(741,250)),('L',(736,209))],fill='#444a40')
    drawpath(image,[('M',(742,216)),('C',(756,220),(777,230),(791,234))],stroke='#7c8070',width=2.4)
    drawpath(image,[('M',(746,240)),('C',(762,239),(776,237),(791,238))],stroke='#afb299',width=.85)
    disk(image,697,220,10,'#7d7962')
    disk(image,697,220,8,'#252f28')
    disk(image,699,217,2,'#fff8e2')
    disk(image,694,224,1,'#687b64')
    return image


def construction():
    image=Image.new('RGB',(W*S,H*S),rgb(PAPER))
    supports(image,'#aaa99a','#c8c7b5')
    drawpath(image,BODY,stroke='#868e80',width=1)
    drawpath(image,WING,stroke='#aaa99a',width=.8)
    d=ImageDraw.Draw(image)
    d.ellipse((552*S,146*S,743*S,330*S),outline='#bfbdab',width=2)
    # Tilted body oval, intentionally not used as the final contour.
    pp=[]
    for i in range(241):
        a=i/240*math.tau
        x,y=204*math.cos(a),117*math.sin(a)
        phi=-.65
        pp.append((526+x*math.cos(phi)-y*math.sin(phi),407+x*math.sin(phi)+y*math.cos(phi)))
    line(image,pp,'#bfbdab',.8)
    line(image,[(335,488),(690,212)],'#b6b9a9',.8)
    for x,y in [(555,260),(697,220),(741,250),(530,549),(552,635),(613,632)]:
        disk(image,x,y,2.3,'#889982')
    return image


def choose_label_font(size=36):
    try:
        return ImageFont.truetype('DejaVuSerif.ttf',size)
    except OSError:
        return ImageFont.load_default(size=size)


def main():
    builders=[('geometris',geometric),('linocut',lino),('gouache',gouache)]
    panels=[]
    for name,build in builders:
        image=build().resize((1800,1520),Image.Resampling.LANCZOS)
        image.save(ROOT/f'{name}.png')
        panels.append(image)
    construction().resize((1800,1520),Image.Resampling.LANCZOS).save(ROOT/'construction.png')
    sheet=Image.new('RGB',(3240,1440),rgb(PAPER))
    font=choose_label_font(36)
    for i,((name,_),image) in enumerate(zip(builders,panels)):
        fit=image.resize((1044,882),Image.Resampling.LANCZOS)
        sheet.paste(fit,(i*1080+18,233))
        d=ImageDraw.Draw(sheet)
        label=name.capitalize()
        box=d.textbbox((0,0),label,font=font)
        x=i*1080+(1080-(box[2]-box[0]))//2
        d.text((x,1210),label,font=font,fill='#4e5148')
    sheet.save(ROOT/'three-styles.png')
    sheet.resize((1080,480),Image.Resampling.LANCZOS).save(ROOT/'preview.png')
    print('Rendered three styles, construction and preview')

if __name__=='__main__':
    main()
