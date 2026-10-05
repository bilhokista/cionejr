"""Output checks are not certificates of drawing quality."""
from pathlib import Path
import unittest
import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
NAMES = ('pixel-art', 'ink-line', 'paper-cut', 'stained-glass', 'blueprint')


class Outputs(unittest.TestCase):
    def test_five_standalone_images_are_valid(self):
        for name in NAMES:
            with self.subTest(style=name):
                path = ROOT / f'{name}.png'
                self.assertTrue(path.exists(), f'Missing {name}')
                with Image.open(path) as image:
                    self.assertEqual(image.size, (1800, 1520))
                    self.assertEqual(image.mode, 'RGB')
                    image.verify()

    def test_styles_are_pairwise_different(self):
        images = [np.asarray(Image.open(ROOT / f'{name}.png').convert('RGB'), dtype=np.int16) for name in NAMES]
        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                mean_gap = np.abs(images[i] - images[j]).mean()
                self.assertGreater(mean_gap, 8, f'{NAMES[i]} and {NAMES[j]} are too alike')

    def test_pixel_art_is_made_of_uniform_blocks(self):
        arr = np.asarray(Image.open(ROOT / 'pixel-art.png').convert('RGB'))
        step = 12
        blocks = arr[:1512].reshape(126, step, 150, step, 3)
        uniform = (blocks == blocks[:, :1, :, :1, :]).all(axis=(1, 3, 4))
        self.assertGreater(uniform.mean(), 0.999)
        colours = {tuple(c) for c in blocks[:, 0, :, 0, :].reshape(-1, 3)}
        self.assertLess(len(colours), 40)

    def test_sheet_and_preview(self):
        for name, size in [('five-styles.png', (3240, 2240)), ('preview.png', (1080, 747))]:
            with self.subTest(name=name):
                with Image.open(ROOT / name) as image:
                    self.assertEqual(image.size, size)
                    image.verify()


if __name__ == '__main__':
    unittest.main()
