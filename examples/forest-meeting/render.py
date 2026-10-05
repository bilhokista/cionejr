"""A woodland meeting: an owl chairs from a stump while the others listen.

The scene is written as SVG; the PNGs are rendered from it. `composition.png` is the
same scene in greys, which is how placement, gaze and overlap are judged before
any colour decisions.
"""
from pathlib import Path
import importlib.util
import io
import math
import random
from PIL import Image

ROOT = Path(__file__).parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kit = load('svgkit', ROOT.parent / 'svgkit.py')
chars = load('meeting_characters', ROOT / 'characters.py')

W, H = 1000, 1250
STUMP = (500, 590)  # centre of the stump top; the owl stands here
FINAL = (2400, 3000)

# name -> (draw function, x and y of the feet, scale, mirrored so it faces the owl)
CAST = {
    'deer': (chars.deer, 236, 800, .74, False),
    'squirrel': (chars.squirrel, 850, 722, .8, True),
    'fox': (chars.fox, 212, 1024, .82, False),
    'rabbit': (chars.rabbit, 790, 1012, .82, True),
    'hedgehog': (chars.hedgehog, 640, 1172, 1.0, True),
    'mouse': (chars.mouse, 336, 1164, 1.4, False),
}
BACK_TO_FRONT = ('deer', 'squirrel', 'fox', 'rabbit', 'hedgehog', 'mouse')


# --- foliage ---------------------------------------------------------------------------

def on_branch(branch, t):
    (_, start), (_, a, b, end) = branch
    return tuple((1 - t) ** 3 * start[j] + 3 * (1 - t) ** 2 * t * a[j] + 3 * (1 - t) * t * t * b[j] + t ** 3 * end[j] for j in (0, 1))


def jitter(colour, rng, amount=9):
    value = colour.lstrip('#')
    channels = [int(value[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(max(0, min(255, c + rng.randint(-amount, amount))) for c in channels)


def leaf(d, root, tip, width, colour, vein=None):
    dx, dy = tip[0] - root[0], tip[1] - root[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    shape = [('M', root),
             ('C', (root[0] + dx * .18 + nx * width, root[1] + dy * .18 + ny * width),
              (root[0] + dx * .7 + nx * width * .5, root[1] + dy * .7 + ny * width * .5), tip),
             ('C', (root[0] + dx * .7 - nx * width * .55, root[1] + dy * .7 - ny * width * .55),
              (root[0] + dx * .17 - nx * width * .65, root[1] + dy * .17 - ny * width * .65), root), ('Z',)]
    d.path(shape, fill=colour)
    if vein:
        d.line(root, (root[0] + dx * .83, root[1] + dy * .83), vein, .8)


def sprig(d, base, tip, count, colour, stem, seed=0, leaf_width=10, kind='frond'):
    rng = random.Random(seed)
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    d.path([('M', base), ('C', (base[0] + dx * .3, base[1] + dy * .3), (base[0] + dx * .75, base[1] + dy * .75), tip)],
           stroke=stem, width=1.4)
    for i in range(1, count + 1):
        t = i / (count + 1)
        root = (base[0] + dx * t, base[1] + dy * t)
        if kind == 'broad':
            side = 1 if i % 2 else -1
            reach = rng.uniform(26, 40) * (1 - t * .3)
            end = (root[0] + nx * reach * side + dx * .2, root[1] + ny * reach * side + dy * .2)
            leaf(d, root, end, leaf_width * rng.uniform(1.25, 1.7), jitter(colour, rng), stem)
            continue
        for side in (-1, 1):
            reach = rng.uniform(21, 42) * (1 - t * .4)
            end = (root[0] + nx * reach * side + dx * .11, root[1] + ny * reach * side + dy * .11)
            leaf(d, root, end, leaf_width * rng.uniform(.65, 1.15), jitter(colour, rng, 6), stem)
    leaf(d, (base[0] + dx * .85, base[1] + dy * .85), tip, leaf_width * (1.1 if kind == 'broad' else .65), colour)


# --- the glade -------------------------------------------------------------------------------

BRANCHES = [([('M', (60, 330)), ('C', (210, 280), (330, 170), (430, 96))], 30),
            ([('M', (940, 300)), ('C', (790, 240), (690, 150), (610, 70))], 30)]


def backdrop(d):
    d.rect(0, 0, W, H, fill='#4d786a')
    glow = d.radial_gradient([(0, '#e6e6b2', 1), (.55, '#cfd7a2', .55), (1, '#cfd7a2', 0)], cx=.5, cy=.34, r=.62)
    d.rect(0, 0, W, H, fill=glow)
    with d.group(ident='distant-trunks'):
        for i, (x0, w, lean) in enumerate([(130, 20, 18), (255, 16, -22), (350, 18, 20), (655, 19, -24), (752, 21, 26), (862, 22, -18)]):
            colour = ['#9bb48f', '#a8bd94', '#92ae8b'][i % 3]
            d.path([('M', (x0 - w, 0)), ('L', (x0 + w, 0)), ('C', (x0 + lean + w, 280), (x0 + lean + w, 560), (x0 + lean + w, 800)),
                    ('L', (x0 + lean - w, 804)), ('C', (x0 + lean - w, 560), (x0 + lean - w, 290), (x0 - w, 0)), ('Z',)], fill=colour)
    with d.group(ident='ground'):
        d.path([('M', (0, 800)), ('C', (200, 690), (360, 700), (500, 740)), ('C', (650, 690), (820, 690), (1000, 790)),
                ('L', (1000, 1250)), ('L', (0, 1250)), ('Z',)], fill='#729478')
        d.path([('M', (0, 900)), ('C', (200, 830), (400, 810), (520, 826)), ('C', (700, 806), (860, 826), (1000, 900)),
                ('L', (1000, 1250)), ('L', (0, 1250)), ('Z',)], fill='#82a07a')
        d.path([('M', (60, 960)), ('C', (60, 830), (260, 770), (500, 770)), ('C', (740, 770), (940, 830), (940, 960)),
                ('C', (940, 1130), (740, 1250), (500, 1250)), ('C', (260, 1250), (60, 1130), (60, 960)), ('Z',)], fill='#c9cc99', ident='clearing')
        d.path([('M', (150, 965)), ('C', (150, 860), (320, 815), (500, 815)), ('C', (680, 815), (850, 860), (850, 965)),
                ('C', (850, 1100), (690, 1190), (500, 1190)), ('C', (310, 1190), (150, 1100), (150, 965)), ('Z',)], fill='#d9d8a6')


def trunks(d):
    with d.group(ident='trunks'):
        d.path([('M', (-60, 0)), ('L', (170, 0)), ('C', (176, 220), (146, 420), (150, 650)), ('C', (156, 830), (186, 960), (190, 1060)),
                ('L', (-50, 1090)), ('Z',)], fill='#284f49')
        d.path([('M', (860, -10)), ('L', (1060, -10)), ('L', (1060, 1100)), ('L', (830, 1070)), ('C', (870, 950), (874, 800), (880, 560)),
                ('C', (884, 330), (872, 160), (860, -10)), ('Z',)], fill='#31574c')
        d.path([('M', (70, 0)), ('C', (82, 260), (84, 720), (118, 1040)), ('L', (146, 1070)), ('C', (108, 740), (116, 420), (130, 0)), ('Z',)], fill='#3d6657')
        d.path([('M', (920, 0)), ('C', (940, 360), (910, 640), (930, 1010)), ('L', (958, 1070)), ('C', (938, 740), (958, 400), (956, 0)), ('Z',)], fill='#456950')


def stump(d):
    x, top = STUMP
    with d.group(ident='stump'):
        d.ellipse(x, 786, 120, 16, fill='#a4ad80')
        d.path([('M', (x - 88, top)), ('C', (x - 84, 650), (x - 96, 720), (x - 100, 780)), ('C', (x - 50, 796), (x + 52, 796), (x + 100, 780)),
                ('C', (x + 96, 720), (x + 84, 650), (x + 88, top)), ('Z',)], fill='#9a7752')
        d.path([('M', (x - 60, 610)), ('C', (x - 62, 680), (x - 68, 740), (x - 66, 790)), ('L', (x - 20, 794)),
                ('C', (x - 28, 740), (x - 22, 670), (x - 24, 610)), ('Z',)], fill='#ab8858')
        for gx, y0, y1 in [(x - 76, 640, 770), (x - 38, 650, 780), (x + 10, 640, 786), (x + 44, 650, 780), (x + 78, 640, 760)]:
            d.path([('M', (gx, y0)), ('C', (gx + 4, y0 + 40), (gx - 3, y1 - 40), (gx, y1))], stroke='#7d6549', width=2)
        d.ellipse(x, top, 88, 24, fill='#dfc59b')
        for rx, ry in [(66, 17), (42, 11), (20, 5)]:
            d.ellipse(x, top, rx, ry, stroke='#b5966d', width=1.1)
        d.path([('M', (x - 88, 600)), ('C', (x - 80, 628), (x - 66, 614), (x - 56, 636)), ('C', (x - 70, 650), (x - 84, 646), (x - 90, 640)),
                ('C', (x - 92, 622), (x - 90, 610), (x - 88, 600)), ('Z',)], fill='#7f9a58')


def log(d):
    with d.group(ident='log'):
        d.ellipse(800, 764, 150, 12, fill='#a4ad80')
        d.path([('M', (660, 712)), ('C', (700, 700), (900, 704), (950, 716)), ('L', (948, 760)), ('C', (900, 772), (700, 772), (656, 758)), ('Z',)], fill='#8d6b49')
        d.path([('M', (664, 716)), ('C', (720, 706), (880, 708), (944, 720)), ('L', (944, 732)), ('C', (880, 722), (720, 720), (664, 730)), ('Z',)], fill='#a07c56')
        d.ellipse(662, 735, 20, 26, fill='#d8bb8c')
        d.ellipse(662, 735, 12, 17, stroke='#b0936a', width=1.2)
        for x0 in (720, 790, 860):
            d.path([('M', (x0, 740)), ('C', (x0 + 12, 748), (x0 + 30, 746), (x0 + 42, 752))], stroke='#6e553c', width=1.6)


def canopy(d):
    with d.group(ident='canopy'):
        for branch, width in BRANCHES:
            d.path(branch, stroke='#31584c', width=width, cap='butt')
        d.path([('M', (0, 0)), ('L', (1000, 0)), ('L', (1000, 215)), ('C', (940, 200), (930, 150), (880, 160)), ('C', (820, 150), (810, 100), (760, 118)),
                ('C', (700, 135), (690, 60), (640, 82)), ('C', (580, 100), (570, 34), (520, 58)), ('C', (470, 86), (440, 24), (390, 66)),
                ('C', (340, 108), (310, 76), (268, 122)), ('C', (222, 172), (170, 120), (130, 196)), ('C', (96, 246), (40, 214), (0, 280)), ('Z',)],
               fill='#254f47')
        for index, t, tip, count, colour, seed, kind in [(0, .2, (300, 190), 7, '#4c775a', 21, 'frond'), (0, .6, (390, 40), 5, '#66865d', 22, 'broad'),
                                                       (1, .25, (700, 170), 6, '#527c59', 23, 'frond'), (1, .65, (570, 44), 5, '#809460', 24, 'broad'),
                                                       (0, .08, (110, 420), 5, '#7fa378', 25, 'broad')]:
            sprig(d, on_branch(BRANCHES[index][0], t), tip, count, colour, '#91ae76', seed, 12, kind)


def mushroom(d, x, y, r, colour):
    d.path([('M', (x - r * .15, y - r * .15)), ('L', (x - r * .19, y + r * .9)), ('C', (x - r * .05, y + r), (x + r * .19, y + r), (x + r * .22, y + r * .82)),
            ('L', (x + r * .15, y - r * .15)), ('Z',)], fill='#dfd2a8')
    d.path([('M', (x - r, y)), ('C', (x - r, y - r * .75), (x - r * .32, y - r), (x, y - r * .8)), ('C', (x + r * .58, y - r * .9), (x + r * .91, y - r * .5), (x + r, y)),
            ('C', (x + r * .45, y + r * .14), (x - r * .44, y + r * .12), (x - r, y)), ('Z',)], fill=colour)
    d.ellipse(x - r * .34, y - r * .45, r * .14, r * .08, fill='#e8d5ab')
    d.ellipse(x + r * .26, y - r * .49, r * .11, r * .07, fill='#e8d5ab')


def keep_clear(x, y):
    """Boxes around the cast and the stump where no grass is drawn."""
    for _, cx, cy, scale, _ in CAST.values():
        half, height = 150 * scale, 330 * scale
        if cx - half <= x <= cx + half and cy - height <= y <= cy + 12:
            return True
    return 380 <= x <= 620 and 380 <= y <= 800


def foreground(d):
    rng = random.Random(31)
    with d.group(ident='grass'):
        placed = 0
        while placed < 120:
            x, y = rng.uniform(120, 880), rng.uniform(790, 1230)
            if keep_clear(x, y):
                continue
            colour = rng.choice(['#7f9465', '#9caa74', '#a6b27d'])
            for j in (-1, 0, 1):
                d.line((x, y), (x + j * 5, y - rng.uniform(6, 14)), colour, 1.1)
            placed += 1
    with d.group(ident='mushrooms'):
        for x, y, r, colour in [(120, 1090, 20, '#b07755'), (150, 1112, 13, '#c39365'), (880, 1060, 18, '#b47554'), (906, 1080, 12, '#c39667')]:
            mushroom(d, x, y, r, colour)
    with d.group(ident='foreground-leaves'):
        d.path([('M', (0, 1100)), ('C', (70, 1040), (150, 1100), (160, 1160)), ('C', (250, 1130), (270, 1210), (320, 1250)), ('L', (0, 1250)), ('Z',)], fill='#234c42')
        d.path([('M', (1000, 1090)), ('C', (940, 1060), (890, 1100), (900, 1160)), ('C', (830, 1130), (800, 1210), (750, 1250)), ('L', (1000, 1250)), ('Z',)], fill='#244e43')
        for start, tip, count, colour, seed, width, kind in [((6, 1240), (170, 1110), 6, '#557c55', 1, 14, 'frond'), ((990, 1236), (820, 1100), 6, '#5b8055', 3, 13, 'broad')]:
            sprig(d, start, tip, count, colour, '#93a66b', seed, width, kind)
        for root, tip, width, colour in [((0, 1180), (80, 1070), 36, '#486f4f'), ((1000, 1150), (952, 1052), 30, '#4f7550')]:
            leaf(d, root, tip, width, colour, '#8ca067')


# --- assembly -----------------------------------------------------------------------------------

def scene(greyscale=False, only=None, with_background=True):
    """Build the drawing. `only` limits it to named characters (used to measure each one alone)."""
    d = kit.Drawing(W, H, title='Woodland meeting',
                    description='An owl chairs a meeting from a stump while a fox, deer, rabbit, squirrel, hedgehog and mouse listen.')
    d.greyscale = greyscale
    if with_background:
        backdrop(d)
        trunks(d)
        stump(d)
        log(d)
    names = BACK_TO_FRONT if only is None else [n for n in BACK_TO_FRONT if n in only]
    with d.group(ident='audience'):
        for name in names:
            draw, x, y, scale, flip = CAST[name]
            chars.place(d, draw, name, x, y, scale, flip)
    if only is None or 'owl' in only:
        chars.place(d, chars.owl, 'owl', STUMP[0], STUMP[1] - 4, 1.0)
    if with_background:
        foreground(d)
        canopy(d)
    return d


def to_png(drawing, size):
    data = kit.render_png(drawing.to_svg(), *size)
    return Image.open(io.BytesIO(data)).convert('RGB')


def main():
    full = scene()
    full.save(ROOT / 'forest-meeting.svg')
    image = to_png(full, FINAL)
    image.save(ROOT / 'forest-meeting.png', dpi=(300, 300))
    image.resize((600, 750), Image.Resampling.LANCZOS).save(ROOT / 'preview.png')
    to_png(scene(greyscale=True), (1000, 1250)).save(ROOT / 'composition.png')
    print('Saved forest-meeting.svg, forest-meeting.png, preview.png and composition.png')


if __name__ == '__main__':
    main()
