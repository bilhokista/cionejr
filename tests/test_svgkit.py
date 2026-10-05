from pathlib import Path
import importlib.util
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('svgkit', ROOT / 'examples' / 'svgkit.py')
svgkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svgkit)


class SvgKit(unittest.TestCase):
    def test_path_data_keeps_cubic_curves(self):
        data = svgkit.path_data([('M', (1, 2)), ('C', (3, 4), (5, 6), (7.5, 8)), ('L', (0, 0)), ('Z',)])
        self.assertEqual(data, 'M1 2C3 4 5 6 7.5 8L0 0Z')

    def test_numbers_are_compact(self):
        self.assertEqual(svgkit.num(3.0), '3')
        self.assertEqual(svgkit.num(3.14159), '3.14')
        self.assertEqual(svgkit.num(-0.001), '0')

    def test_document_is_well_formed_and_has_the_requested_structure(self):
        d = svgkit.Drawing(100, 80, background='#fff', title='Test <&>')
        d.path([('M', (0, 0)), ('L', (10, 0)), ('L', (10, 10))], fill='#123456', ident='tri')
        with d.group(ident='moved', transform='translate(5 5)'):
            d.circle(5, 5, 3, fill='#ff0000')
        d.text(1, 2, 'a & b', 10, '#000')
        root = ET.fromstring(d.to_svg())
        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
        self.assertEqual(root.get('viewBox'), '0 0 100 80')
        ids = {el.get('id') for el in root.iter() if el.get('id')}
        self.assertTrue({'tri', 'moved'} <= ids)
        self.assertEqual(root.find('{http://www.w3.org/2000/svg}title').text, 'Test <&>')

    def test_gradients_and_clips_are_defined_once_and_referenced(self):
        d = svgkit.Drawing(10, 10)
        fill = d.linear_gradient([(0, '#fff'), (1, '#000')])
        clip = d.clip_path([('M', (0, 0)), ('L', (5, 0)), ('L', (5, 5)), ('Z',)])
        with d.group(clip=clip):
            d.rect(0, 0, 10, 10, fill=fill)
        svg = d.to_svg()
        self.assertIn(fill, svg)
        self.assertIn(f'clip-path="url(#{clip})"', svg)
        ET.fromstring(svg)

    def test_greyscale_mode_keeps_lightness_and_removes_hue(self):
        d = svgkit.Drawing(10, 10)
        d.greyscale = True
        d.rect(0, 0, 5, 5, fill='#ff0000')
        self.assertIn('fill="#4c4c4c"', d.to_svg())

    def test_colour_map_recolours_fills_strokes_and_gradient_stops(self):
        d = svgkit.Drawing(10, 10)
        d.colour_map = lambda colour: '#00ff00'
        d.rect(0, 0, 5, 5, fill='#ff0000', stroke='#0000ff')
        fill = d.linear_gradient([(0, '#111111'), (1, '#eeeeee')])
        d.rect(0, 5, 5, 5, fill=fill)
        svg = d.to_svg()
        self.assertNotIn('#ff0000', svg)
        self.assertNotIn('#0000ff', svg)
        self.assertNotIn('#111111', svg)
        self.assertIn('fill="#00ff00"', svg)

    def test_render_png_uses_the_requested_size(self):
        d = svgkit.Drawing(100, 50, background='#336699')
        d.circle(50, 25, 20, fill='#ffffff')
        data = svgkit.render_png(d.to_svg(), 200, 100)
        self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
        from io import BytesIO
        from PIL import Image
        with Image.open(BytesIO(data)) as image:
            self.assertEqual(image.size, (200, 100))
            self.assertEqual(image.getpixel((100, 50))[:3], (255, 255, 255))
            self.assertEqual(image.getpixel((2, 2))[:3], (51, 102, 153))

    def test_ribbon_width_follows_widths(self):
        outline = svgkit.ribbon([(0, 0), (10, 0), (20, 0)], [2, 6, 2])
        ys = sorted(y for _, y in outline)
        self.assertAlmostEqual(ys[0], -3)
        self.assertAlmostEqual(ys[-1], 3)


if __name__ == '__main__':
    unittest.main()
