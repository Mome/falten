#! /usr/bin/python3

"""Converts bar-bra notation for the side views of cross-folded paper to a 2-dimensional terminal output. Ugly, but probably working version. Works best with a fixed bitmap font like GNU Unifont Mono."""


bottom_left = '╰' #'└'
top_right = '╮' #'┐'
horizontal = '─' #'─'
vertical = '│'
bottom_right = '╯' #'┘'
top_left = '╭' #'┌'
quer_lr = '╱'
quer_rl = '╲'


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
    #bottom = [
    #    ' '*i +
    #    quer_rl*(hl-i) +
    #    quer_lr*(hl-i) +
    #    ''*i
    #    for i in range(hl)
    #]
    #layers += bottom
    #return '\n'.join([''.join(lay) for lay in layers])

    #print('top   ',layers)
    #print('bottom',bottom)
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

            
if __name__ == '__main__':
    import sys
    inp = sys.argv[1]
    for s in inp.split(): 
        output = to_2d_repr(s)
        print(output)
    print()
