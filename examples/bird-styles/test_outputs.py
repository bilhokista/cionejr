from pathlib import Path
import unittest
import numpy as np
from PIL import Image, ImageChops

ROOT = Path(__file__).parent
NAMES = ('geometric', 'linocut', 'gouache')
EXTRA = ('pixel-art', 'ink-line', 'paper-cut', 'stained-glass', 'blueprint')
ALL = NAMES + EXTRA

class Outputs(unittest.TestCase):
    def test_three_standalone_images_are_valid(self):
        for name in NAMES:
            with self.subTest(style=name):
                file = ROOT / f'{name}.png'
                self.assertTrue(file.exists(), f'Missing {name}')
                with Image.open(file) as image:
                    self.assertEqual(image.size, (1800, 1520))
                    image.verify()

    def test_three_distinct_images_are_not_identical(self):
        paths = [ROOT / f'{name}.png' for name in NAMES]
        self.assertTrue(all(path.exists() for path in paths), 'Styles not rendered')
        images = [Image.open(path).convert('RGB') for path in paths]
        for i in range(3):
            for j in range(i+1,3):
                self.assertIsNotNone(ImageChops.difference(images[i],images[j]).getbbox())

    def test_panel_backgrounds_match_sheet_background(self):
        self.assertTrue((ROOT/'eight-styles.png').exists(), 'Sheet not rendered')
        with Image.open(ROOT/'eight-styles.png') as sheet:
            background = sheet.getpixel((0,0))
        for name in NAMES:
            with Image.open(ROOT/f'{name}.png') as image:
                self.assertEqual(image.getpixel((0,0)),background,
                                 f'{name} creates an unintended panel rectangle')

    def test_sheet_and_small_preview(self):
        for name,size in [('eight-styles.png',(4320,2240)),('preview.png',(1080,560)),
                          ('construction.png',(1800,1520))]:
            with self.subTest(name=name):
                path = ROOT / name
                self.assertTrue(path.exists(), f'Missing {name}')
                with Image.open(path) as image:
                    self.assertEqual(image.size,size)
                    image.verify()

    def test_all_eight_styles_are_standalone_images_and_pairwise_different(self):
        arrays = []
        for name in ALL:
            with self.subTest(style=name):
                path = ROOT / f'{name}.png'
                self.assertTrue(path.exists(), f'Missing {name}')
                with Image.open(path) as image:
                    self.assertEqual(image.size, (1800, 1520))
                    self.assertEqual(image.mode, 'RGB')
                    arrays.append(np.asarray(image, dtype=np.int16))
        for i in range(len(ALL)):
            for j in range(i + 1, len(ALL)):
                gap = np.abs(arrays[i] - arrays[j]).mean()
                self.assertGreater(gap, 2, f'{ALL[i]} and {ALL[j]} are too alike')

    def test_pixel_art_is_made_of_uniform_blocks_with_a_small_palette(self):
        arr = np.asarray(Image.open(ROOT / 'pixel-art.png').convert('RGB'))
        step = 12
        blocks = arr[:1512].reshape(126, step, 150, step, 3)
        uniform = (blocks == blocks[:, :1, :, :1, :]).all(axis=(1, 3, 4))
        self.assertGreater(uniform.mean(), 0.999)
        colours = {tuple(c) for c in blocks[:, 0, :, 0, :].reshape(-1, 3)}
        self.assertLess(len(colours), 40)


if __name__ == '__main__':
    unittest.main()
