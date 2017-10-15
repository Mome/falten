from svg_falts import SvgFold
from unicode_falts import to_2d_repr, TERMINAL_COLOR_AVAILABLE, colorize

class BarBra(str):

    def __init__(self, barbra_str, sep=';'):
        assert len(barbra_str) % 2 == 0, "Length of barbra must be even!!"

        # absolute and relative matching bracket indices
        self._ambi = BarBra._get_matching_brackets(barbra_str)
        self._rmbi = tuple((self.ambi[i] - i) for i in range(len(barbra_str)))

        # local maximum pack sizes
        self._pack_sizes = BarBra._get_pack_sizes(self.rmbi)

        self.sep = sep

    @property
    def ambi(self):
        return self._ambi

    @property
    def rmbi(self):
        return self._rmbi

    @property
    def pack_sizes(self):
        return self._pack_sizes

    """def __repr__(self):
        return "{cls_}['{bb}']".format(
            cls_ = self.__class__.__name__,
            bb = str(self),
        )"""

    @staticmethod
    def _get_pack_sizes(rmbi):
        lmps = 0
        pack_sizes = []
        for ri in rmbi:

            if lmps == 0:
                lmps = ri

            pack_sizes.append(lmps + 1)

            if ri == -lmps:
                lmps = 0

        return tuple(pack_sizes)

    @staticmethod
    def _get_matching_brackets(barbra_str):
        stack = []
        out = list(range(len(barbra_str)))
        for i, c in enumerate(barbra_str):
            if c == '(':
                stack.append(i)
            elif c == ')':
                assert stack, "Non matching closing bracket at index %s!" % i
                j = stack.pop()
                out[i] = j
                out[j] = i

        assert len(stack) == 0, "Too many opening backets!"
        return tuple(out)

    def render_svg(self, palette):
        return SvgFold(self, palette=palette).render()

    def render_unicode(self, palette, invert_bg):
        falt_2d_str = to_2d_repr(self)
        if palette and TERMINAL_COLOR_AVAILABLE:
            falt_2d_str = colorize(falt_2d_str, palette, invert_bg)
        return falt_2d_str

    def _repr_html_(self, palette):
        return self.render_svg(palette)
