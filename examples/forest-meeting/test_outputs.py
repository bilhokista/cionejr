"""Output checks are not certificates of drawing quality."""
from pathlib import Path
import importlib.util
import unittest
import numpy as np
from PIL import Image

ROOT = Path(__file__).parent


def load_renderer():
    spec = importlib.util.spec_from_file_location('meeting_renderer', ROOT / 'render.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Outputs(unittest.TestCase):
    def test_full_page_size_and_full_bleed(self):
        with Image.open(ROOT / 'forest-meeting.png') as image:
            self.assertEqual(image.size, (2400, 3000))
            self.assertEqual(image.mode, 'RGB')
            image.verify()
        with Image.open(ROOT / 'forest-meeting.png') as image:
            for xy in ((0, 0), (2399, 0), (0, 2999), (2399, 2999)):
                self.assertLess(max(image.getpixel(xy)), 245)

    def test_preview_and_layout_exist(self):
        for name, size in [('preview.png', (600, 750)), ('composition.png', (1000, 1250))]:
            with self.subTest(name=name), Image.open(ROOT / name) as image:
                self.assertEqual(image.size, size)
                image.verify()

    def test_audience_members_do_not_overlap_each_other(self):
        module = load_renderer()
        placed = {}
        module.stage(placed)
        names = list(placed)
        arrays = {n: np.asarray(placed[n]) > 40 for n in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                overlap = (arrays[a] & arrays[b]).sum()
                self.assertEqual(overlap, 0, f'{a} overlaps {b}')

    def test_every_animal_stands_inside_the_page_and_below_the_stump_top(self):
        module = load_renderer()
        placed = {}
        module.stage(placed)
        for name, alpha in placed.items():
            left, top, right, bottom = alpha.getbbox()
            with self.subTest(animal=name):
                self.assertGreaterEqual(left, 0)
                self.assertLessEqual(right, module.CANVAS[0])
                self.assertLessEqual(bottom, module.CANVAS[1])
                self.assertGreater(bottom, module.STUMP_TOP * module.S)


if __name__ == '__main__':
    unittest.main()
