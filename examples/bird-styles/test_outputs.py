from pathlib import Path
import unittest
from PIL import Image, ImageChops

ROOT = Path(__file__).parent
NAMES = ('geometric', 'linocut', 'gouache')

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
        self.assertTrue((ROOT/'three-styles.png').exists(), 'Sheet not rendered')
        with Image.open(ROOT/'three-styles.png') as sheet:
            background = sheet.getpixel((0,0))
        for name in NAMES:
            with Image.open(ROOT/f'{name}.png') as image:
                self.assertEqual(image.getpixel((0,0)),background,
                                 f'{name} creates an unintended panel rectangle')

    def test_sheet_and_small_preview(self):
        for name,size in [('three-styles.png',(3240,1440)),('preview.png',(1080,480)),
                          ('construction.png',(1800,1520))]:
            with self.subTest(name=name):
                path = ROOT / name
                self.assertTrue(path.exists(), f'Missing {name}')
                with Image.open(path) as image:
                    self.assertEqual(image.size,size)
                    image.verify()

if __name__ == '__main__':
    unittest.main()
