from itertools import cycle

try:
    import colored
    TERMINAL_COLOR_AVAILABLE = True
except Exception as e:
    print(e)
    print('Terminal coloring not available!')
    print('Install with: ´pip install colored´')
    TERMINAL_COLOR_AVAILABLE = False
    
default_palette = ("red green yellow blue magenta cyan light_red light_green "
    + "light_yellow light_blue light_magenta light_cyan dark_gray light_gray")
  
bottom_left = '╰' #'└'
top_right = '╮' #'┐'
horizontal = '─'
vertical = '│'
bottom_right = '╯' #'┘'
top_left = '╭' #'┌'

def to_2d_repr(s):
    s = s.replace('.', ',')
    s = s.replace(';', ',')
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
    block = [t + b for t, b in zip(tops, bottoms)]

    # join rows
    block = [' '.join(row) for row in zip(*block)]

    block = '\n'.join(block)

    return block

def process_one_block(s):
    s = s.replace('.','')
    if s == '|':
        return [vertical], [vertical]
    if len(s) % 2 != 0:
        raise Exception('Not even: ' + s)
    s = s.replace('|', vertical)
    s = s.replace('(', top_left)
    s = s.replace(')', top_right)

    layers = []
    construct_layers(s, layers)
    correct_layers(layers)
    layers = [''.join(l) for l in layers]

    hl = len(s) // 2
    bottom = [
        vertical * (hl - i - 1) +
        bottom_left +
        horizontal * (2 * i) +
        bottom_right +
        vertical * (hl - i - 1)
        for i in range(hl)
    ]
    return layers, bottom

def correct_layers(layers):
    for i in range(1,len(layers)):
        for j in range(len(layers[i])):
            if layers[i][j] == horizontal:
                if layers[i-1][j] in [vertical,top_left,top_right]:
                    layers[i][j] = vertical


def construct_layers(s, layers, lay_num=0, i=0):
    if lay_num == len(layers):
        layers.append([horizontal] * len(s))
    layer = layers[lay_num]
    while i<len(s):
        if s[i] == vertical:
            layer[i] = vertical
        elif s[i] == top_left:
            layer[i] = top_left
            i = construct_layers(s, layers, lay_num + 1, i + 1)
            layer[i] = top_right
        elif s[i] == top_right:
            return i
        i+=1


def _next_direction(segment, direction):
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

    return direction


def colorize(pipes, palette, background=False):
    """Colorizes each individual edge."""
    
    if palette == None:
        palette = default_palette

    palette = cycle(palette.split())

    if background:
        color_func = colored.bg
    else:
        color_func = colored.fg

    lines = pipes.split('\n')
    pixels = list(map(list, lines))
    already_colored = []

    for i, segment in enumerate(lines[0]):
        if (segment != vertical) or (i in already_colored):
            continue
        direction = 'down'
        color = next(palette)
        y = 0
        x = i
        while 0 <= y < len(lines):
            segment = pixels[y][x]
            pixel = color_func(color)
            pixel += segment + colored.attr('reset')
            pixels[y][x] = pixel

            direction = _next_direction(segment, direction)

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


def print_colors():
    names = (n.lower() for n in colored.names)
    print(' '.join(colored.fg(n) + n + colored.attr('reset') for n in names))
