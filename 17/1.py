import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def pretty_print(grid):
    for row in grid:
        for item in row:
            print(item,end='')
        print()
    print()

def main(in_string):
    ops = list(map(int,in_string.split(',')))
    position = 0
    relbase = 0
    inputs = []
    outputs = []
    while position >= 0:
        position, relbase = intcode.operate(position, relbase, ops, inputs, outputs)

    grid = []
    current_line = []
    for output in outputs:
        if output == 10:
            if len(current_line) > 0:
                grid.append(current_line)
            current_line = []
        else:
            current_line.append(str(chr(output)))

    intersections = []
    for y,row in enumerate(grid):
        for x,item in enumerate(row):
            if item == '#':
                inter = True
                if x - 1 >= 0:
                    if not grid[y][x-1] == '#':
                        inter = False
                else:
                    inter = False
                if x + 1 < len(row):
                    if not grid[y][x+1] == '#':
                        inter = False
                else:
                    inter = False
                if y - 1 >= 0:
                    if not grid[y-1][x] == '#':
                        inter = False
                else:
                    inter = False
                if y + 1 < len(grid):
                    if not grid[y+1][x] == '#':
                        inter = False
                else:
                    inter = False

                if inter == True:
                    intersections.append((x,y))

    pretty_print(grid)
    print('Intersections:',intersections)
    print('#:',len(intersections))

    total = 0
    for inter in intersections:
        total += (inter[0]*inter[1])

    print('Answer:',total)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
