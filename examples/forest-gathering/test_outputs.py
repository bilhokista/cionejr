"""Output checks are not certificates of drawing or viewer comprehension."""
from pathlib import Path
import importlib.util
import unittest
from PIL import Image

ROOT = Path(__file__).parent

class Outputs(unittest.TestCase):
    def test_ground_grass_excludes_character_areas(self):
        spec = importlib.util.spec_from_file_location('forest_renderer',ROOT/'render.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module,'grass_allowed'), 'Grass exclusion not implemented')
        for point in ((300,760),(682,745),(150,970),(550,1070),(550,640),(500,860)):
            self.assertFalse(module.grass_allowed(*point),point)
        for point in ((300,1180),(820,960),(205,1080)):
            self.assertTrue(module.grass_allowed(*point),point)

    def test_ground_protection_follows_shapes_not_bounding_boxes(self):
        spec = importlib.util.spec_from_file_location('forest_renderer',ROOT/'render.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Inside the old rectangles but clear of every animal and prop.
        for point in ((130,800),(420,1115),(690,1110)):
            self.assertTrue(module.grass_allowed(*point),point)
        # Just outside a contour: the margin still keeps marks off the silhouette.
        for point in ((409,1051),(430,900)):
            self.assertFalse(module.grass_allowed(*point),point)
        # Ears, paws and the stump rim stay protected.
        for point in ((650,520),(430,820),(623,815),(525,826)):
            self.assertFalse(module.grass_allowed(*point),point)

    def test_full_page_exists_and_has_requested_ratio(self):
        path = ROOT/'forest-gathering.png'
        self.assertTrue(path.exists(), 'Full illustration not rendered')
        with Image.open(path) as image:
            self.assertEqual(image.size,(2400,3000))
            self.assertEqual(image.mode,'RGB')
            image.verify()

    def test_preview_and_composition_exist(self):
        for name,size in [('preview.png',(600,750)),('composition.png',(1000,1250))]:
            with self.subTest(name=name):
                path = ROOT/name
                self.assertTrue(path.exists(), f'{name} not rendered')
                with Image.open(path) as image:
                    self.assertEqual(image.size,size)
                    image.verify()

    def test_page_is_full_bleed_not_a_white_canvas_with_inset(self):
        path = ROOT/'forest-gathering.png'
        self.assertTrue(path.exists(), 'Full illustration not rendered')
        with Image.open(path) as image:
            for xy in ((0,0),(2399,0),(0,2999),(2399,2999)):
                self.assertLess(max(image.getpixel(xy)),245)

if __name__=='__main__':
    unittest.main()
