"""Output checks are not certificates of drawing quality."""
from io import BytesIO
from pathlib import Path
import importlib.util
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
SVG_NS = '{http://www.w3.org/2000/svg}'
CHARACTERS = ('owl', 'fox', 'deer', 'rabbit', 'squirrel', 'hedgehog', 'mouse')


def load_renderer():
    spec = importlib.util.spec_from_file_location('meeting_renderer', ROOT / 'render.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coverage(module, name):
    """Boolean page mask of one character drawn alone on a transparent page."""
    drawing = module.scene(only=[name], with_background=False)
    data = module.kit.render_png(drawing.to_svg(), 500, 625)
    return np.asarray(Image.open(BytesIO(data)).convert('RGBA'))[:, :, 3] > 40


class Outputs(unittest.TestCase):
    def test_full_page_size_and_full_bleed(self):
        with Image.open(ROOT / 'forest-meeting.png') as image:
            self.assertEqual(image.size, (2400, 3000))
            self.assertEqual(image.mode, 'RGB')
            for xy in ((0, 0), (2399, 0), (0, 2999), (2399, 2999)):
                self.assertLess(max(image.getpixel(xy)), 245)

    def test_preview_and_greyscale_layout_exist(self):
        for name, size in [('preview.png', (600, 750)), ('composition.png', (1000, 1250))]:
            with self.subTest(name=name), Image.open(ROOT / name) as image:
                self.assertEqual(image.size, size)
        layout = np.asarray(Image.open(ROOT / 'composition.png').convert('RGB'), dtype=np.int16)
        self.assertLess(np.abs(layout[:, :, 0] - layout[:, :, 1]).max(), 3, 'layout should carry no hue')


class VectorMaster(unittest.TestCase):
    def setUp(self):
        self.root = ET.parse(ROOT / 'forest-meeting.svg').getroot()

    def test_svg_is_well_formed_and_has_no_embedded_raster(self):
        self.assertEqual(self.root.get('viewBox'), '0 0 1000 1250')
        text = (ROOT / 'forest-meeting.svg').read_text(encoding='utf-8')
        self.assertNotIn('<image', text)
        self.assertNotIn('data:image', text)

    def test_every_character_and_set_piece_is_a_named_group(self):
        ids = {el.get('id') for el in self.root.iter() if el.get('id')}
        self.assertTrue(set(CHARACTERS) <= ids, ids)
        self.assertTrue({'stump', 'log', 'canopy', 'trunks', 'ground'} <= ids, ids)

    def test_characters_are_transformed_groups_not_baked_coordinates(self):
        groups = {el.get('id'): el for el in self.root.iter(SVG_NS + 'g') if el.get('id')}
        for name in CHARACTERS:
            with self.subTest(character=name):
                self.assertIn('translate(', groups[name].get('transform', ''))

    def test_cast_horizontal_facing_matches_the_stump_side(self):
        groups = {el.get('id'): el.get('transform') for el in self.root.iter(SVG_NS + 'g') if el.get('id') in CHARACTERS}
        owl_x = 500
        module = load_renderer()
        for name in module.BACK_TO_FRONT:
            _, x, _, _, flipped = module.CAST[name]
            faces_right = 'scale(-' not in groups[name]
            with self.subTest(character=name):
                self.assertEqual(faces_right, x < owl_x, f'{name} should face the stump')
                self.assertEqual(flipped, not faces_right)


class Placement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_renderer()
        cls.masks = {name: coverage(cls.module, name) for name in CHARACTERS}

    def test_no_two_characters_overlap(self):
        names = list(self.masks)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                with self.subTest(pair=(a, b)):
                    self.assertEqual(int((self.masks[a] & self.masks[b]).sum()), 0, f'{a} overlaps {b}')

    def test_every_character_is_fully_inside_the_page_and_visible(self):
        for name, mask in self.masks.items():
            with self.subTest(character=name):
                ys, xs = np.nonzero(mask)
                self.assertGreater(len(xs), 400, f'{name} is missing or tiny')
                self.assertGreater(xs.min(), 0)
                self.assertGreater(ys.min(), 0)
                self.assertLess(xs.max(), mask.shape[1] - 1)
                self.assertLess(ys.max(), mask.shape[0] - 1)

    def test_the_owl_is_highest_and_horizontally_aligned_over_the_stump(self):
        tops = {name: int(np.nonzero(mask.any(axis=1))[0].min()) for name, mask in self.masks.items()}
        self.assertEqual(min(tops, key=tops.get), 'owl')
        ys, xs = np.nonzero(self.masks['owl'])
        self.assertAlmostEqual(xs.mean() / self.masks['owl'].shape[1] * 1000, 500, delta=25)


if __name__ == '__main__':
    unittest.main()
