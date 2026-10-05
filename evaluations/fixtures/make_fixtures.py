"""Deterministic test images for the image-dependent evaluation cases (01, 02, 03, 11).

Each image is built to contain one known, checkable property. They are test inputs,
not examples of good drawing.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SIZE = (1000, 800)
PAPER = '#f2ecdc'
INK = '#3b3128'


def canvas():
    image = Image.new('RGB', SIZE, PAPER)
    return image, ImageDraw.Draw(image)


def perched_legs(draw, x, y):
    for dx in (-22, 22):
        draw.line([(x + dx, y), (x + dx - 6, y + 70)], fill=INK, width=6)
    draw.line([(250, y + 72), (700, y + 66)], fill='#6d5a45', width=14)


def case01_pasted_head():
    """Observational bird whose head is a separate circle with no neck transition."""
    image, d = canvas()
    d.ellipse((330, 330, 690, 600), fill='#c9b48d', outline=INK, width=5)
    d.polygon([(340, 470), (150, 600), (180, 640), (370, 540)], fill='#7b8070', outline=INK)
    d.ellipse((600, 215, 770, 385), fill='#a65f3e', outline=INK, width=5)
    d.polygon([(765, 285), (840, 310), (765, 330)], fill='#3b4038', outline=INK)
    d.ellipse((700, 276, 716, 292), fill=INK)
    perched_legs(d, 520, 595)
    image.save(ROOT / '01-pasted-head.png')


def case02_logo_and_illustration():
    logo, d = canvas()
    d.ellipse((380, 250, 640, 510), fill='#2f4a3f')
    d.polygon([(600, 330), (760, 370), (600, 410)], fill='#d89a4a')
    d.polygon([(400, 430), (230, 560), (330, 560), (440, 480)], fill='#2f4a3f')
    d.ellipse((540, 320, 566, 346), fill=PAPER)
    logo.save(ROOT / '02a-logo.png')

    art, d = canvas()
    d.ellipse((330, 330, 690, 600), fill='#d6c39b', outline=INK, width=3)
    d.ellipse((600, 230, 760, 390), fill='#a65f3e', outline=INK, width=3)
    d.polygon([(755, 300), (835, 325), (755, 345)], fill='#3b4038', outline=INK)
    d.ellipse((690, 290, 704, 304), fill=INK)
    # Contract for this drawing: short coverts sit on top of the long flight feathers.
    # Here the flight feathers are drawn last, so they cut across the coverts.
    d.polygon([(400, 430), (560, 420), (500, 520)], fill='#8a6a45', outline=INK)
    for i in range(4):
        d.polygon([(380 + i * 40, 520 + i * 6), (440 + i * 40, 420), (470 + i * 40, 430),
                   (420 + i * 40, 540 + i * 6)], fill='#6e7b64', outline=INK)
    d.polygon([(340, 470), (150, 600), (180, 640), (370, 540)], fill='#7b8070', outline=INK)
    perched_legs(d, 520, 595)
    art.save(ROOT / '02b-detailed-illustration.png')


def case11_petal_wing():
    """Wing feathers that still read as petals after parameter revisions."""
    image, d = canvas()
    d.ellipse((330, 330, 690, 600), fill='#d6c39b', outline=INK, width=4)
    d.ellipse((600, 230, 760, 390), fill='#a65f3e', outline=INK, width=4)
    d.polygon([(755, 300), (835, 325), (755, 345)], fill='#3b4038', outline=INK)
    d.ellipse((690, 290, 704, 304), fill=INK)
    d.polygon([(340, 470), (150, 600), (180, 640), (370, 540)], fill='#7b8070', outline=INK)
    for i in range(7):
        x = 400 + i * 28
        d.ellipse((x, 400 + i * 8, x + 70, 470 + i * 8), fill='#8a7d5a', outline=INK, width=3)
    perched_legs(d, 520, 595)
    image.save(ROOT / '11-petal-wing.png')


def case03_large_head_character():
    """Fictional character: huge head, tiny feet, consistent round-shape rules."""
    image, d = canvas()
    d.line([(150, 690), (850, 690)], fill='#8a7a60', width=6)
    d.ellipse((330, 120, 670, 460), fill='#e9b98a', outline=INK, width=5)
    d.ellipse((400, 250, 440, 300), fill=INK)
    d.ellipse((560, 250, 600, 300), fill=INK)
    d.arc((440, 320, 560, 410), 20, 160, fill=INK, width=5)
    d.ellipse((410, 440, 590, 640), fill='#6a8fb0', outline=INK, width=5)
    d.ellipse((400, 640, 480, 692), fill='#b66a4a', outline=INK, width=5)
    d.ellipse((520, 640, 600, 692), fill='#b66a4a', outline=INK, width=5)
    d.line([(410, 500), (340, 560)], fill=INK, width=14)
    d.line([(590, 500), (670, 450)], fill=INK, width=14)
    image.save(ROOT / '03-large-head-character.png')


if __name__ == '__main__':
    case01_pasted_head()
    case02_logo_and_illustration()
    case03_large_head_character()
    case11_petal_wing()
    print('Saved fixtures')
