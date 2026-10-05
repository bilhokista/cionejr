"""A woodland meeting: an owl chairs from a stump while the others listen.

New composition. The animals come from cast.py and are placed as sprites; the owl, mouse, stump,
log and glade are drawn here.
"""
from functools import lru_cache
from pathlib import Path
import importlib.util
import math
import random
import sys
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).parent
_spec = importlib.util.spec_from_file_location('forest_cast', ROOT / 'cast.py')
fg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fg)

S, SIZE = fg.S, fg.SIZE
CANVAS = (SIZE[0] * S, SIZE[1] * S)
KEY = (255, 0, 255)
STUMP_X, STUMP_TOP = 500, 590

# name -> (draw function, anchor x, anchor y of the animal's feet, scale, mirrored)
CAST = {
    'deer': ('deer', 312, 796, .64, True),
    'squirrel': ('squirrel', 858, 738, .95, False),
    'fox': ('fox', 138, 1018, .64, False),
    'rabbit': ('rabbit', 760, 1010, .68, False),
    'hedgehog': ('hedgehog', 640, 1160, .85, True),
    'mouse': ('mouse', 330, 1150, 1.0, False),
}
BACK_TO_FRONT = ('deer', 'squirrel', 'fox', 'rabbit', 'hedgehog', 'mouse')


@lru_cache(maxsize=None)
def sprite(name):
    """Draw one animal on a key-coloured canvas and return it as an RGBA cut-out."""
    im = Image.new('RGB', CANVAS, KEY)
    (globals().get(CAST[name][0]) or getattr(fg, CAST[name][0]))(im)
    arr = np.asarray(im).copy()
    solid = ~np.all(arr == KEY, axis=2)
    # Spread edge colours outward so resampling does not bleed the key colour in.
    for _ in range(4):
        for shift, axis in ((1, 0), (-1, 0), (1, 1), (-1, 1)):
            neighbour = np.roll(arr, shift, axis)
            fill = ~solid & np.roll(solid, shift, axis)
            arr[fill] = neighbour[fill]
            solid = solid | fill
    alpha = Image.fromarray((~np.all(np.asarray(im) == KEY, axis=2) * 255).astype(np.uint8))
    cut = Image.fromarray(arr).convert('RGBA')
    cut.putalpha(alpha)
    return cut.crop(alpha.getbbox())


def place(base, name):
    """Paste a sprite with its feet at the cast anchor; return its alpha at page size."""
    _, ax, ay, scale, mirror = CAST[name]
    cut = sprite(name)
    if mirror:
        cut = ImageOps.mirror(cut)
    size = (round(cut.width * scale), round(cut.height * scale))
    cut = cut.resize(size, Image.Resampling.LANCZOS)
    x, y = round(ax * S - size[0] / 2), round(ay * S - size[1])
    base.paste(cut, (x, y), cut)
    page = Image.new('L', CANVAS)
    page.paste(cut.getchannel('A'), (x, y))
    return page


def glade(im):
    yy, xx = np.mgrid[0:CANVAS[1], 0:CANVAS[0]]
    x, y = xx / S, yy / S
    light = np.exp(-((x - 500) / 330) ** 2 - ((y - 420) / 430) ** 2)
    dark = np.array(fg.rgb('#4d786a'), dtype=np.float32)
    warm = np.array(fg.rgb('#dedfaa'), dtype=np.float32)
    im.paste(Image.fromarray((dark + light[:, :, None] * (warm - dark)).astype(np.uint8)))
    for i, (x0, w, lean) in enumerate([(130, 20, 18), (255, 16, -22), (350, 18, 20), (655, 19, -24), (752, 21, 26), (862, 22, -18)]):
        col = ['#9bb48f', '#a8bd94', '#92ae8b'][i % 3]
        fg.path(im, [('M', (x0 - w, 0)), ('L', (x0 + w, 0)), ('C', (x0 + lean + w, 280), (x0 + lean + w, 560), (x0 + lean + w, 800)),
                     ('L', (x0 + lean - w, 804)), ('C', (x0 + lean - w, 560), (x0 + lean - w, 290), (x0 - w, 0))], fill=col)
    fg.path(im, [('M', (0, 800)), ('C', (200, 690), (360, 700), (500, 740)), ('C', (650, 690), (820, 690), (1000, 790)),
                 ('L', (1000, 1250)), ('L', (0, 1250))], fill='#729478')
    fg.path(im, [('M', (0, 900)), ('C', (200, 830), (400, 810), (520, 826)), ('C', (700, 806), (860, 826), (1000, 900)),
                 ('L', (1000, 1250)), ('L', (0, 1250))], fill='#82a07a')
    ring = [('M', (60, 960)), ('C', (60, 830), (260, 770), (500, 770)), ('C', (740, 770), (940, 830), (940, 960)),
            ('C', (940, 1130), (740, 1250), (500, 1250)), ('C', (260, 1250), (60, 1130), (60, 960))]
    fg.path(im, ring, fill='#c9cc99')
    fg.path(im, [('M', (150, 965)), ('C', (150, 860), (320, 815), (500, 815)), ('C', (680, 815), (850, 860), (850, 965)),
                 ('C', (850, 1100), (690, 1190), (500, 1190)), ('C', (310, 1190), (150, 1100), (150, 965))], fill='#d9d8a6')


BRANCHES = [([('M', (60, 330)), ('C', (210, 280), (330, 170), (430, 96))], 30),
            ([('M', (940, 300)), ('C', (790, 240), (690, 150), (610, 70))], 30)]


def trunks(im):
    left = [('M', (-60, 0)), ('L', (170, 0)), ('C', (176, 220), (146, 420), (150, 650)), ('C', (156, 830), (186, 960), (190, 1060)),
            ('L', (-50, 1090)), ('L', (-60, 0))]
    right = [('M', (860, -10)), ('L', (1060, -10)), ('L', (1060, 1100)), ('L', (830, 1070)),
             ('C', (870, 950), (874, 800), (880, 560)), ('C', (884, 330), (872, 160), (860, -10))]
    fg.path(im, left, fill='#284f49')
    fg.path(im, right, fill='#31574c')
    fg.path(im, [('M', (70, 0)), ('C', (82, 260), (84, 720), (118, 1040)), ('L', (146, 1070)), ('C', (108, 740), (116, 420), (130, 0))], fill='#3d6657')
    fg.path(im, [('M', (920, 0)), ('C', (940, 360), (910, 640), (930, 1010)), ('L', (958, 1070)), ('C', (938, 740), (958, 400), (956, 0))], fill='#456950')


def canopy(im):
    for branch, width in BRANCHES:
        fg.path(im, branch, stroke='#31584c', width=width)
    fg.path(im, [('M', (0, 0)), ('L', (1000, 0)), ('L', (1000, 215)),
                 ('C', (940, 200), (930, 150), (880, 160)), ('C', (820, 150), (810, 100), (760, 118)),
                 ('C', (700, 135), (690, 60), (640, 82)), ('C', (580, 100), (570, 34), (520, 58)),
                 ('C', (470, 86), (440, 24), (390, 66)), ('C', (340, 108), (310, 76), (268, 122)),
                 ('C', (222, 172), (170, 120), (130, 196)), ('C', (96, 246), (40, 214), (0, 280)), ('L', (0, 0))], fill='#254f47')
    for index, t, tip, count, colour, seed, kind in [(0, .2, (300, 190), 7, '#4c775a', 21, 'frond'), (0, .6, (390, 40), 5, '#66865d', 22, 'broad'),
                                                   (1, .25, (700, 170), 6, '#527c59', 23, 'frond'), (1, .65, (570, 44), 5, '#809460', 24, 'broad'),
                                                   (0, .08, (110, 420), 5, '#7fa378', 25, 'broad')]:
        fg.sprig(im, fg.on_branch(BRANCHES[index][0], t), tip, count, colour, '#91ae76', seed, 12, kind)


def stump(im):
    x = STUMP_X
    fg.ellipse(im, x, 786, 120, 16, '#a4ad80')
    fg.path(im, [('M', (x - 88, STUMP_TOP)), ('C', (x - 84, 650), (x - 96, 720), (x - 100, 780)), ('C', (x - 50, 796), (x + 52, 796), (x + 100, 780)),
                 ('C', (x + 96, 720), (x + 84, 650), (x + 88, STUMP_TOP)), ('L', (x - 88, STUMP_TOP))], fill='#9a7752')
    fg.path(im, [('M', (x - 60, 610)), ('C', (x - 62, 680), (x - 68, 740), (x - 66, 790)), ('L', (x - 20, 794)),
                 ('C', (x - 28, 740), (x - 22, 670), (x - 24, 610)), ('L', (x - 60, 610))], fill='#ab8858')
    for gx, y0, y1 in [(x - 76, 640, 770), (x - 38, 650, 780), (x + 10, 640, 786), (x + 44, 650, 780), (x + 78, 640, 760)]:
        fg.path(im, [('M', (gx, y0)), ('C', (gx + 4, y0 + 40), (gx - 3, y1 - 40), (gx, y1))], stroke='#7d6549', width=2)
    fg.ellipse(im, x, STUMP_TOP, 88, 24, '#dfc59b')
    for rx, ry in [(66, 17), (42, 11), (20, 5)]:
        fg.ellipse(im, x, STUMP_TOP, rx, ry, None, '#b5966d', 1.1)
    fg.path(im, [('M', (x - 88, 600)), ('C', (x - 80, 628), (x - 66, 614), (x - 56, 636)), ('C', (x - 70, 650), (x - 84, 646), (x - 90, 640)), ('C', (x - 92, 622), (x - 90, 610), (x - 88, 600))], fill='#7f9a58')


def log(im):
    fg.ellipse(im, 800, 764, 150, 12, '#a4ad80')
    fg.path(im, [('M', (660, 712)), ('C', (700, 700), (900, 704), (950, 716)), ('L', (948, 760)), ('C', (900, 772), (700, 772), (656, 758)), ('L', (660, 712))], fill='#8d6b49')
    fg.path(im, [('M', (664, 716)), ('C', (720, 706), (880, 708), (944, 720)), ('L', (944, 732)), ('C', (880, 722), (720, 720), (664, 730))], fill='#a07c56')
    fg.ellipse(im, 662, 735, 20, 26, '#d8bb8c')
    fg.ellipse(im, 662, 735, 12, 17, None, '#b0936a', 1.2)
    for x0 in (720, 790, 860):
        fg.path(im, [('M', (x0, 740)), ('C', (x0 + 12, 748), (x0 + 30, 746), (x0 + 42, 752))], stroke='#6e553c', width=1.6)


def owl(im):
    """Front view, perched at the stump's centre, a leaf held like a page."""
    x, top = STUMP_X, STUMP_TOP
    brown, dark, cream = '#8a6847', '#6b4e36', '#e3d2a8'
    fg.ellipse(im, x, top - 4, 50, 8, '#b9a074')
    for dx in (-18, 18):
        fg.path(im, [('M', (x + dx - 8, top - 6)), ('L', (x + dx, top + 6)), ('L', (x + dx + 8, top - 6))], fill='#c88f3a')
    fg.ellipse(im, x, top - 82, 64, 84, brown)
    for side in (-1, 1):
        fg.path(im, [('M', (x + side * 52, top - 120)), ('C', (x + side * 82, top - 90), (x + side * 80, top - 30), (x + side * 56, top - 8)),
                     ('C', (x + side * 52, top - 40), (x + side * 46, top - 80), (x + side * 52, top - 120))], fill=dark)
    fg.ellipse(im, x, top - 70, 42, 62, cream)
    for row in range(4):
        for col in range(3 - row % 2):
            cx = x - 22 + col * 22 + (11 if row % 2 else 0)
            fg.path(im, [('M', (cx - 9, top - 100 + row * 20)), ('C', (cx - 5, top - 90 + row * 20), (cx + 5, top - 90 + row * 20), (cx + 9, top - 100 + row * 20))],
                    stroke='#b99d70', width=1.6)
    # Head, with ear tufts and a pale facial disc.
    fg.path(im, [('M', (x - 52, top - 168)), ('L', (x - 44, top - 206)), ('L', (x - 20, top - 178))], fill=brown)
    fg.path(im, [('M', (x + 52, top - 168)), ('L', (x + 44, top - 206)), ('L', (x + 20, top - 178))], fill=brown)
    fg.ellipse(im, x, top - 148, 58, 50, '#9b7a55')
    for dx in (-24, 24):
        fg.ellipse(im, x + dx, top - 146, 26, 27, '#ecdcb4')
        fg.ellipse(im, x + dx, top - 144, 13.5, 13.5, '#d99b2b')
        fg.ellipse(im, x + dx + 1.5, top - 142, 7, 7.5, '#2a2a22')
        fg.ellipse(im, x + dx + 3.5, top - 145, 2.4, 2.4, '#fff3cc')
        fg.path(im, [('M', (x + dx - 16, top - 163)), ('C', (x + dx - 6, top - 170), (x + dx + 6, top - 170), (x + dx + 16, top - 163))], stroke='#6b4e36', width=2.2)
    fg.path(im, [('M', (x - 7, top - 138)), ('L', (x, top - 116)), ('L', (x + 7, top - 138)), ('C', (x + 3, top - 142), (x - 3, top - 142), (x - 7, top - 138))], fill='#d08a2a')
    # The leaf page is held by one raised wing; a second wing rests along the body.
    fg.leaf(im, (x - 34, top - 6), (x + 18, top - 118), 44, '#86a65e', '#c9d79a')
    fg.path(im, [('M', (x + 30, top - 112)), ('C', (x + 58, top - 100), (x + 62, top - 66), (x + 36, top - 56)), ('C', (x + 34, top - 76), (x + 30, top - 96), (x + 30, top - 112))], fill=dark)
    fg.ellipse(im, x + 28, top - 70, 8, 6, '#caa36a')


def mouse(im, k=1.45):
    """Front-left, taking notes on a leaf with a twig. Drawn at its final size, not upscaled."""
    x, y = 365, 1126
    pt = lambda dx, dy: (x + dx * k, y + dy * k)
    el = lambda dx, dy, rx, ry, col, **kw: fg.ellipse(im, x + dx * k, y + dy * k, rx * k, ry * k, col, **kw)
    el(0, 16, 52, 8, '#a8af82')
    fg.path(im, [('M', pt(-30, 6)), ('C', pt(-66, 8), pt(-84, -18), pt(-70, -34))], stroke='#c9a79a', width=3 * k)
    el(0, -2, 34, 28, '#b8a995')
    el(6, 4, 20, 18, '#e0d3bd')
    fg.leaf(im, pt(4, 22), pt(60, -6), 20 * k, '#8fae62', '#c9d79a')
    el(36, -22, 20, 17, '#bfb09b')
    for dx in (-8, 12):
        el(28 + dx, -40, 9, 10, '#bfb09b')
        el(28 + dx, -40, 5, 6, '#dcaaa0')
    fg.eye(im, *pt(44, -25), 3 * k, gaze=(1.2, -1.4))
    el(55, -19, 3, 2.4, '#7d5a52')
    fg.line(im, [pt(22, 6), pt(44, 4)], '#b8a995', 7 * k)
    fg.line(im, [pt(40, -2), pt(58, 6)], '#7a5c3d', 2.2 * k)


def stage(placed):
    """Back-to-front composition: glade, stump and log, audience, owl, foreground."""
    im = Image.new('RGB', CANVAS)
    glade(im)
    trunks(im)
    stump(im)
    log(im)
    for name in BACK_TO_FRONT[:-1]:
        placed[name] = place(im, name)
    owl(im)
    placed['mouse'] = place(im, 'mouse')
    return im


def occupied(placed, margin=10):
    page = Image.new('L', SIZE)
    for alpha in placed.values():
        page = ImageChops.lighter(page, alpha.resize(SIZE, Image.Resampling.BILINEAR).point(lambda v: 255 if v > 40 else 0))
    d = ImageDraw.Draw(page)
    for box in [(STUMP_X - 100, 560, STUMP_X + 100, 800), (STUMP_X - 70, 380, STUMP_X + 80, 600), (650, 700, 960, 775)]:
        d.rectangle(box, fill=255)
    return page.filter(ImageFilter.MaxFilter(margin * 2 + 1))


def floor_detail(im, protect):
    rng = random.Random(31)
    for _ in range(150):
        x, y = rng.uniform(120, 880), rng.uniform(790, 1230)
        if protect.getpixel((int(x), int(y))):
            continue
        col = rng.choice(['#7f9465', '#9caa74', '#a6b27d'])
        for j in (-1, 0, 1):
            fg.line(im, [(x, y), (x + j * 5, y - rng.uniform(6, 14))], col, 1.1)
    for x, y, r, col in [(120, 1090, 20, '#b07755'), (150, 1112, 13, '#c39365'), (880, 1060, 18, '#b47554'), (906, 1080, 12, '#c39667')]:
        fg.mushroom(im, x, y, r, col)
    fg.path(im, [('M', (0, 1100)), ('C', (70, 1040), (150, 1100), (160, 1160)), ('C', (250, 1130), (270, 1210), (320, 1250)), ('L', (0, 1250))], fill='#234c42')
    fg.path(im, [('M', (1000, 1090)), ('C', (940, 1060), (890, 1100), (900, 1160)), ('C', (830, 1130), (800, 1210), (750, 1250)), ('L', (1000, 1250))], fill='#244e43')
    for b, t, n, col, seed, width, kind in [((6, 1240), (170, 1110), 6, '#557c55', 1, 14, 'frond'), ((990, 1236), (820, 1100), 6, '#5b8055', 3, 13, 'broad')]:
        fg.sprig(im, b, t, n, col, '#93a66b', seed, width, kind)
    for root, tip, width, color in [((0, 1180), (80, 1070), 36, '#486f4f'), ((1000, 1150), (952, 1052), 30, '#4f7550')]:
        fg.leaf(im, root, tip, width, color, '#8ca067')


def scene(with_detail=True):
    placed = {}
    im = stage(placed)
    if with_detail:
        canopy(im)
        floor_detail(im, occupied(placed))
        fg.pigment(im)
    return im, placed


def layout():
    """Grey masses only: used to judge placement, gaze and overlap before any material."""
    im = Image.new('RGB', CANVAS, (176, 182, 170))
    stump(im)
    log(im)
    shade = {'deer': 150, 'squirrel': 130, 'fox': 110, 'rabbit': 205, 'hedgehog': 95, 'mouse': 120}
    for name in BACK_TO_FRONT[:-1]:
        alpha = place(Image.new('RGB', CANVAS), name)
        im.paste(Image.new('RGB', CANVAS, (shade[name],) * 3), (0, 0), alpha)
    owl(im)
    alpha = place(Image.new('RGB', CANVAS), 'mouse')
    im.paste(Image.new('RGB', CANVAS, (shade['mouse'],) * 3), (0, 0), alpha)
    im.resize(SIZE, Image.Resampling.LANCZOS).save(ROOT / 'composition.png')
    print('Saved composition.png')


if __name__ == '__main__':
    if '--layout' in sys.argv:
        layout()
    else:
        image, _ = scene()
        image = image.resize((2400, 3000), Image.Resampling.LANCZOS)
        image.save(ROOT / 'forest-meeting.png', dpi=(300, 300))
        image.resize((600, 750), Image.Resampling.LANCZOS).save(ROOT / 'preview.png')
        print('Saved forest-meeting.png and preview.png')
