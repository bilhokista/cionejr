"""The woodland characters, drawn as vector shapes.

Each function draws one character in its own local space: the feet rest on y = 0,
the character faces right (+x), and up is negative y. `place` positions, scales
and optionally mirrors it so it faces the owl. Nothing here is raster.
"""
import math

# --- helpers ---------------------------------------------------------------------


def place(d, draw, ident, x, y, scale=1.0, flip=False, **kwargs):
    """Draw a character inside a transformed group so the SVG keeps it as one editable unit."""
    sx = -scale if flip else scale
    with d.group(ident=ident, transform=f'translate({x} {y}) scale({sx} {scale})'):
        draw(d, **kwargs)


# --- fox: seated, head raised toward the speaker ---------------------------------------

def fox(d):
    orange, deep, cream, sock = '#da7a2f', '#bd6420', '#f6ead2', '#3b2b24'
    tail = [('M', (-30, -22)), ('C', (-135, 6), (-198, -72), (-156, -156)),
            ('C', (-128, -126), (-104, -84), (-30, -74)), ('Z',)]
    clip = d.clip_path(tail)
    d.path(tail, fill=orange, ident='fox-tail')
    with d.group(clip=clip):
        d.ellipse(-158, -150, 34, 44, fill=cream)
        d.path([('M', (-60, -20)), ('C', (-80, -70), (-110, -100), (-140, -112))], stroke=deep, width=7, opacity=.5)
    # Seated body: narrow chest, round haunch.
    d.path([('M', (-46, 0)), ('C', (-64, -42), (-54, -112), (-22, -152)), ('C', (-4, -172), (32, -170), (50, -148)),
            ('C', (72, -120), (74, -62), (62, -22)), ('C', (57, -6), (46, 0), (30, 0)), ('Z',)], fill=orange, ident='fox-body')
    d.ellipse(-26, -32, 40, 31, fill=deep)
    # Forelegs end in dark socks, set side by side.
    for dx in (0, 26):
        d.path([('M', (24 + dx, -84)), ('C', (28 + dx, -52), (32 + dx, -30), (32 + dx, -10)), ('L', (50 + dx, -10)),
                ('C', (50 + dx, -30), (48 + dx, -60), (44 + dx, -88)), ('Z',)], fill=orange)
        d.path([('M', (30 + dx, -26)), ('L', (30 + dx, -4)), ('C', (30 + dx, 3), (52 + dx, 3), (52 + dx, -4)), ('L', (50 + dx, -26)), ('Z',)], fill=sock)
    d.path([('M', (26, -156)), ('C', (66, -136), (70, -80), (58, -40)), ('C', (40, -44), (22, -100), (26, -156)), ('Z',)], fill=cream)
    # Head, tipped up and to the right.
    with d.group(transform='rotate(-14 22 -152)'):
        for ear in ([('M', (-24, -205)), ('L', (-36, -266)), ('L', (8, -233)), ('Z',)],
                    [('M', (30, -234)), ('L', (58, -268)), ('L', (68, -212)), ('Z',)]):
            d.path(ear, fill=orange)
        d.path([('M', (-20, -212)), ('L', (-28, -250)), ('L', (0, -230)), ('Z',)], fill=sock, opacity=.8)
        d.path([('M', (38, -232)), ('L', (56, -254)), ('L', (62, -222)), ('Z',)], fill=sock, opacity=.8)
        d.path([('M', (-30, -170)), ('C', (-30, -205), (-12, -228), (10, -232)), ('C', (36, -236), (62, -218), (70, -196)),
                ('L', (112, -188)), ('C', (119, -182), (117, -173), (108, -169)), ('C', (80, -150), (40, -140), (10, -146)),
                ('C', (-15, -150), (-30, -155), (-30, -170)), ('Z',)], fill=orange, ident='fox-head')
        d.path([('M', (10, -146)), ('C', (40, -140), (80, -150), (108, -169)), ('C', (90, -183), (60, -178), (40, -172)),
                ('C', (20, -165), (5, -155), (10, -146)), ('Z',)], fill=cream)
        d.ellipse(112, -181, 6.5, 5.2, fill=sock)
        d.ellipse(54, -201, 5.4, 6.4, fill='#2a1d18')
        d.circle(56, -204, 1.8, fill='#fff6e0')
        d.path([('M', (42, -214)), ('C', (50, -219), (60, -218), (66, -212))], stroke=deep, width=2.4)


# --- deer: standing, neck raised ----------------------------------------------------------

def deer(d):
    coat, shade, light, hoof = '#c9a06a', '#b08655', '#ead9b4', '#4b3c30'
    # Far legs sit behind the body in a darker tone.
    for pts in ([('M', (52, -92)), ('L', (64, -92)), ('L', (60, -16)), ('L', (51, -16)), ('Z',)],
                [('M', (-66, -96)), ('C', (-78, -64), (-58, -50), (-64, -16)), ('L', (-54, -16)), ('C', (-50, -50), (-66, -64), (-52, -96)), ('Z',)]):
        d.path(pts, fill=shade)
    d.ellipse(0, -122, 98, 48, fill=coat, ident='deer-body')
    d.ellipse(6, -100, 82, 24, fill=light, opacity=.55)
    for x, y in [(-50, -146), (-22, -156), (8, -152), (34, -146), (-36, -130), (-4, -134), (24, -128), (-58, -118), (50, -126), (-14, -112)]:
        d.ellipse(x, y, 4.6, 3.2, fill='#f6ecd2')
    d.ellipse(-96, -134, 8, 14, fill='#fff2d8')
    # Near legs and hooves.
    d.path([('M', (74, -96)), ('L', (88, -96)), ('L', (82, -14)), ('L', (72, -14)), ('Z',)], fill=coat)
    d.path([('M', (-80, -100)), ('C', (-94, -70), (-72, -52), (-80, -14)), ('L', (-68, -14)), ('C', (-62, -52), (-80, -70), (-62, -100)), ('Z',)], fill=coat)
    for x in (51, 72, -66, -80):
        d.path([('M', (x - 1, -16)), ('L', (x + 12, -16)), ('L', (x + 11, 0)), ('L', (x - 2, 0)), ('Z',)], fill=hoof)
    # Neck, head and ears reach up toward the owl.
    d.path([('M', (58, -150)), ('C', (74, -192), (84, -228), (92, -266)), ('L', (120, -254)),
            ('C', (110, -216), (104, -180), (96, -138)), ('Z',)], fill=coat)
    d.path([('M', (100, -150)), ('C', (108, -190), (114, -224), (118, -252)), ('L', (126, -246)), ('C', (118, -210), (112, -176), (108, -140)), ('Z',)], fill=light, opacity=.8)
    head = [('M', (84, -272)), ('C', (88, -296), (112, -300), (128, -288)), ('C', (144, -282), (156, -272), (162, -262)),
            ('C', (166, -254), (162, -247), (154, -247)), ('C', (132, -243), (102, -247), (90, -253)), ('C', (84, -259), (82, -265), (84, -272)), ('Z',)]
    d.path([('M', (106, -294)), ('C', (112, -322), (132, -330), (142, -321)), ('C', (136, -306), (124, -296), (106, -294)), ('Z',)], fill=shade)
    d.path(head, fill=coat, ident='deer-head')
    d.path([('M', (134, -276)), ('C', (148, -272), (160, -264), (162, -260)), ('C', (166, -252), (160, -246), (154, -247)), ('C', (140, -245), (130, -248), (126, -256)), ('Z',)], fill=light)
    d.path([('M', (92, -292)), ('C', (80, -316), (62, -320), (54, -307)), ('C', (62, -298), (78, -292), (92, -292)), ('Z',)], fill=coat)
    d.path([('M', (88, -296)), ('C', (80, -310), (68, -312), (62, -306)), ('C', (70, -300), (80, -296), (88, -296)), ('Z',)], fill='#8c6a4a', opacity=.8)
    d.ellipse(160, -258, 5.4, 4.2, fill='#3a2c24')
    d.ellipse(118, -276, 4.4, 5, fill='#2a1d18')
    d.circle(119.6, -278, 1.5, fill='#fff6e0')


# --- rabbit: sitting up, one paw raised to ask a question -------------------------------------

def rabbit(d):
    fur, shade, pink = '#f0e7d6', '#ddd0b8', '#e8b6a8'
    d.ellipse(-62, -46, 17, 16, fill='#fbf6ea', ident='rabbit-tail')
    d.ellipse(0, -72, 60, 72, fill=fur, ident='rabbit-body')
    d.ellipse(-20, -42, 44, 42, fill=shade)
    d.ellipse(44, -8, 38, 11, fill=fur)
    d.path([('M', (40, -104)), ('C', (48, -80), (54, -50), (52, -20)), ('L', (66, -20)), ('C', (68, -54), (60, -86), (54, -110)), ('Z',)], fill=fur)
    with d.group(transform='rotate(-10 40 -160)'):
        for ear, inner in (([('M', (22, -192)), ('C', (10, -252), (12, -292), (26, -300)), ('C', (42, -292), (46, -246), (46, -196)), ('Z',)],
                            [('M', (28, -200)), ('C', (20, -250), (22, -280), (28, -286)), ('C', (36, -278), (38, -246), (38, -202)), ('Z',)]),
                           ([('M', (52, -190)), ('C', (74, -244), (92, -272), (106, -268)), ('C', (108, -246), (86, -208), (68, -184)), ('Z',)],
                            [('M', (60, -196)), ('C', (76, -236), (88, -256), (98, -258)), ('C', (96, -242), (82, -214), (68, -194)), ('Z',)])):
            d.path(ear, fill=fur)
            d.path(inner, fill=pink, opacity=.85)
        d.ellipse(40, -172, 42, 36, fill=fur, ident='rabbit-head')
        d.ellipse(76, -163, 22, 16, fill='#f8f1e4')
        d.ellipse(92, -166, 5, 4, fill='#c98f84')
        d.ellipse(60, -178, 4.8, 5.6, fill='#2a1d18')
        d.circle(61.6, -180.2, 1.6, fill='#fff6e0')
        d.ellipse(58, -160, 9, 5.5, fill=pink, opacity=.6)
        d.path([('M', (80, -158)), ('C', (84, -153), (90, -152), (94, -155))], stroke='#b5a48a', width=1.6)
    # The raised paw sits in front of the face, as if asking to speak.
    d.path([('M', (40, -118)), ('C', (74, -122), (100, -140), (106, -176)), ('L', (92, -180)), ('C', (88, -154), (68, -140), (40, -136)), ('Z',)], fill=fur, ident='rabbit-raised-arm')
    d.ellipse(100, -186, 11, 15, fill=fur, ident='rabbit-raised-paw')
    d.path([('M', (97, -192)), ('L', (97, -182))], stroke=shade, width=1.4)
    d.path([('M', (103, -192)), ('L', (103, -182))], stroke=shade, width=1.4)


# --- squirrel: seated, tail raised, holding an acorn ---------------------------------------------

def squirrel(d):
    fur, deep, belly = '#b9703a', '#9a5a2c', '#ecd2a6'
    d.path([('M', (-26, -44)), ('C', (-122, -34), (-146, -164), (-84, -206)), ('C', (-52, -228), (-20, -198), (-34, -172))],
           stroke=fur, width=38, ident='squirrel-tail')
    d.path([('M', (-30, -48)), ('C', (-116, -38), (-136, -158), (-82, -198)), ('C', (-54, -216), (-30, -194), (-40, -174))], stroke='#e2a96c', width=14, opacity=.85)
    d.ellipse(0, -56, 35, 52, fill=fur, ident='squirrel-body')
    d.ellipse(16, -50, 19, 36, fill=belly)
    d.ellipse(-4, -7, 26, 9, fill=deep)
    d.ellipse(30, -126, 24, 22, fill=fur, ident='squirrel-head')
    d.path([('M', (14, -140)), ('L', (10, -162)), ('L', (28, -148)), ('Z',)], fill=fur)
    d.path([('M', (34, -146)), ('L', (42, -166)), ('L', (48, -140)), ('Z',)], fill=fur)
    d.ellipse(44, -118, 13, 9, fill=belly)
    d.ellipse(54, -119, 4, 3.4, fill='#3a2a22')
    d.ellipse(38, -130, 3.6, 4.2, fill='#2a1d18')
    d.circle(39.2, -131.5, 1.2, fill='#fff6e0')
    # Acorn held in both paws.
    d.ellipse(42, -78, 9, 12, fill='#a8743c')
    d.ellipse(42, -89, 11, 6, fill='#6a4a2a')
    d.ellipse(32, -84, 6.4, 5, fill=fur)
    d.ellipse(51, -80, 6.4, 5, fill=fur)


# --- hedgehog: side view, snout lifted ---------------------------------------------------------------

def hedgehog(d):
    quill, tip, skin = '#6a5642', '#9a8265', '#dac4a0'
    cx, cy, rx, ry = -4, -50, 80, 54
    spikes = []
    count = 40
    for i in range(count + 1):
        angle = math.radians(150 + 240 * i / count)
        spikes.append((cx + rx * 1.22 * math.cos(angle), cy + ry * 1.2 * math.sin(angle)))
        if i < count:
            mid = math.radians(150 + 240 * (i + .5) / count)
            spikes.append((cx + rx * .98 * math.cos(mid), cy + ry * .98 * math.sin(mid)))
    spikes = [(x, min(y, -6)) for x, y in spikes]
    d.polygon(spikes, fill=quill, ident='hedgehog-quills')
    inner = [(cx + rx * .8 * math.cos(math.radians(150 + 240 * i / 30)), cy + ry * .8 * math.sin(math.radians(150 + 240 * i / 30))) for i in range(31)]
    d.polygon(inner, fill=tip, opacity=.45)
    d.ellipse(-34, -7, 15, 7, fill='#8d7455')
    d.ellipse(40, -7, 15, 7, fill='#8d7455')
    d.path([('M', (26, -70)), ('C', (60, -68), (94, -46), (104, -28)), ('C', (106, -18), (98, -10), (86, -10)),
            ('C', (60, -8), (40, -8), (24, -14)), ('Z',)], fill=skin, ident='hedgehog-face')
    d.ellipse(104, -28, 6.4, 5.4, fill='#3a2c24')
    d.ellipse(76, -42, 4.8, 5.4, fill='#2a1d18')
    d.circle(77.6, -44, 1.6, fill='#fff6e0')
    d.ellipse(46, -66, 9, 11, fill='#c4a77e')
    d.path([('M', (84, -20)), ('C', (90, -16), (98, -16), (102, -20))], stroke='#9c8160', width=1.8)


# --- mouse: taking notes ---------------------------------------------------------------------------

def mouse(d):
    fur, belly, pink = '#b7a894', '#e0d3bd', '#dcaaa0'
    d.path([('M', (-26, -14)), ('C', (-70, -10), (-92, -40), (-76, -64))], stroke='#c9a79a', width=3.4, ident='mouse-tail')
    d.ellipse(0, -34, 33, 34, fill=fur, ident='mouse-body')
    d.ellipse(6, -26, 20, 24, fill=belly)
    d.ellipse(0, -5, 28, 7, fill='#9a8b78')
    d.path([('M', (10, -16)), ('C', (24, -2), (60, -6), (78, -20)), ('C', (60, -34), (30, -30), (10, -16)), ('Z',)], fill='#8fae62')
    d.path([('M', (14, -16)), ('C', (34, -16), (56, -22), (72, -20))], stroke='#c9d79a', width=1.4)
    d.ellipse(26, -62, 21, 18, fill=fur, ident='mouse-head')
    d.circle(14, -80, 13, fill=fur)
    d.circle(36, -82, 13, fill=fur)
    d.circle(14, -80, 7.5, fill=pink)
    d.circle(36, -82, 7.5, fill=pink)
    d.ellipse(46, -56, 12, 9, fill=belly)
    d.ellipse(57, -58, 3.6, 3, fill='#7d5a52')
    d.ellipse(36, -65, 3.4, 4, fill='#2a1d18')
    d.circle(37, -66.4, 1.1, fill='#fff6e0')
    # A paw guides the twig across the leaf page.
    d.line((40, -40), (70, -26), '#7a5c3d', 2.4)
    d.ellipse(38, -38, 8, 6.4, fill=fur)


# --- owl: front view on the stump, a leaf page held up ---------------------------------------------------

def owl(d):
    brown, dark, cream, face = '#8a6847', '#6b4e36', '#e3d2a8', '#ecdcb4'
    for dx in (-18, 18):
        d.path([('M', (dx - 9, -6)), ('L', (dx, 8)), ('L', (dx + 9, -6)), ('Z',)], fill='#c88f3a')
    d.ellipse(0, -82, 64, 84, fill=brown, ident='owl-body')
    for side in (-1, 1):
        d.path([('M', (side * 52, -120)), ('C', (side * 82, -90), (side * 80, -30), (side * 56, -8)),
                ('C', (side * 52, -40), (side * 46, -80), (side * 52, -120)), ('Z',)], fill=dark)
    d.ellipse(0, -70, 42, 62, fill=cream)
    for row in range(4):
        for col in range(3 - row % 2):
            cx = -22 + col * 22 + (11 if row % 2 else 0)
            y = -100 + row * 20
            d.path([('M', (cx - 9, y)), ('C', (cx - 5, y + 10), (cx + 5, y + 10), (cx + 9, y))], stroke='#b99d70', width=1.6)
    for side in (-1, 1):
        d.path([('M', (side * 52, -168)), ('L', (side * 44, -206)), ('L', (side * 20, -178)), ('Z',)], fill=brown)
    d.ellipse(0, -148, 58, 50, fill='#9b7a55', ident='owl-head')
    for dx in (-24, 24):
        d.circle(dx, -146, 26.5, fill=face)
        d.circle(dx, -144, 13.5, fill='#d99b2b')
        d.ellipse(dx + 1.5, -142, 7, 7.6, fill='#2a2a22')
        d.circle(dx + 3.6, -145, 2.4, fill='#fff3cc')
        d.path([('M', (dx - 16, -163)), ('C', (dx - 6, -170), (dx + 6, -170), (dx + 16, -163))], stroke=dark, width=2.2)
    d.path([('M', (-7, -138)), ('L', (0, -116)), ('L', (7, -138)), ('C', (3, -142), (-3, -142), (-7, -138)), ('Z',)], fill='#d08a2a')
    # A leaf page, held up by a raised wing.
    d.path([('M', (-34, -8)), ('C', (-40, -60), (-16, -108), (22, -120)), ('C', (30, -80), (6, -30), (-34, -8)), ('Z',)], fill='#86a65e', ident='owl-leaf')
    d.path([('M', (-30, -12)), ('C', (-14, -50), (4, -90), (18, -116))], stroke='#c9d79a', width=1.6)
    d.path([('M', (30, -112)), ('C', (58, -100), (62, -66), (36, -56)), ('C', (34, -76), (30, -96), (30, -112)), ('Z',)], fill=dark)
    d.ellipse(28, -70, 8, 6, fill='#caa36a')
