"""Seven bird treatments written as SVG, built on the construction in render.py.

Each function returns a Drawing. The SVG is the master file; render.py rasterizes
it to PNG. The gouache study stays raster-only because its character is brush
texture, which does not survive as clean vector shapes.
"""
from pathlib import Path
import importlib.util
import math
import random
import numpy as np
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load('bird_base', ROOT / 'render.py')
kit = _load('svgkit', ROOT.parent / 'svgkit.py')

W, H, PAPER = base.W, base.H, base.PAPER
BEAK_TOP = [('M', (733, 201)), ('L', (800, 236)), ('L', (741, 239)), ('Z',)]
BEAK_LOW = [('M', (741, 239)), ('L', (800, 236)), ('L', (741, 250)), ('Z',)]
EYE = (697, 220)


def canvas(title, description, background=PAPER):
    return kit.Drawing(W, H, background=background, title=title, description=description)


def supports(d, ink, branch, leg_width=4, toe_width=3):
    d.path(base.BRANCH, fill=branch, ident='branch')
    for i, leg in enumerate(base.LEGS):
        d.path(leg, stroke=ink, width=leg_width, ident=f'leg-{i + 1}')
    for toe in base.TOES:
        d.path(toe, stroke=ink, width=toe_width)


# --- geometric ------------------------------------------------------------------

def geometric():
    d = canvas('Geometric bird', 'A perched sparrow built from flat colour planes.')
    supports(d, '#725947', '#a4aa8c')
    with d.group(ident='bird'):
        for name, commands, fill in [('body', base.BODY, '#ddd2b4'), ('belly-shade', base.BELLY_SHADOW, '#b7b89b'),
                                     ('tail', base.TAIL, '#5b6658'), ('back', base.BACK, '#bc774d'),
                                     ('wing', base.WING, '#745c45'), ('flight-1', base.FLIGHTS[0], '#c69a65'),
                                     ('flight-2', base.FLIGHTS[1], '#3e554b'), ('flight-3', base.FLIGHTS[2], '#a67c51'),
                                     ('scapular', base.SCAPULAR, '#c58955')]:
            d.path(commands, fill=fill, ident=name)
        d.path([('M', (444, 355)), ('C', (465, 365), (494, 364), (512, 351))], stroke='#f2e5c4', width=6)
        d.path([('M', (458, 384)), ('C', (476, 381), (495, 371), (510, 363))], stroke='#e8d8b6', width=3.5)
        dark = '#2e433b'
        for name, commands, fill in [('crown', base.CROWN, '#a56140'), ('cheek', base.CHEEK, '#f3e9ce'),
                                     ('mask', base.MASK, dark), ('ear-patch', base.EAR, dark), ('bib', base.BIB, dark),
                                     ('beak-upper', BEAK_TOP, dark), ('beak-lower', BEAK_LOW, dark)]:
            d.path(commands, fill=fill, ident=name)
        d.circle(*EYE, 8.5, fill='#f3e9ce')
        d.circle(*EYE, 7, fill=dark)
        d.circle(699.5, 217, 2.1, fill='#fff8dd')
    return d


# --- linocut ----------------------------------------------------------------------

def linocut():
    paper, ink = PAPER, '#4e392f'
    d = canvas('Linocut-style bird', 'A one-ink perched sparrow with carved paper-white cuts.')
    supports(d, ink, ink)
    body_clip, wing_clip, crown_clip = d.clip_path(base.BODY), d.clip_path(base.WING), d.clip_path(base.CROWN)
    d.path(base.BODY, fill=ink, ident='body')
    d.path(base.CHEEK, fill=paper, ident='cheek')
    d.path(base.EAR, fill=ink)
    with d.group(clip=body_clip, ident='flank-cuts'):
        for i in range(26):
            t = i / 25
            sx, sy, ex, ey = 397 + 208 * t, 429 - 37 * t, 442 + 214 * t, 517 - 30 * t
            d.path([('M', (sx, sy)), ('C', (sx + 3, sy + 29), (ex - 17, ey - 12), (ex, ey))], stroke=paper,
                   width=1.3 + (.55 if i % 4 == 0 else 0))
        for i in range(10):
            d.path([('M', (644 + i * 6, 331 + i * 2)), ('C', (650 + i * 6, 357 + i * 3), (644 + i * 6, 385 + i * 3),
                                                       (632 + i * 6, 411 + i * 3))], stroke=paper, width=1.3)
    d.path(base.WING, fill=ink, ident='wing')
    d.path(base.WING, stroke=paper, width=2.2)
    with d.group(clip=wing_clip, ident='wing-cuts'):
        for i in range(9):
            sx, sy, ex, ey = 350 + i * 16, 449 - i * 2.4, 512 + i * 5, 336 + i * 5
            d.path([('M', (sx, sy)), ('C', (sx + 59, sy - 21), (ex - 36, ey + 48), (ex, ey))], stroke=paper,
                   width=1.8 if i % 3 else 2.6)
        for x, y, dx, dy in [(433, 350, 35, -28), (459, 337, 28, -25), (486, 323, 22, -15), (516, 310, 20, -11)]:
            d.path([('M', (x, y)), ('C', (x + 7, y - 6), (x + dx - 8, y + dy - 3), (x + dx, y + dy))], stroke=paper, width=2.5)
        d.path([('M', (427, 366)), ('C', (452, 379), (480, 371), (503, 353))], stroke=paper, width=5)
        d.path([('M', (443, 390)), ('C', (463, 389), (491, 374), (511, 363))], stroke=paper, width=3.2)
    with d.group(clip=crown_clip, ident='crown-cuts'):
        for i in range(17):
            x = 571 + i * 7.3
            d.path([('M', (x, 239 - i * .7)), ('C', (x + 1, 213 - i * .6), (x + 14, 185 - i * .2), (x + 36, 172 + i * .65))],
                   stroke=paper, width=1.45)
    for i in range(5):
        d.path([('M', (148 + i * 4, 574 - i * 3)), ('C', (214, 536 - i * 3), (277, 502 - i * 4), (342, 468 - i * 4))],
               stroke=paper, width=1.4)
    d.path([('M', (571, 270)), ('C', (581, 282), (600, 298), (621, 308))], stroke=paper, width=4)
    d.path(base.MASK, fill=ink, ident='mask')
    d.path(base.BIB, fill=ink, ident='bib')
    d.path([('M', (735, 210)), ('L', (800, 236)), ('L', (741, 250)), ('Z',)], fill=ink, ident='beak')
    d.path([('M', (748, 233)), ('L', (785, 237))], stroke=paper, width=1.3)
    for commands, width in [([('M', (542, 640)), ('C', (541, 644), (539, 646), (537, 647))], 1.6),
                            ([('M', (630, 637)), ('C', (633, 640), (633, 644), (632, 646))], 1.8),
                            ([('M', (646, 636)), ('C', (649, 640), (649, 644), (647, 647))], 1.5)]:
        d.path(commands, stroke=paper, width=width)
    d.circle(*EYE, 9.6, fill=paper)
    d.circle(*EYE, 6.5, fill=ink)
    d.circle(699, 217, 1.5, fill=paper)
    return d


# --- pixel art ---------------------------------------------------------------------

GRID = (150, 126)  # one art pixel is 6 design units


def pixel_grid():
    cols, rows = GRID
    k = cols / W
    small = Image.new('RGB', (cols, rows), base.rgb(PAPER))
    draw = ImageDraw.Draw(small)

    def pts(commands):
        return [(x * k, y * k) for x, y in base.points([c for c in commands if c[0] != 'Z'])]

    draw.polygon(pts(base.BRANCH), fill=base.rgb('#6b5a45'))
    for leg in base.LEGS + base.TOES:
        draw.line(pts(leg), fill=base.rgb('#8a5f4d'), width=1)
    for commands, colour in [(base.TAIL, '#566253'), (base.BODY, '#dcd0b0'), (base.BELLY_SHADOW, '#aeb394'),
                             (base.BACK, '#b86f45'), (base.WING, '#6f573f'), (base.FLIGHTS[0], '#c69a65'),
                             (base.FLIGHTS[1], '#3b5248'), (base.FLIGHTS[2], '#a67c51'), (base.SCAPULAR, '#c58955'),
                             (base.CROWN, '#a05a3b'), (base.CHEEK, '#f1e6c8'), (base.MASK, '#2b3f37'),
                             (base.EAR, '#2b3f37'), (base.BIB, '#2b3f37'), (BEAK_TOP, '#6a6e62'), (BEAK_LOW, '#3c4038')]:
        draw.polygon(pts(commands), fill=base.rgb(colour))
    ex, ey = EYE[0] * k, EYE[1] * k
    draw.rectangle((ex - 1, ey - 1, ex + 1, ey + 1), fill=base.rgb('#1f2a25'))
    draw.point((ex + 1, ey - 1), fill=base.rgb('#fff6d8'))

    def mask_of(commands):
        layer = Image.new('L', small.size)
        ImageDraw.Draw(layer).polygon(pts(commands), fill=255)
        return layer

    area = np.asarray(ImageChops.multiply(mask_of(base.BELLY_SHADOW), mask_of(base.BODY))) > 0
    yy, xx = np.mgrid[0:rows, 0:cols]
    arr = np.asarray(small).copy()
    arr[area & ((xx + yy) % 2 == 0)] = base.rgb('#c9c3a2')
    silhouette = Image.new('L', small.size)
    for commands in (base.BODY, base.TAIL, BEAK_TOP, BEAK_LOW, base.CROWN):
        ImageDraw.Draw(silhouette).polygon(pts(commands), fill=255)
    from PIL import ImageFilter
    ring = np.asarray(silhouette.filter(ImageFilter.MaxFilter(3))).astype(int) - np.asarray(silhouette).astype(int) > 0
    arr[ring] = base.rgb('#3a2f2a')
    return arr


def pixel_art():
    arr = pixel_grid()
    rows, cols = arr.shape[:2]
    cell = 12  # one art pixel is 12 units; the viewBox is a whole 1800 x 1520 so PNG scaling stays exact
    d = kit.Drawing(1800, 1520, background=PAPER, title='Pixel-art bird',
                    description='A perched sparrow on a 150 x 126 pixel grid with a checker dither.')
    paper = tuple(base.rgb(PAPER))
    with d.group(ident='pixels', shape_rendering='crispEdges'):
        for y in range(rows):
            x = 0
            while x < cols:
                colour = tuple(int(v) for v in arr[y, x])
                run = 1
                while x + run < cols and tuple(int(v) for v in arr[y, x + run]) == colour:
                    run += 1
                if colour != paper:
                    d.rect(x * cell, y * cell, run * cell, cell, fill='#%02x%02x%02x' % colour)
                x += run
    return d


# --- ink line ----------------------------------------------------------------------

INK = '#2f261e'


def ink_stroke(d, commands, width, seed):
    """A contour whose width swells and thins, with a slight hand wobble, as a filled outline."""
    rng = random.Random(seed)
    pts = base.points([c for c in commands if c[0] != 'Z'])
    phase = rng.uniform(0, 6)
    wobbled = [(x + rng.uniform(-.25, .25), y + rng.uniform(-.25, .25)) for x, y in pts]
    widths = [width * (0.8 + 0.45 * math.sin(i * 0.09 + phase)) * rng.uniform(.95, 1.05) for i in range(len(pts))]
    outline = kit.ribbon(wobbled, widths)
    d.polygon(outline, fill=INK)


def hatch(d, commands, angle, spacing, width, seed, clip):
    rng = random.Random(seed)
    xs = [x for x, _ in base.points([c for c in commands if c[0] != 'Z'])]
    ys = [y for _, y in base.points([c for c in commands if c[0] != 'Z'])]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    reach = (x1 - x0) + (y1 - y0)
    dx, dy = math.cos(angle), math.sin(angle)
    with d.group(clip=clip):
        for i in range(-int(reach / spacing), int(reach / spacing)):
            sx = x0 + i * spacing + rng.uniform(-.8, .8)
            d.line((sx - dx * reach, y0 - dy * reach), (sx + dx * reach, y0 + dy * reach), INK,
                   width * rng.uniform(.7, 1.2), cap='butt')


def ink_line():
    d = canvas('Ink line bird', 'A perched sparrow in pen and ink with hatching.')
    belly_clip = d.clip_path(base.BELLY_SHADOW)
    body_clip = d.clip_path(base.BODY)
    d.path(base.BRANCH, fill='#d9d0bb', ident='branch')
    with d.group(ident='hatching'):
        with d.group(clip=body_clip):
            hatch(d, base.BELLY_SHADOW, 1.05, 5.2, 1.0, 1, belly_clip)
        hatch(d, base.FLIGHTS[1], .45, 4.2, .9, 2, d.clip_path(base.FLIGHTS[1]))
        hatch(d, base.TAIL, .38, 5.0, .9, 3, d.clip_path(base.TAIL))
        hatch(d, base.CROWN, .75, 4.4, 1.0, 4, d.clip_path(base.CROWN))
    for name, commands in [('mask', base.MASK), ('ear-patch', base.EAR), ('bib', base.BIB), ('beak-upper', BEAK_TOP),
                           ('beak-lower', BEAK_LOW)]:
        d.path(commands, fill=INK, ident=name)
    with d.group(ident='contours'):
        for i, (commands, width) in enumerate([(base.BODY, 2.6), (base.TAIL, 2.2), (base.WING, 2.4), (base.CROWN, 2.2),
                                               (base.CHEEK, 1.8), (base.FLIGHTS[0], 1.8), (base.FLIGHTS[2], 1.8),
                                               (base.SCAPULAR, 1.8), (base.BRANCH, 2.4)]):
            ink_stroke(d, commands, width, 10 + i)
        for i, leg in enumerate(base.LEGS):
            ink_stroke(d, leg, 2.6, 40 + i)
        for i, toe in enumerate(base.TOES):
            ink_stroke(d, toe, 2.1, 50 + i)
    d.circle(*EYE, 8, fill=PAPER)
    ex, ey = EYE
    ink_stroke(d, [('M', (ex + 8, ey)), ('C', (ex + 8, ey - 11), (ex - 8, ey - 11), (ex - 8, ey)),
                   ('C', (ex - 8, ey + 11), (ex + 8, ey + 11), (ex + 8, ey))], 1.6, 60)
    d.circle(*EYE, 4, fill=INK)
    return d


# --- cut paper ---------------------------------------------------------------------

def facet(commands, seed, step=6):
    """Scissor cut: a coarse polygon with small corner jitter instead of a smooth curve."""
    rng = random.Random(seed)
    pts = base.points([c for c in commands if c[0] != 'Z'])
    kept = pts[::step] + [pts[-1]]
    return [('M', kept[0])] + [('L', (x + rng.uniform(-1.3, 1.3), y + rng.uniform(-1.3, 1.3))) for x, y in kept[1:]] + [('Z',)]


def paper_cut():
    d = canvas('Cut-paper bird', 'A perched sparrow assembled from layered, scissor-cut paper.', background='#efe6d2')
    d.raw_def('<filter id="cut-shadow" x="-10%" y="-10%" width="125%" height="130%" color-interpolation-filters="sRGB">'
              '<feGaussianBlur in="SourceAlpha" stdDeviation="3.2" result="blur"/>'
              '<feOffset in="blur" dx="3" dy="4" result="offset"/>'
              '<feFlood flood-color="#1e160e" flood-opacity="0.34"/>'
              '<feComposite in2="offset" operator="in" result="shadow"/>'
              '<feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    d.raw_def('<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
              '<feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="4" result="noise"/>'
              '<feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.25  0 0 0 0 0.19  0 0 0 0 0.1  0.55 0 0 0 -0.14"/></filter>')
    d.raw_def('<filter id="mottle" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
              '<feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="9" result="noise"/>'
              '<feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.36  0 0 0 0 0.2  0.5 0 0 0 -0.12"/></filter>')
    inner = d.clip_path([base.BODY, base.WING])
    layers = [('branch', base.BRANCH, '#7e8f6c', False), ('tail', base.TAIL, '#5b6a62', False), ('body', base.BODY, '#e2d3ae', False),
              ('belly-shade', base.BELLY_SHADOW, '#b9b496', True), ('back', base.BACK, '#c1743f', False),
              ('wing', base.WING, '#7a5a3f', False), ('flight-1', base.FLIGHTS[0], '#d1a56a', True),
              ('flight-2', base.FLIGHTS[1], '#3f5a52', True), ('flight-3', base.FLIGHTS[2], '#b0834f', True),
              ('scapular', base.SCAPULAR, '#cc8c52', True), ('crown', base.CROWN, '#a8573a', False),
              ('cheek', base.CHEEK, '#f4ead0', True), ('mask', base.MASK, '#2c403a', False),
              ('ear-patch', base.EAR, '#2c403a', False), ('bib', base.BIB, '#2c403a', False),
              ('beak-upper', BEAK_TOP, '#4a4d44', False), ('beak-lower', BEAK_LOW, '#2c403a', False)]
    d.rect(0, 0, W, H, fill='#000', filter='url(#mottle)', opacity=.5)
    for i, (name, commands, colour, clipped) in enumerate(layers):
        piece = facet(commands, 100 + i)
        if clipped:
            with d.group(clip=inner):
                with d.group(filter='cut-shadow'):
                    d.path(piece, fill=colour, ident=name)
        else:
            with d.group(filter='cut-shadow'):
                d.path(piece, fill=colour, ident=name)
    for leg in base.LEGS + base.TOES:
        d.path(leg, stroke='#5e4a3b', width=3.6)
    d.circle(*EYE, 9, fill='#f2e8cf')
    d.circle(*EYE, 6, fill='#1f2b27')
    d.rect(0, 0, W, H, fill='#000', filter='url(#grain)', opacity=.55)
    return d


# --- stained glass -----------------------------------------------------------------

LEAD = '#1b1a20'


def clip_half_plane(polygon, point, normal):
    """Keep the part of `polygon` where (p - point) . normal <= 0 (Sutherland-Hodgman)."""
    def inside(p):
        return (p[0] - point[0]) * normal[0] + (p[1] - point[1]) * normal[1] <= 0
    result = []
    for i, current in enumerate(polygon):
        previous = polygon[i - 1]
        if inside(current) != inside(previous):
            t_num = (point[0] - previous[0]) * normal[0] + (point[1] - previous[1]) * normal[1]
            t_den = (current[0] - previous[0]) * normal[0] + (current[1] - previous[1]) * normal[1]
            t = t_num / t_den
            result.append((previous[0] + (current[0] - previous[0]) * t, previous[1] + (current[1] - previous[1]) * t))
        if inside(current):
            result.append(current)
    return result


def voronoi_cells(seeds, width, height):
    cells = []
    for i, s in enumerate(seeds):
        polygon = [(0, 0), (width, 0), (width, height), (0, height)]
        for j, o in enumerate(seeds):
            if i == j or not polygon:
                continue
            midpoint = ((s[0] + o[0]) / 2, (s[1] + o[1]) / 2)
            polygon = clip_half_plane(polygon, midpoint, (o[0] - s[0], o[1] - s[1]))
        cells.append(polygon)
    return cells


def glass_gradient(d, colour):
    value = colour.lstrip('#')
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    top = '#%02x%02x%02x' % tuple(min(255, round(c * 1.28 + 12)) for c in (r, g, b))
    low = '#%02x%02x%02x' % tuple(round(c * .82) for c in (r, g, b))
    return d.linear_gradient([(0, top), (1, low)])


def stained_glass():
    d = kit.Drawing(W, H, background=LEAD, title='Stained-glass bird',
                    description='A perched sparrow in leaded glass against a cool mosaic of panes.')
    rng = random.Random(7)
    seeds = [(rng.uniform(0, W), rng.uniform(0, H)) for _ in range(46)]
    palette = ['#1e3e68', '#245679', '#2c6880', '#1a3056', '#3c5c8a', '#266e6e']
    with d.group(ident='background-panes'):
        for cell in voronoi_cells(seeds, W, H):
            if len(cell) >= 3:
                d.polygon(cell, fill=rng.choice(palette), stroke=LEAD, width=2.6, join='round')
    inner = d.clip_path([base.BODY, base.WING])
    layers = [('branch', base.BRANCH, '#6c9a5a', False), ('tail', base.TAIL, '#2f7b78', False), ('body', base.BODY, '#e1b04a', False),
              ('belly-shade', base.BELLY_SHADOW, '#efd48a', True), ('back', base.BACK, '#cf6a30', False),
              ('wing', base.WING, '#98383a', False), ('flight-1', base.FLIGHTS[0], '#d79a42', True),
              ('flight-2', base.FLIGHTS[1], '#27636b', True), ('flight-3', base.FLIGHTS[2], '#b46f34', True),
              ('scapular', base.SCAPULAR, '#d97e3a', True), ('crown', base.CROWN, '#bd4a2a', False),
              ('cheek', base.CHEEK, '#f5e6b8', True), ('mask', base.MASK, '#243a45', False),
              ('ear-patch', base.EAR, '#243a45', False), ('bib', base.BIB, '#243a45', False),
              ('beak-upper', BEAK_TOP, '#4a5258', False), ('beak-lower', BEAK_LOW, '#243a45', False)]
    with d.group(ident='bird'):
        for name, commands, colour, clipped in layers:
            fill = glass_gradient(d, colour)
            if clipped:
                with d.group(clip=inner):
                    d.path(commands, fill=fill, ident=name)
            else:
                d.path(commands, fill=fill, ident=name)
        with d.group(ident='lead'):
            for name, commands, colour, clipped in layers:
                if clipped:
                    with d.group(clip=inner):
                        d.path(commands, stroke=LEAD, width=9, join='round')
                else:
                    d.path(commands, stroke=LEAD, width=4.6, join='round')
            for leg in base.LEGS + base.TOES:
                d.path(leg, stroke=LEAD, width=5)
        d.circle(*EYE, 10, fill='#f5e6b8', stroke=LEAD, width=2)
        d.circle(*EYE, 5, fill=LEAD)
    d.rect(0, 0, W, H, stroke=LEAD, width=32)
    return d


# --- blueprint ---------------------------------------------------------------------

LINE = '#e6f0ff'
GUIDE = '#9fc2ee'


def ellipse_points(cx, cy, rx, ry, angle=0.0, n=120):
    ca, sa = math.cos(angle), math.sin(angle)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in (i / n * math.tau for i in range(n + 1))]


def blueprint():
    d = kit.Drawing(W, H, background='#1d3a63', title='Blueprint-style bird',
                    description='A construction sheet for a perched sparrow, with guide ellipses and part labels.')
    with d.group(ident='grid'):
        for x in range(0, W + 1, 30):
            major = x % 150 == 0
            d.line((x, 0), (x, H), '#335a8a' if major else '#27476f', 2 if major else 1, cap='butt')
        for y in range(0, H + 1, 30):
            major = y % 150 == 0
            d.line((0, y), (W, y), '#335a8a' if major else '#27476f', 2 if major else 1, cap='butt')
    with d.group(ident='construction-guides'):
        d.polyline(ellipse_points(545, 420, 200, 132, -.47), GUIDE, 1.4, dash=(14, 9))
        d.polyline(ellipse_points(650, 232, 92, 92), GUIDE, 1.4, dash=(14, 9))
        d.line((40, 220), (860, 220), '#7fa6d8', 1.0, dash=(22, 8), cap='butt')
        d.line((125, 584), (555, 260), '#7fa6d8', 1.0, dash=(16, 8), cap='butt')
    with d.group(ident='contours'):
        for commands in (base.BODY, base.TAIL, base.WING, base.CROWN, base.CHEEK, base.FLIGHTS[0], base.FLIGHTS[1],
                         base.FLIGHTS[2], base.SCAPULAR, base.MASK, base.BIB, BEAK_TOP, BEAK_LOW, base.BRANCH):
            d.path(commands, stroke=LINE, width=1.9, join='round')
        for leg in base.LEGS + base.TOES:
            d.path(leg, stroke=LINE, width=1.9)
        d.circle(*EYE, 8, stroke=LINE, width=2)
        d.circle(*EYE, 3, fill=LINE)
    with d.group(ident='labels'):
        for text, anchor, target in [('head', (720, 90), (676, 160)), ('body', (440, 640), (480, 520)),
                                     ('wing', (300, 340), (400, 400)), ('tail', (110, 470), (190, 540))]:
            d.line(anchor, target, GUIDE, 1, cap='butt')
            d.circle(*target, 3, fill=GUIDE)
            d.text(anchor[0], anchor[1] - 6, text, 15, LINE, anchor='middle')
        d.rect(600, 690, 280, 54, stroke=LINE, width=1.5)
        d.text(612, 711, 'CONSTRUCTION STUDY', 13, LINE)
        d.text(612, 733, 'side view / not to scale', 13, GUIDE)
    return d


STYLES = [('geometric', geometric), ('linocut', linocut), ('pixel-art', pixel_art), ('ink-line', ink_line),
          ('paper-cut', paper_cut), ('stained-glass', stained_glass), ('blueprint', blueprint)]
