"""Five more authored digital treatments of the bird in examples/bird-styles.

They reuse its construction (body, wing, tail, head masses) and change only the
visual language. Each is a digital study, not a physical print, glass or paper.
"""
from pathlib import Path
import importlib.util
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = Path(__file__).parent
_spec = importlib.util.spec_from_file_location('bird_base', ROOT.parent / 'bird-styles' / 'render.py')
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

S, W, H, PAPER = base.S, base.W, base.H, base.PAPER
FINAL = (1800, 1520)
PIXEL = 12  # one art pixel is 12 final pixels
BEAK_TOP = [('M', (733, 201)), ('L', (800, 236)), ('L', (741, 239)), ('L', (733, 201))]
BEAK_LOW = [('M', (741, 239)), ('L', (800, 236)), ('L', (741, 250)), ('L', (741, 239))]
EYE = (697, 220)
FLIGHT_COLOURS = ['#c69a65', '#3e554b', '#a67c51']


def full():
    return Image.new('RGB', (W * S, H * S), base.rgb(PAPER))


def scaled(commands, factor):
    return [(kind, *[(x * factor, y * factor) for x, y in coords]) for kind, *coords in commands]


def mask_of(*shapes):
    result = base.shape_mask(shapes[0])
    for shape in shapes[1:]:
        result = ImageChops.lighter(result, base.shape_mask(shape))
    return result


# --- pixel art ---------------------------------------------------------------

def pixel_art():
    cols, rows = FINAL[0] // PIXEL, FINAL[1] // PIXEL
    k = cols / W  # the 900 x 760 design space maps onto the whole art grid
    ox, oy = 0, 0
    small = Image.new('RGB', (cols, rows), base.rgb(PAPER))
    d = ImageDraw.Draw(small)

    def poly(commands, colour):
        pts = [(x * k + ox, y * k + oy) for x, y in base.points(commands)]
        d.polygon(pts, fill=base.rgb(colour))

    def stroke(commands, colour, width=1):
        pts = [(x * k + ox, y * k + oy) for x, y in base.points(commands)]
        d.line(pts, fill=base.rgb(colour), width=width)

    poly(base.BRANCH, '#6b5a45')
    for leg in base.LEGS:
        stroke(leg, '#8a5f4d')
    for toe in base.TOES:
        stroke(toe, '#8a5f4d')
    shapes = [(base.TAIL, '#566253'), (base.BODY, '#dcd0b0'), (base.BELLY_SHADOW, '#aeb394'),
              (base.BACK, '#b86f45'), (base.WING, '#6f573f'), (base.FLIGHTS[0], '#c69a65'),
              (base.FLIGHTS[1], '#3b5248'), (base.FLIGHTS[2], '#a67c51'), (base.SCAPULAR, '#c58955'),
              (base.CROWN, '#a05a3b'), (base.CHEEK, '#f1e6c8'), (base.MASK, '#2b3f37'),
              (base.EAR, '#2b3f37'), (base.BIB, '#2b3f37'), (BEAK_TOP, '#6a6e62'), (BEAK_LOW, '#3c4038')]
    for commands, colour in shapes:
        poly(commands, colour)
    ex, ey = EYE[0] * k + ox, EYE[1] * k + oy
    d.rectangle((ex - 1, ey - 1, ex + 1, ey + 1), fill=base.rgb('#1f2a25'))
    d.point((ex + 1, ey - 1), fill=base.rgb('#fff6d8'))

    # Dither the belly shade in a checker pattern instead of a smooth blend.
    shade = Image.new('L', small.size)
    ImageDraw.Draw(shade).polygon([(x * k + ox, y * k + oy) for x, y in base.points(base.BELLY_SHADOW)], fill=255)
    body = Image.new('L', small.size)
    ImageDraw.Draw(body).polygon([(x * k + ox, y * k + oy) for x, y in base.points(base.BODY)], fill=255)
    area = np.asarray(ImageChops.multiply(shade, body)) > 0
    yy, xx = np.mgrid[0:rows, 0:cols]
    checker = area & ((xx + yy) % 2 == 0)
    arr = np.asarray(small).copy()
    arr[checker] = base.rgb('#c9c3a2')
    small = Image.fromarray(arr)

    # One-pixel dark outline around the whole silhouette.
    sil = Image.new('L', small.size)
    sd = ImageDraw.Draw(sil)
    for commands in (base.BODY, base.TAIL, BEAK_TOP, BEAK_LOW, base.CROWN):
        sd.polygon([(x * k + ox, y * k + oy) for x, y in base.points(commands)], fill=255)
    ring = np.asarray(sil.filter(ImageFilter.MaxFilter(3))).astype(int) - np.asarray(sil).astype(int) > 0
    arr = np.asarray(small).copy()
    arr[ring] = base.rgb('#3a2f2a')
    result = Image.fromarray(arr).resize((cols * PIXEL, rows * PIXEL), Image.Resampling.NEAREST)
    canvas = Image.new('RGB', FINAL, base.rgb(PAPER))
    canvas.paste(result, (0, 0))
    return canvas


# --- ink line drawing ------------------------------------------------------------

INK = '#2f261e'


def inked(image, commands, width, seed):
    """Contour with pressure that swells and thins, and a slight hand wobble."""
    rng = random.Random(seed)
    pts = [(x * S, y * S) for x, y in base.points(commands)]
    d = ImageDraw.Draw(image)
    phase = rng.uniform(0, 6)
    for i in range(len(pts) - 1):
        w = width * S * (0.8 + 0.45 * math.sin(i * 0.09 + phase)) * rng.uniform(0.92, 1.08)
        jx, jy = rng.uniform(-.5, .5) * S, rng.uniform(-.5, .5) * S
        a, b = pts[i], (pts[i + 1][0] + jx, pts[i + 1][1] + jy)
        d.line([a, b], fill=base.rgb(INK), width=max(1, round(w)))
        d.ellipse((b[0] - w / 2, b[1] - w / 2, b[0] + w / 2, b[1] + w / 2), fill=base.rgb(INK))


def hatch(commands, angle, spacing, width, seed, clip=None):
    mask = base.shape_mask(commands)
    if clip is not None:
        mask = ImageChops.multiply(mask, clip)
    rng = random.Random(seed)

    def paint(layer):
        d = ImageDraw.Draw(layer)
        x0, y0, x1, y1 = [v / S for v in mask.getbbox()]
        reach = (x1 - x0) + (y1 - y0)
        dx, dy = math.cos(angle), math.sin(angle)
        n = int(reach / spacing)
        for i in range(-n, n):
            cx = x0 + i * spacing
            sx = cx + rng.uniform(-.8, .8)
            d.line([((sx - dx * reach) * S, (y0 - dy * reach) * S), ((sx + dx * reach) * S, (y0 + dy * reach) * S)],
                   fill=base.rgb(INK), width=max(1, round(width * S * rng.uniform(.7, 1.2))))

    return mask, paint


def ink_drawing():
    image = full()
    d = ImageDraw.Draw(image)
    body = base.shape_mask(base.BODY)
    for commands, angle, spacing, width, seed in [
            (base.BELLY_SHADOW, 1.05, 5.2, 1.0, 1), (base.FLIGHTS[1], .45, 4.2, .9, 2),
            (base.TAIL, .38, 5.0, .9, 3), (base.CROWN, .75, 4.4, 1.0, 4)]:
        mask, paint = hatch(commands, angle, spacing, width, seed, clip=body if commands is base.BELLY_SHADOW else None)
        base.clipped(image, mask, paint)
    for commands in (base.MASK, base.EAR, base.BIB, BEAK_TOP, BEAK_LOW):
        base.drawpath(image, commands, fill=INK)
    base.drawpath(image, base.BRANCH, fill='#d9d0bb')
    outlines = [(base.BODY, 2.6), (base.TAIL, 2.2), (base.WING, 2.0), (base.CROWN, 2.2), (base.CHEEK, 1.8),
                (base.FLIGHTS[0], 1.4), (base.FLIGHTS[2], 1.4), (base.SCAPULAR, 1.4), (base.BRANCH, 2.4)]
    for i, (commands, width) in enumerate(outlines):
        inked(image, commands, width, 10 + i)
    for i, leg in enumerate(base.LEGS):
        inked(image, leg, 2.6, 40 + i)
    for i, toe in enumerate(base.TOES):
        inked(image, toe, 2.1, 50 + i)
    d.ellipse(((EYE[0] - 8) * S, (EYE[1] - 8) * S, (EYE[0] + 8) * S, (EYE[1] + 8) * S), fill=base.rgb(PAPER))
    inked(image, [('M', (EYE[0] + 8, EYE[1])), ('C', (EYE[0] + 8, EYE[1] - 11), (EYE[0] - 8, EYE[1] - 11), (EYE[0] - 8, EYE[1])),
                  ('C', (EYE[0] - 8, EYE[1] + 11), (EYE[0] + 8, EYE[1] + 11), (EYE[0] + 8, EYE[1]))], 1.6, 60)
    d.ellipse(((EYE[0] - 4) * S, (EYE[1] - 4) * S, (EYE[0] + 4) * S, (EYE[1] + 4) * S), fill=base.rgb(INK))
    return image


# --- cut paper collage -------------------------------------------------------------

def facet(commands, seed, step=6):
    """Scissor cut: a coarse polygon with small corner jitter instead of a smooth curve."""
    rng = random.Random(seed)
    pts = base.points(commands)
    kept = pts[::step] + [pts[-1]]
    return [('M', kept[0])] + [('L', (x + rng.uniform(-1.3, 1.3), y + rng.uniform(-1.3, 1.3))) for x, y in kept[1:]]


def paper_sheet(colour, seed):
    rng = np.random.default_rng(seed)
    arr = np.array(base.rgb(colour), dtype=np.float32)[None, None, :] + np.zeros((H * S, W * S, 1), np.float32)
    arr += base.smooth_noise(rng, (H * S, W * S), 40 * S)[:, :, None] * 5
    arr += rng.normal(0, 2.2, (H * S, W * S))[:, :, None]
    # Faint fibres, long and thin, like the grain of handmade paper.
    fibre = Image.new('L', (W * S, H * S))
    fd = ImageDraw.Draw(fibre)
    for _ in range(900):
        x, y, a, length = rng.uniform(0, W * S), rng.uniform(0, H * S), rng.uniform(0, math.pi), rng.uniform(8, 30) * S
        fd.line([(x, y), (x + math.cos(a) * length, y + math.sin(a) * length)], fill=int(rng.integers(20, 60)), width=1)
    arr += (np.asarray(fibre, dtype=np.float32) / 255 * 22)[:, :, None] - 3
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def paper_collage():
    image = paper_sheet('#efe6d2', 1)
    layers = [(base.BRANCH, '#7e8f6c'), (base.TAIL, '#5b6a62'), (base.BODY, '#e2d3ae'),
              (base.BELLY_SHADOW, '#b9b496'), (base.BACK, '#c1743f'), (base.WING, '#7a5a3f'),
              (base.FLIGHTS[0], '#d1a56a'), (base.FLIGHTS[1], '#3f5a52'), (base.FLIGHTS[2], '#b0834f'),
              (base.SCAPULAR, '#cc8c52'), (base.CROWN, '#a8573a'), (base.CHEEK, '#f4ead0'),
              (base.MASK, '#2c403a'), (base.EAR, '#2c403a'), (base.BIB, '#2c403a'),
              (BEAK_TOP, '#4a4d44'), (BEAK_LOW, '#2c403a')]
    body = base.shape_mask(base.BODY)
    for i, (commands, colour) in enumerate(layers):
        cut = facet(commands, 100 + i)
        mask = base.shape_mask(cut)
        if commands in (base.BELLY_SHADOW, base.FLIGHTS[0], base.FLIGHTS[1], base.FLIGHTS[2], base.SCAPULAR, base.CHEEK):
            mask = ImageChops.multiply(mask, ImageChops.lighter(body, base.shape_mask(base.WING)))
        # Each piece casts a short soft shadow onto the layers below it.
        shadow = ImageChops.offset(mask, 3 * S, 4 * S).filter(ImageFilter.GaussianBlur(3.2 * S))
        dark = Image.eval(shadow, lambda v: int(v * .34))
        image.paste(Image.new('RGB', image.size, (30, 22, 14)), (0, 0), dark)
        image.paste(paper_sheet(colour, 200 + i), (0, 0), mask)
    for leg in base.LEGS + base.TOES:
        base.drawpath(image, leg, stroke='#5e4a3b', width=3.6)
    d = ImageDraw.Draw(image)
    d.ellipse(((EYE[0] - 9) * S, (EYE[1] - 9) * S, (EYE[0] + 9) * S, (EYE[1] + 9) * S), fill=base.rgb('#f2e8cf'))
    d.ellipse(((EYE[0] - 6) * S, (EYE[1] - 6) * S, (EYE[0] + 6) * S, (EYE[1] + 6) * S), fill=base.rgb('#1f2b27'))
    return image


# --- stained glass -------------------------------------------------------------------

LEAD = '#1b1a20'


def glass_fill(image, mask, colour, seed):
    """Translucent glass: lighter towards the top where light enters, with mottling."""
    x0, y0, x1, y1 = mask.getbbox()
    rng = np.random.default_rng(seed)
    height, width = y1 - y0, x1 - x0
    t = np.linspace(0, 1, height)[:, None, None]
    top = np.array(base.rgb(colour), dtype=np.float32) * 1.28 + 12
    low = np.array(base.rgb(colour), dtype=np.float32) * .82
    arr = top[None, None, :] * (1 - t) + low[None, None, :] * t
    arr = arr + np.zeros((height, width, 3), np.float32)
    arr += base.smooth_noise(rng, (height, width), 14 * S)[:, :, None] * 9
    patch = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    image.paste(patch, (x0, y0), mask.crop((x0, y0, x1, y1)))


def voronoi_background(image):
    rng = np.random.default_rng(7)
    seeds = rng.uniform((0, 0), (W * S, H * S), (46, 2))
    palette = [(30, 62, 104), (36, 86, 122), (44, 104, 128), (26, 48, 86), (60, 92, 138), (38, 110, 110)]
    yy, xx = np.mgrid[0:H * S, 0:W * S]
    best = np.full((H * S, W * S), 1e12, np.float32)
    label = np.zeros((H * S, W * S), np.int16)
    for i, (sx, sy) in enumerate(seeds):
        dist = (xx - sx) ** 2 + (yy - sy) ** 2
        closer = dist < best
        best[closer] = dist[closer]
        label[closer] = i
    colours = np.array([palette[int(rng.integers(len(palette)))] for _ in seeds], dtype=np.float32)
    arr = colours[label] + rng.normal(0, 3, (H * S, W * S, 1))
    edge = (label != np.roll(label, 1, 0)) | (label != np.roll(label, 1, 1))
    edge = np.asarray(Image.fromarray((edge * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * S + 1))) > 0
    arr[edge] = base.rgb(LEAD)
    image.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))


def stained_glass():
    image = Image.new('RGB', (W * S, H * S))
    voronoi_background(image)
    layers = [(base.BRANCH, '#6c9a5a'), (base.TAIL, '#2f7b78'), (base.BODY, '#e1b04a'),
              (base.BELLY_SHADOW, '#efd48a'), (base.BACK, '#cf6a30'), (base.WING, '#98383a'),
              (base.FLIGHTS[0], '#d79a42'), (base.FLIGHTS[1], '#27636b'), (base.FLIGHTS[2], '#b46f34'),
              (base.SCAPULAR, '#d97e3a'), (base.CROWN, '#bd4a2a'), (base.CHEEK, '#f5e6b8'),
              (base.MASK, '#243a45'), (base.EAR, '#243a45'), (base.BIB, '#243a45'),
              (BEAK_TOP, '#4a5258'), (BEAK_LOW, '#243a45')]
    body = base.shape_mask(base.BODY)
    inner = ImageChops.lighter(body, base.shape_mask(base.WING))
    clipped_pieces = (base.BELLY_SHADOW, base.FLIGHTS[0], base.FLIGHTS[1], base.FLIGHTS[2], base.SCAPULAR, base.CHEEK)
    for i, (commands, colour) in enumerate(layers):
        mask = base.shape_mask(commands)
        if commands in clipped_pieces:
            mask = ImageChops.multiply(mask, inner)
        glass_fill(image, mask, colour, 300 + i)
    for commands, _ in layers:
        if commands in clipped_pieces:
            # Lead only where the piece is actually visible; the stroke is centred on the edge, so double it.
            base.clipped(image, ImageChops.multiply(base.shape_mask(commands), inner),
                         lambda layer, c=commands: base.drawpath(layer, c, stroke=LEAD, width=9))
        else:
            base.drawpath(image, commands, stroke=LEAD, width=4.6)
    for leg in base.LEGS + base.TOES:
        base.drawpath(image, leg, stroke=LEAD, width=5)
    d = ImageDraw.Draw(image)
    d.ellipse(((EYE[0] - 10) * S, (EYE[1] - 10) * S, (EYE[0] + 10) * S, (EYE[1] + 10) * S), fill=base.rgb('#f5e6b8'), outline=base.rgb(LEAD), width=4 * S // 2)
    d.ellipse(((EYE[0] - 5) * S, (EYE[1] - 5) * S, (EYE[0] + 5) * S, (EYE[1] + 5) * S), fill=base.rgb(LEAD))
    d.rectangle((0, 0, W * S - 1, H * S - 1), outline=base.rgb(LEAD), width=16 * S)
    return image


# --- blueprint ------------------------------------------------------------------------

LINE = '#e6f0ff'


def dashed(image, pts, dash=14, gap=9, colour='#9fc2ee', width=1.4):
    d = ImageDraw.Draw(image)
    i, on = 0, True
    while i < len(pts) - 1:
        step = dash if on else gap
        j = min(len(pts) - 1, i + step)
        if on:
            d.line([(x * S, y * S) for x, y in pts[i:j + 1]], fill=base.rgb(colour), width=max(1, round(width * S)))
        i, on = j, not on


def ellipse_points(cx, cy, rx, ry, angle=0.0, n=240):
    ca, sa = math.cos(angle), math.sin(angle)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in (i / n * math.tau for i in range(n + 1))]


def blueprint():
    image = Image.new('RGB', (W * S, H * S), base.rgb('#1d3a63'))
    d = ImageDraw.Draw(image)
    for x in range(0, W, 30):
        d.line([(x * S, 0), (x * S, H * S)], fill=base.rgb('#27476f' if x % 150 else '#335a8a'), width=S if x % 150 else 2 * S)
    for y in range(0, H, 30):
        d.line([(0, y * S), (W * S, y * S)], fill=base.rgb('#27476f' if y % 150 else '#335a8a'), width=S if y % 150 else 2 * S)
    dashed(image, ellipse_points(545, 420, 200, 132, -.47))
    dashed(image, ellipse_points(650, 232, 92, 92))
    dashed(image, [(x, 220) for x in range(40, 860, 2)], 22, 8, '#7fa6d8', 1.0)
    dashed(image, [(125 + t * 4.3, 584 - t * 3.24) for t in range(0, 101)], 16, 8, '#7fa6d8', 1.0)
    for commands in (base.BODY, base.TAIL, base.WING, base.CROWN, base.CHEEK, base.FLIGHTS[0], base.FLIGHTS[1],
                     base.FLIGHTS[2], base.SCAPULAR, base.MASK, base.BIB, BEAK_TOP, BEAK_LOW, base.BRANCH):
        base.drawpath(image, commands, stroke=LINE, width=1.9)
    for leg in base.LEGS + base.TOES:
        base.drawpath(image, leg, stroke=LINE, width=1.9)
    d.ellipse(((EYE[0] - 8) * S, (EYE[1] - 8) * S, (EYE[0] + 8) * S, (EYE[1] + 8) * S), outline=base.rgb(LINE), width=2 * S)
    d.ellipse(((EYE[0] - 3) * S, (EYE[1] - 3) * S, (EYE[0] + 3) * S, (EYE[1] + 3) * S), fill=base.rgb(LINE))
    font = base.choose_label_font(15 * S)
    for text, anchor, target in [('head', (720, 90), (676, 160)), ('body', (440, 640), (480, 520)),
                                 ('wing', (300, 340), (400, 400)), ('tail', (110, 470), (190, 540))]:
        d.line([(anchor[0] * S, anchor[1] * S), (target[0] * S, target[1] * S)], fill=base.rgb('#9fc2ee'), width=S)
        d.ellipse(((target[0] - 3) * S, (target[1] - 3) * S, (target[0] + 3) * S, (target[1] + 3) * S), fill=base.rgb('#9fc2ee'))
        box = d.textbbox((0, 0), text, font=font)
        d.text((anchor[0] * S - (box[2] - box[0]) / 2, anchor[1] * S - (box[3] - box[1]) - 6 * S), text, font=font, fill=base.rgb(LINE))
    title = base.choose_label_font(13 * S)
    d.rectangle((600 * S, 690 * S, 880 * S, 744 * S), outline=base.rgb(LINE), width=S + 1)
    d.text((612 * S, 696 * S), 'CONSTRUCTION STUDY', font=title, fill=base.rgb(LINE))
    d.text((612 * S, 718 * S), 'side view / not to scale', font=title, fill=base.rgb('#9fc2ee'))
    return image


STYLES = [('pixel-art', pixel_art), ('ink-line', ink_drawing), ('paper-cut', paper_collage),
          ('stained-glass', stained_glass), ('blueprint', blueprint)]


def contact_sheet(panels):
    sheet = Image.new('RGB', (3240, 2240), base.rgb(PAPER))
    font = base.choose_label_font(36)
    d = ImageDraw.Draw(sheet)
    for i, ((name, _), image) in enumerate(zip(STYLES, panels)):
        row, col = divmod(i, 3)
        offset = 540 if row == 1 else 0
        x = offset + col * 1080 + 18
        y = row * 1080 + 80
        sheet.paste(image.resize((1044, 882), Image.Resampling.LANCZOS), (x, y))
        label = name.replace('-', ' ').capitalize()
        box = d.textbbox((0, 0), label, font=font)
        d.text((x + (1044 - (box[2] - box[0])) // 2, y + 900), label, font=font, fill='#4e5148')
    return sheet


def main():
    panels = []
    for name, build in STYLES:
        image = build()
        if image.size != FINAL:
            image = image.resize(FINAL, Image.Resampling.LANCZOS)
        image.save(ROOT / f'{name}.png')
        panels.append(image)
        print('Saved', name)
    sheet = contact_sheet(panels)
    sheet.save(ROOT / 'five-styles.png')
    sheet.resize((1080, 747), Image.Resampling.LANCZOS).save(ROOT / 'preview.png')
    print('Saved five-styles.png and preview.png')


if __name__ == '__main__':
    main()
