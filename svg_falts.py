from collections import namedtuple
from operator import sub
from itertools import cycle

SvgElemement = namedtuple("SvgElement", ['name', 'attr'])


def get_matching_brackets(barbra):
    stack = []
    out = list(range(len(barbra)))
    for i, c in enumerate(barbra):
        if c == '(':
            stack.append(i)
        elif c == ')':
            assert stack, "Non matching closing bracket at index %s!" % i
            j = stack.pop()
            out[i] = j
            out[j] = i

    assert len(stack) == 0, "Too many opening backets!"
    return out


def get_curve(direction, start_i, end_i, w_dist, h_dist):

    assert direction in {'up', 'down'}

    length = end_i - start_i

    end_x = w_dist * length
    end_y = 0

    control_x = end_x / 2
    control_y = h_dist * length

    if (
        (direction == 'up'   and control_y > 0) or
        (direction == 'down' and control_y < 0)
    ):
        control_y *= -1

    return ('q', control_x, control_y, end_x, end_y)


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
    def __init__(self, barbra, width=None, height=None, plate=None):
        assert len(barbra) % 2 == 0, "Length of barbra must be even!!"

        if width == None:
            width = (len(barbra) + 1) * 30

        if height == None:
            height = width

        super().__init__(width, height)

        self.barbra = barbra
        self.plate = plate if (plate != None) else cycle(['black'])

    def draw_lines(self):
        bb = self.barbra
        matching_brackets = get_matching_brackets(bb)
        diffs = tuple(map(sub, matching_brackets, range(len(bb))))
        max_pack_size = max(diffs)
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
            vertical_line = ('v', max_pack_size * h_dist / 2)

            start_i = i
            end_i = len(bb) - start_i - 1
            down_curve = get_curve('down', start_i, end_i, w_dist, h_dist)

            path = [*start_point, *vertical_line, *down_curve]

            while bb[end_i] != '|':

                start_i = end_i
                end_i = matching_brackets[end_i]
                up_curve = get_curve('up', start_i, end_i, w_dist, h_dist)

                start_i = end_i
                end_i = len(bb) - start_i - 1
                down_curve = get_curve('down', start_i, end_i, w_dist, h_dist)

                path += up_curve + down_curve

            path += ('v', -max_pack_size * h_dist / 2)
            self.add('path',
                d = path,
                fill="none",
                stroke=next(self.plate),
                style="stroke-width:7",
            )
            already_done.append(end_i)

    def render(self):
        self.clear()
        self.add('rect', width=self.width, height=self.height, style="fill:white")
        self.draw_lines()
        return super().render()
