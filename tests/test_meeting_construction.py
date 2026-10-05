"""Narrow construction regressions, not an artistic-quality benchmark."""
from copy import deepcopy
import importlib.util
import inspect
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'
spec = importlib.util.spec_from_file_location('meeting_construction', ROOT / 'examples/forest-meeting/render.py')
meeting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meeting)


def mask(svg):
    data = meeting.kit.render_png(svg, 1000, 1250)
    return np.asarray(Image.open(BytesIO(data)).convert('RGBA'))[:, :, 3] > 40


def selected_mask(root, predicate):
    """Keep a selected shape and its transforms/defs, without the other paint."""
    def prune(element):
        if predicate(element) or element.tag == NS + 'defs':
            return deepcopy(element)
        kept = [result for child in element if (result := prune(child)) is not None]
        if not kept:
            return None
        result = deepcopy(element)
        result[:] = kept
        return result

    result = prune(root)
    if result is None:
        raise AssertionError('Required shape not found')
    return mask(ET.tostring(result, encoding='unicode'))


class MassLayout(unittest.TestCase):
    def test_layout_only_does_not_overwrite_the_finished_art(self):
        self.assertIn('argv', inspect.signature(meeting.main).parameters,
                      'The renderer needs a layout-only command before finishing')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / 'forest-meeting.png'
            final.write_bytes(b'preserved final')
            with patch.object(meeting, 'ROOT', root):
                meeting.main(['--layout'])
            self.assertEqual(final.read_bytes(), b'preserved final')
            self.assertTrue((root / 'layout.svg').exists())
            with Image.open(root / 'composition.png') as image:
                self.assertEqual(image.size, (1000, 1250))

    def test_layout_has_a_separate_mass_builder(self):
        self.assertTrue(callable(getattr(meeting, 'layout_scene', None)),
                        'A desaturated finished illustration is not a mass layout')
        root = ET.fromstring(meeting.layout_scene().to_svg())
        ids = {element.get('id') for element in root.iter()}
        self.assertTrue({'owl', *meeting.CAST} <= ids)
        self.assertIn('layout-masses', ids)
        for material in ('owl-leaf', 'hedgehog-quills', 'grass', 'mushrooms', 'canopy'):
            self.assertNotIn(material, ids)


class CharacterContact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.squirrel = meeting.scene(only=['squirrel'], with_background=False).to_svg()
        cls.owl = ET.fromstring(meeting.scene(only=['owl'], with_background=False).to_svg())

    def test_squirrel_head_is_connected_to_its_body(self):
        root = ET.fromstring(self.squirrel)
        head = selected_mask(root, lambda el: el.get('id') == 'squirrel-head')
        body = selected_mask(root, lambda el: el.get('id') == 'squirrel-body')
        silhouette = Image.fromarray(mask(self.squirrel).astype('uint8') * 255).copy()
        y, x = np.argwhere(head)[len(np.argwhere(head)) // 2]
        ImageDraw.floodfill(silhouette, (int(x), int(y)), 128)
        connected = np.asarray(silhouette) == 128
        self.assertGreater((connected & body).sum() / body.sum(), .95,
                           'The head must reach the body through a visible neck/shoulder')

    def test_owl_grip_overlaps_the_leaf(self):
        leaf = selected_mask(self.owl, lambda el: el.get('id') == 'owl-leaf')
        grip = selected_mask(self.owl, lambda el: el.tag == NS + 'ellipse' and el.get('fill') == '#caa36a')
        self.assertGreater(int((leaf & grip).sum()), 5,
                           'A nearby paw does not hold the leaf; their paint must meet')

    def test_owl_grip_remains_attached_to_a_wing(self):
        wing = selected_mask(self.owl, lambda el: el.get('fill') == '#6b4e36')
        grip = selected_mask(self.owl, lambda el: el.tag == NS + 'ellipse' and el.get('fill') == '#caa36a')
        self.assertGreater(int((wing & grip).sum()), 5)


if __name__ == '__main__':
    unittest.main()
