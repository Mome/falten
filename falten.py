#! /usr/bin/env python3

"""
Converts bar-bra notation for the side views of cross-folded paper to a
2-dimensional terminal output. Ugly, but probably working version. Works best
with a fixed bitmap font like GNU Unifont Mono.
"""

from itertools import cycle, chain

from barbra import BarBra

default_palette_unicode = ("red green yellow blue magenta cyan light_red light_green "
    + "light_yellow light_blue light_magenta light_cyan dark_gray light_gray")

default_palette_svg = "blue red green purple orange limegreen magenta cyan brown black"



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

    falt_iter = (string.split() for string in args.barbra)
    falt_iter = filter(bool, chain(*falt_iter))

    if args.palette == None:
        palette = default_palette_svg if args.svg else default_palette_unicode
    else:
        palette = args.palette

    palette = cycle(palette.split())

    for barbra_str in falt_iter: # this iterates the input lines
        bb = BarBra(barbra_str)

        if args.svg:
            output = bb.render_svg(palette)
        else:
            output = bb.render_unicode(palette, args.invert_bg)

        print(output)


if __name__ == '__main__':
    main()
