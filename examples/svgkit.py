"""A small SVG builder shared by the examples.

The SVG is the master file. PNGs are rendered from it with resvg, so the vector
and raster outputs cannot drift apart. Coordinates are design units (the SVG
viewBox); the PNG size is chosen when rendering.

Path commands use the same tuples as the raster code: ('M', p), ('L', p),
('C', p1, p2, p3), plus ('Z',) to close.
"""
from contextlib import contextmanager
import math
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

NS = 'http://www.w3.org/2000/svg'


def num(value, places=2):
    """Compact number: at most `places` decimals, no trailing zeros."""
    text = f'{value:.{places}f}'.rstrip('0').rstrip('.')
    return '0' if text in ('-0', '') else text


def path_data(commands):
    parts = []
    for kind, *points in commands:
        if kind == 'Z':
            parts.append('Z')
        else:
            coords = ' '.join(f'{num(x)} {num(y)}' for x, y in points)
            parts.append(f'{kind}{coords}')
    return ''.join(parts)


def luminance_grey(colour):
    """Grey of the same lightness, used for layout renders."""
    value = colour.lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    grey = round(.299 * r + .587 * g + .114 * b)
    return f'#{grey:02x}{grey:02x}{grey:02x}'


class Drawing:
    def __init__(self, width, height, background=None, title=None, description=None):
        self.width, self.height = width, height
        self.background = background
        self.title, self.description = title, description
        self.defs = []
        self.body = []
        self._stack = [self.body]
        self._ids = set()
        self.greyscale = False

    # -- structure ---------------------------------------------------------
    def _emit(self, element):
        self._stack[-1].append(element)

    def _unique(self, prefix):
        index = 1
        while f'{prefix}{index}' in self._ids:
            index += 1
        self._ids.add(f'{prefix}{index}')
        return f'{prefix}{index}'

    def _colour(self, colour):
        if colour is None:
            return 'none'
        if colour.startswith('url(') or colour == 'none':
            return colour
        return luminance_grey(colour) if self.greyscale else colour

    @contextmanager
    def group(self, ident=None, transform=None, opacity=None, clip=None, filter=None, **attrs):
        children = []
        self._stack.append(children)
        try:
            yield
        finally:
            self._stack.pop()
        parts = []
        if ident:
            parts.append(f'id={quoteattr(ident)}')
        if transform:
            parts.append(f'transform={quoteattr(transform)}')
        if opacity is not None:
            parts.append(f'opacity="{num(opacity)}"')
        if clip:
            parts.append(f'clip-path="url(#{clip})"')
        if filter:
            parts.append(f'filter="url(#{filter})"')
        for key, value in attrs.items():
            parts.append(f'{key.replace("_", "-")}={quoteattr(str(value))}')
        self._emit(f'<g {" ".join(parts)}>' + ''.join(children) + '</g>')

    # -- definitions -------------------------------------------------------
    def clip_path(self, commands, ident=None):
        """Clip to one path, or to the union of several (pass a list of command lists)."""
        ident = ident or self._unique('clip')
        shapes = commands if commands and isinstance(commands[0], list) else [commands]
        body = ''.join(f'<path d="{path_data(shape)}"/>' for shape in shapes)
        self.defs.append(f'<clipPath id={quoteattr(ident)}>{body}</clipPath>')
        return ident

    def linear_gradient(self, stops, x1=0, y1=0, x2=0, y2=1, ident=None, units='objectBoundingBox'):
        ident = ident or self._unique('lin')
        body = ''.join(f'<stop offset="{num(o)}" stop-color="{self._colour(c)}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id={quoteattr(ident)} gradientUnits="{units}" '
                         f'x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}">{body}</linearGradient>')
        return f'url(#{ident})'

    def radial_gradient(self, stops, cx=.5, cy=.5, r=.5, ident=None, units='objectBoundingBox'):
        """stops: (offset, colour) or (offset, colour, opacity)."""
        ident = ident or self._unique('rad')
        pieces = []
        for stop in stops:
            opacity = f' stop-opacity="{num(stop[2])}"' if len(stop) > 2 else ''
            pieces.append(f'<stop offset="{num(stop[0])}" stop-color="{self._colour(stop[1])}"{opacity}/>')
        self.defs.append(f'<radialGradient id={quoteattr(ident)} gradientUnits="{units}" '
                         f'cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}">{"".join(pieces)}</radialGradient>')
        return f'url(#{ident})'

    def raw_def(self, markup):
        self.defs.append(markup)

    # -- shapes ------------------------------------------------------------
    def _style(self, fill, stroke, width, cap, join, dash, opacity, extra):
        parts = [f'fill="{self._colour(fill)}"']
        if stroke:
            parts.append(f'stroke="{self._colour(stroke)}" stroke-width="{num(width)}"')
            parts.append(f'stroke-linecap="{cap}" stroke-linejoin="{join}"')
            if dash:
                parts.append(f'stroke-dasharray="{" ".join(num(d) for d in dash)}"')
        if opacity is not None:
            parts.append(f'opacity="{num(opacity)}"')
        for key, value in extra.items():
            parts.append(f'{key.replace("_", "-")}={quoteattr(str(value))}')
        return ' '.join(parts)

    def path(self, commands, fill=None, stroke=None, width=1, cap='round', join='round', dash=None,
             opacity=None, ident=None, **extra):
        ident_attr = f' id={quoteattr(ident)}' if ident else ''
        style = self._style(fill, stroke, width, cap, join, dash, opacity, extra)
        self._emit(f'<path{ident_attr} d="{path_data(commands)}" {style}/>')

    def polygon(self, points, **kwargs):
        commands = [('M', points[0])] + [('L', p) for p in points[1:]] + [('Z',)]
        self.path(commands, **kwargs)

    def polyline(self, points, stroke, width=1, **kwargs):
        self.path([('M', points[0])] + [('L', p) for p in points[1:]], fill=None, stroke=stroke, width=width, **kwargs)

    def line(self, a, b, stroke, width=1, **kwargs):
        self.polyline([a, b], stroke, width, **kwargs)

    def ellipse(self, cx, cy, rx, ry, fill=None, stroke=None, width=1, opacity=None, ident=None, **extra):
        ident_attr = f' id={quoteattr(ident)}' if ident else ''
        style = self._style(fill, stroke, width, 'round', 'round', None, opacity, extra)
        self._emit(f'<ellipse{ident_attr} cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx)}" ry="{num(ry)}" {style}/>')

    def circle(self, cx, cy, r, **kwargs):
        self.ellipse(cx, cy, r, r, **kwargs)

    def rect(self, x, y, w, h, fill=None, stroke=None, width=1, opacity=None, **extra):
        style = self._style(fill, stroke, width, 'butt', 'miter', None, opacity, extra)
        self._emit(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" {style}/>')

    def text(self, x, y, content, size, fill, anchor='start', family='DejaVu Sans, Verdana, sans-serif', **extra):
        extras = ''.join(f' {k.replace("_", "-")}={quoteattr(str(v))}' for k, v in extra.items())
        self._emit(f'<text x="{num(x)}" y="{num(y)}" font-size="{num(size)}" fill="{self._colour(fill)}" '
                   f'text-anchor="{anchor}" font-family={quoteattr(family)}{extras}>{escape(content)}</text>')

    # -- output ------------------------------------------------------------
    def to_svg(self):
        w, h = num(self.width, 4), num(self.height, 4)
        head = f'<svg xmlns="{NS}" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        meta = ''
        if self.title:
            meta += f'<title>{escape(self.title)}</title>'
        if self.description:
            meta += f'<desc>{escape(self.description)}</desc>'
        defs = f'<defs>{"".join(self.defs)}</defs>' if self.defs else ''
        ground = ''
        if self.background:
            # One unit of bleed on every side so rounding in the PNG scale never leaves a transparent edge.
            ground = (f'<rect x="-1" y="-1" width="{num(self.width + 2)}" height="{num(self.height + 2)}" '
                      f'fill="{self._colour(self.background)}"/>')
        return head + meta + defs + ground + ''.join(self.body) + '</svg>\n'

    def save(self, path):
        Path(path).write_text(self.to_svg(), encoding='utf-8', newline='\n')


def render_png(svg_text, width, height, path=None):
    """Rasterize SVG text with resvg; returns the PNG bytes and optionally writes them."""
    import resvg_py
    data = bytes(resvg_py.svg_to_bytes(svg_string=svg_text, width=width, height=height))
    if path is not None:
        Path(path).write_bytes(data)
    return data


def ribbon(points, widths):
    """Closed outline of a variable-width stroke following `points`."""
    left, right = [], []
    for i, (x, y) in enumerate(points):
        a = points[max(0, i - 1)]
        b = points[min(len(points) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        half = widths[i] / 2
        left.append((x + nx * half, y + ny * half))
        right.append((x - nx * half, y - ny * half))
    return left + right[::-1]
