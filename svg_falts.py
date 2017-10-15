from collections import namedtuple
from operator import sub
from itertools import cycle

SvgElemement = namedtuple("SvgElement", ['name', 'attr'])




class SvgImage():
    def __init__(self, width, height):
        """
        Simple SVG image implementation.

        SVG-Path:
        ---------
          M = moveto
          L = lineto
          H = horizontal lineto
          V = vertical lineto
          C = curveto
          S = smooth curveto
          Q = quadratic Bézier curve
          T = smooth quadratic Bézier curveto
          A = elliptical Arc
          Z = closepath

        """
        self.width = width
        self.height = height
        self.elements = []

    def clear(self):
        self.elements = []

    def add(self, name, **kwargs):
        if 'd' in kwargs:
            d = kwargs['d']
            if type(d) != str:
                d = map(str, d)
                d = " ".join(d)
            kwargs['d'] = d
        self.elements.append(SvgElemement(name, kwargs))

    def render(self):
        first = '<svg width="%s" height="%s">' % (self.width, self.height)
        last = "</svg>"
        middle = []

        for name, attr in self.elements:
            attr = ['%s="%s"' % kw for kw in attr.items()]
            line = ['<' + name, *attr, '/>']
            middle.append(" ".join(line))

        lines = [first, *middle, last]

        return "\n".join(lines)

    def save(self, name):
        svg_code = self.render()
        with open(name, 'w') as f:
            f.write(svg_code)

    def _repr_html_(self):
        return self.render()


class SvgFold(SvgImage):

    H_CURVE_STRETCH = 1.2

    def __init__(self, barbra, width=None, height=None, palette=None):

        if width == None:
            width = (len(barbra) + 1) * 30

        if height == None:
            height = width

        super().__init__(width, height)

        self.barbra = barbra
        self.palette = palette if (palette != None) else cycle(['black'])

    def draw_lines(self):
        bb = self.barbra
        max_pack_size = max(bb.pack_sizes)
        w_dist = self.width / (len(bb) + 1)
        layers = (max_pack_size + len(bb)) / 2 + 1
        h_dist = self.height / (layers + 1)
        middle_y = (max_pack_size / 2 + 1) * h_dist
        #print('diffs:', diffs)
        #print('w_dist', w_dist, 'h_dist', h_dist, 'middle_y', middle_y)

        already_done = []
        for i, b in enumerate(bb):

            if b != '|':
                continue
            if i in already_done:
                continue

            start_point = ('M', w_dist * (i + 1), h_dist)
            vertical_line = ('v', max_pack_size * h_dist / (2*bb.pack_sizes[i]))

            start_i = i
            end_i = len(bb) - start_i - 1
            width = (end_i - start_i) * w_dist
            height = (end_i - start_i) * h_dist * self.H_CURVE_STRETCH
            down_curve = SvgFold.get_curve('down', width, height)

            path = [*start_point, *vertical_line, *down_curve]

            while bb[end_i] != '|':

                start_i = end_i
                end_i = bb.ambi[end_i]
                width = (end_i - start_i) * w_dist
                h_pack_strech = max_pack_size / bb.pack_sizes[start_i]
                height = (end_i - start_i) * h_dist * h_pack_strech * self.H_CURVE_STRETCH
                up_curve = SvgFold.get_curve('up', width, height)

                start_i = end_i
                end_i = len(bb) - start_i - 1
                width = (end_i - start_i) * w_dist
                height = (end_i - start_i) * h_dist * self.H_CURVE_STRETCH
                down_curve = SvgFold.get_curve('down', width, height)

                path += up_curve + down_curve

            path += ('v', -max_pack_size * h_dist / (2*bb.pack_sizes[end_i]))
            self.add('path',
                d = path,
                fill="none",
                stroke=next(self.palette),
                style="stroke-width:7",
            )
            already_done.append(end_i)

    def render(self):
        self.clear()
        #self.add('rect', width=self.width, height=self.height, style="fill:white")
        self.draw_lines()
        return super().render()

    @staticmethod
    def get_curve(direction, width, height):
        assert direction in {'up', 'down'}

        end_x = width
        end_y = 0

        control_x = end_x / 2
        control_y = height

        if (
            (direction == 'up'   and control_y > 0) or
            (direction == 'down' and control_y < 0)
        ):
            control_y *= -1

        return ('q', control_x, control_y, end_x, end_y)
