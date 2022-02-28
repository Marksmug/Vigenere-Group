from typing import List, Tuple
import sys


def result(matrix , dinner, t, e, index):

    for i in range(e):
        for j in range(i*t, (i+1)*t):
            if dinner[j] > 0:
                matrix[i][j%t].append(index+1)





if __name__ == '__main__':

    try:
        d = int(sys.argv[1])
        c = int(sys.argv[2])
        e = int(sys.argv[3])
    except IndexError:
        print('Usage: python3 cruDesPrint d c e')

    with open("out.dimacs", "r") as f:
        lines = f.readlines()


    input = lines[1]

    t = int(d/c)
    n = d*t*e

    list = []
    i = 0
    j = 0
    matrix = [[[] for j in range(t)] for i in range(e)]
    while i < len(input):
        str = ''
        while i < len(input) and input[i] != ' ':
            str = str + input[i]
            i = i + 1
        list.append(int(str))
        i = i + 1

    list = list[:n]
    diner = []
    index = 0
    for i in range(len(list)):
        if i ==0 or i%(t*e) != 0:
            diner.append(list[i])
        else:
            result(matrix, diner, t, e, index)
            index = index + 1
            diner = []
            diner.append(list[i])

    result(matrix, diner, t, e, index)

    #print design
    #for i in range(e):
    #    print(matrix[i])

    #output design file
    with open('cruDes.txt', 'w') as f:
        f.write(f'{d} {c} {e}')
        f.write('\n')
        for i in range(e):
            for j in range(t):
                for k in range(c):
                    f.write(f'{matrix[i][j][k]} ')
                f.write(' ')
            f.write('\n')














