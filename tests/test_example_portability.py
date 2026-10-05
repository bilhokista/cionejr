from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExamplePortability(unittest.TestCase):
    def test_bird_label_font_loads_without_platform_path(self):
        spec = importlib.util.spec_from_file_location('bird_renderer',ROOT/'examples/bird-styles/render.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module,'choose_label_font'), 'Portable label font not implemented')
        font = module.choose_label_font(36)
        box = font.getbbox('Geometric')
        self.assertGreater(box[2]-box[0],0)
        self.assertGreater(box[3]-box[1],0)


if __name__=='__main__':
    unittest.main()
