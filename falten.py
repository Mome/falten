#! /usr/bin/env python3

"""
Converts bar-bra notation for the side views of cross-folded paper to a
2-dimensional terminal output. Ugly, but probably working version. Works best
with a fixed bitmap font like GNU Unifont Mono.
"""

from itertools import cycle, chain

from barbra import BarBra


def numlist2barbra(numlist, allow_mixed=True):
    """Converts list of number into Barbra str."""

    def _n2b(n):
        try:
            n = int(n)
        except ValueError:
            if allow_mixed and (type(n) == str):
                return n
            else:
                raise
        if n == 0:
            out = "|"
        elif n == 1:
            out = "()"
        else:
            out = "(" + _n2b(n-1) + ")"
        return out

    bb = map(_n2b, numlist)
    bb = map(str, bb)
    bb = "".join(bb)
    return bb


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description = "Converts bar-bra notation for the side views of cross-folded paper to a 2-dimensional terminal output. For color options look at: github.com/dslackw/colored",
        epilog = 'Example: python falten.py -p "cyan magenta blue" "||.||().||.||()||()"',
    )
    parser.add_argument('--palette', '-p',
        metavar = "str",
        help = "Space separated string of colors.",
    )
    parser.add_argument('--invert-bg',
        action = 'store_true',
        help = "Color background instead of foreground.",
    )
    parser.add_argument('--svg',
        action = 'store_true',
        help = "Reder output as SVG. (experimental feature)",
    )
    parser.add_argument('barbra',
        nargs = '*',
        default = sys.stdin,
        help = "Cross-fold in bar-bra notation.",
    )
    args = parser.parse_args()

    # this part is for piping
    if args.barbra == sys.stdin:
        args.barbra = args.barbra.readlines()

    falt_iter = (bbstr.split() for bbstr in args.barbra)
    falt_iter = filter(bool, chain(*falt_iter))
    falt_iter = map(numlist2barbra, falt_iter) # convert numbers into BarBra

    for barbra_str in falt_iter: # this iterates the input lines
        bb = BarBra(barbra_str)

        if args.svg:
            output = bb.render_svg(args.palette)
        else:
            output = bb.render_unicode(args.palette, args.invert_bg)

        print(output)


if __name__ == '__main__':
    main()
