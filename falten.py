#! /usr/bin/env python3

"""
Converts bar-bra notation for the side views of cross-folded paper to a
2-dimensional terminal output. Ugly, but probably working version. Works best
with a fixed bitmap font like GNU Unifont Mono.
"""

from itertools import cycle, chain

from svg_falts import SvgFold
from unicode_falts import to_2d_repr, color_available, colorize


default_plate_unicode = ("red green yellow blue magenta cyan light_red light_green "
    + "light_yellow light_blue light_magenta light_cyan dark_gray light_gray")

default_plate_svg = "blue red green purple orange limegreen magenta cyan brown black"

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description = "Converts bar-bra notation for the side views of cross-folded paper to a 2-dimensional terminal output. For color options look at: github.com/dslackw/colored",
        epilog = 'Example: python falten.py -p "cyan magenta blue" "||.||().||.||()||()"',
    )
    parser.add_argument('--plate', '-p',
        metavar = "str",
        help = "Space separated string of colors.",
    )
    parser.add_argument('-b', '--background',
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

    falt_iter = (string.split() for string in args.barbra)
    falt_iter = filter(bool, chain(*falt_iter))

    if args.plate == None:
        plate = default_plate_svg if args.svg else default_plate_unicode
    else:
        plate = args.plate

    plate = cycle(plate.split())

    if args.svg:
        for bb in falt_iter:
            img = SvgFold(bb, plate=plate)
            svg_code = img.render()
            print(svg_code)
    else:
        for bb in falt_iter:
            falt_2d_str = to_2d_repr(bb)
            if plate and color_available:
                falt_2d_str = colorize(falt_2d_str, plate, args.background)
            print(falt_2d_str, end='\n')


if __name__ == '__main__':
    main()
