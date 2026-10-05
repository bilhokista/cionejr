"""Output checks are not certificates of drawing quality."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
SVG_NS = '{http://www.w3.org/2000/svg}'
VECTOR = ('geometric', 'linocut', 'pixel-art', 'ink-line', 'paper-cut', 'stained-glass', 'blueprint')
ALL = ('geometric', 'linocut', 'gouache') + VECTOR[2:]
ORIGINAL_THREE = ('geometric', 'linocut', 'gouache')


class Outputs(unittest.TestCase):
    def test_every_style_has_a_standalone_png(self):
        for name in ALL:
            with self.subTest(style=name):
                with Image.open(ROOT / f'{name}.png') as image:
                    self.assertEqual(image.size, (1800, 1520))
                    self.assertEqual(image.mode, 'RGB')
                    image.verify()

    def test_styles_are_pairwise_different(self):
        arrays = [np.asarray(Image.open(ROOT / f'{name}.png').convert('RGB'), dtype=np.int16) for name in ALL]
        for i in range(len(ALL)):
            for j in range(i + 1, len(ALL)):
                gap = np.abs(arrays[i] - arrays[j]).mean()
                self.assertGreater(gap, 2, f'{ALL[i]} and {ALL[j]} are too alike')

    def test_panel_backgrounds_match_sheet_background_for_unframed_styles(self):
        with Image.open(ROOT / 'eight-styles.png') as sheet:
            background = sheet.getpixel((0, 0))
        for name in ORIGINAL_THREE + ('pixel-art', 'ink-line'):
            with Image.open(ROOT / f'{name}.png') as image:
                self.assertEqual(image.getpixel((0, 0)), background, f'{name} creates an unintended panel rectangle')

    def test_sheet_preview_and_construction(self):
        for name, size in [('eight-styles.png', (4320, 2240)), ('preview.png', (1080, 560)), ('construction.png', (1800, 1520))]:
            with self.subTest(name=name), Image.open(ROOT / name) as image:
                self.assertEqual(image.size, size)
                image.verify()

    def test_pixel_art_is_made_of_uniform_blocks_with_a_small_palette(self):
        arr = np.asarray(Image.open(ROOT / 'pixel-art.png').convert('RGB'))
        blocks = arr[:1512].reshape(126, 12, 150, 12, 3)
        uniform = (blocks == blocks[:, :1, :, :1, :]).all(axis=(1, 3, 4))
        self.assertGreater(uniform.mean(), 0.999)
        colours = {tuple(c) for c in blocks[:, 0, :, 0, :].reshape(-1, 3)}
        self.assertLess(len(colours), 40)

    def test_the_bottom_edge_is_not_transparent_or_dark(self):
        for name in VECTOR:
            if name in ('stained-glass', 'blueprint'):
                continue
            with self.subTest(style=name), Image.open(ROOT / f'{name}.png') as image:
                self.assertGreater(min(image.convert('RGB').getpixel((900, 1519))), 150)


class VectorMasters(unittest.TestCase):
    def parse(self, name):
        return ET.parse(ROOT / 'svg' / f'{name}.svg').getroot()

    def test_each_vector_style_has_a_well_formed_svg_with_a_viewbox(self):
        for name in VECTOR:
            with self.subTest(style=name):
                root = self.parse(name)
                self.assertEqual(root.tag, SVG_NS + 'svg')
                self.assertEqual(len(root.get('viewBox').split()), 4)
                self.assertIsNotNone(root.find(SVG_NS + 'title'))

    def test_svgs_are_real_vector_with_no_embedded_raster(self):
        for name in VECTOR:
            with self.subTest(style=name):
                text = (ROOT / 'svg' / f'{name}.svg').read_text(encoding='utf-8')
                self.assertNotIn('<image', text)
                self.assertNotIn('data:image', text)

    def test_vector_masters_keep_named_parts_for_editing(self):
        for name in ('geometric', 'linocut', 'stained-glass', 'paper-cut', 'ink-line'):
            with self.subTest(style=name):
                ids = {el.get('id') for el in self.parse(name).iter() if el.get('id')}
                self.assertTrue({'bib', 'mask', 'branch'} <= ids, ids)
                if name != 'ink-line':
                    self.assertTrue({'body', 'wing'} <= ids, ids)

    def test_gouache_is_raster_only(self):
        self.assertFalse((ROOT / 'svg' / 'gouache.svg').exists())

    def test_png_aspect_matches_svg_viewbox(self):
        for name in VECTOR:
            with self.subTest(style=name):
                _, _, w, h = (float(v) for v in self.parse(name).get('viewBox').split())
                self.assertAlmostEqual(w / h, 1800 / 1520, delta=0.003)


if __name__ == '__main__':
    unittest.main()
