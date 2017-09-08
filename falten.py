#! /usr/bin/python3

"""
Converts bar-bra notation for the side views of cross-folded paper to a
2-dimensional terminal output. Ugly, but probably working version. Works best
with a fixed bitmap font like GNU Unifont Mono.
"""

from itertools import cycle

try:
    import colored
except Exception as e:
    print(e)
    print('Install with: ´pip install colored´')


bottom_left = '╰' #'└'
top_right = '╮' #'┐'
horizontal = '─' #'─'
vertical = '│'
bottom_right = '╯' #'┘'
top_left = '╭' #'┌'

corners = (bottom_left, top_right, bottom_right, top_left)
straigts = (horizontal, vertical)


def to_2d_repr(s):
    s = s.replace(';',',')
    blocks = s.split(',')
    pairs = [process_one_block(b) for b in blocks]
    tops, bottoms = zip(*pairs)

    # extend to longest block
    mlen = max([len(t) for t in tops]) + max([len(b) for b in bottoms])
    for top,bot in zip(tops,bottoms):
        extra_layers = [vertical*len(top[0])]*(mlen-len(top)-len(bot))
        #print(top,'add',mlen-len(top))
        top.extend(extra_layers)

    # join bottoms and tops
    block = [t+b for t,b in zip(tops,bottoms)]

    # join rows
    block = [' '.join(row) for row in zip(*block)]

    block = '\n'.join(block)

    return block


def process_one_block(s):
    #print('do_block',s)
    s = s.replace('.','')
    if s == '|':
        return [vertical], [vertical]
    if len(s)%2!=0:
        raise Exception('Not even: '+s)
    s = s.replace('|',vertical)
    s = s.replace('(',top_left)
    s = s.replace(')',top_right)

    layers = []
    construct_layers(s,layers)
    correct_layers(layers)
    layers = [''.join(l) for l in layers]

    hl = len(s)//2
    bottom = [
        vertical*(hl-i-1) +
        bottom_left +
        horizontal*(2*i) +
        bottom_right +
        vertical*(hl-i-1)
        for i in range(hl)
    ]
    return layers, bottom


def correct_layers(layers):
    for i in range(1,len(layers)):
        for j in range(len(layers[i])):
            if layers[i][j]==horizontal:
                if layers[i-1][j] in [vertical,top_left,top_right]:
                    layers[i][j]=vertical




def construct_layers(s, layers, lay_num=0, i=0):
    if lay_num == len(layers):
        layers.append([horizontal]*len(s))
    layer = layers[lay_num]
    while i<len(s):
        if s[i] == vertical:
            layer[i] = vertical
        elif s[i] == top_left:
            layer[i] = top_left
            i = construct_layers(s, layers, lay_num+1, i+1)
            layer[i] = top_right
        elif s[i] == top_right:
            return i
        i+=1

default_plate = "red green yellow blue magenta cyan"

def colorize(pipes, plate=default_plate):
    """Colorizes each individual edge."""

    lines = pipes.split('\n')
    pixels = list(map(list, lines))
    colors = cycle(plate.split())
    already_colored = []

    for i, segment in enumerate(lines[0]):
        if (segment == vertical) and (i not in already_colored):
            direction = 'down'
            color = next(colors)
            y = 0
            x = i
            while y >= 0:
                segment = pixels[y][x]
                pixels[y][x] = colored.fg(color) + segment + colored.attr('reset')

                if segment == top_left:
                    if direction == 'up':
                        direction = 'right'
                    if direction == 'left':
                        direction = 'down'
                if segment == top_right:
                    if direction == 'up':
                        direction = 'left'
                    if direction == 'right':
                        direction = 'down'
                if segment == bottom_left:
                    if direction == 'down':
                        direction = 'right'
                    if direction == 'left':
                        direction = 'up'
                if segment == bottom_right:
                    if direction == 'down':
                        direction = 'left'
                    if direction == 'right':
                        direction = 'up'

                if direction == 'down':
                    y += 1
                elif direction == 'up':
                    y -= 1
                elif direction == 'right':
                    x += 1
                elif direction == 'left':
                    x -= 1

                #print(segment, direction, color, x, y)

            already_colored.append(x)

    return '\n'.join(''.join(line) for line in pixels)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Converts bar-bra notation for the side views of cross-folded paper to a2-dimensional terminal output.")
    parser.add_argument('--plate', '-p', metavar="str",
        default=default_plate,
        help="Space separated string of colors.")
    parser.add_argument('barbra', nargs='+',
        help="Cross-fold in bar-bra notation.")
    args = parser.parse_args()

    for bb in args.barbra:
        falt_2d_str = to_2d_repr(bb)
        if args.plate:
            falt_2d_str = colorize(falt_2d_str, args.plate)
        print(falt_2d_str)

def print_colors():
    names = (n.lower() for n in colored.names)
    print(' '.join(colored.fg(n) + n + colored.attr('reset') for n in names))

if __name__ == '__main__':
    main()
