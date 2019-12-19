import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
import copy

def pretty_print(grid):
    for row in grid:
        for item in row:
            print(item,end='')
        print()

def is_between(top_grad,bot_grad,x,y):
    if y/x <= bot_grad and y/x >= top_grad:
        return True
    else:
        return False

def main(in_string):
    ops = list(map(int,in_string.split(',')))
    orig_ops = copy.deepcopy(ops)

    position = 0
    relbase = 0

    inputs = []
    outputs = []

    grid = [['.' for i in range(50)] for j in range(50)]
    coord_list = []
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            coord_list.append((i,j))
    count = 0

    for coord in coord_list:
        if coord[0] % 100 == 0 or coord[1] % 100 == 0:
            print(coord)

        inputs = []
        outputs = []
        position = 0
        relbase = 0
        ops = orig_ops[:]

        inputs.append(coord[0])
        inputs.append(coord[1])

        while position >= 0:
            position, relbase = intcode.operate(position,relbase,ops,inputs,outputs)

        grid[coord[1]][coord[0]] = '#' if outputs[0] == 1 else '.'
        if outputs[0] == 1:
            count += 1

    top_edge = []
    bottom_edge = []
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == '#':
                if j == 0:
                    top_edge.append((i,j))
                elif grid[j-1][i] == '.':
                    top_edge.append((i,j))
                if i == 0:
                    bottom_edge.append((i,j))
                elif grid[j][i-1] == '.':
                    bottom_edge.append((i,j))


    bottom_grads = []
    top_grads = []

    origin = bottom_edge[0]
    for coord in bottom_edge[1:]:
        bottom_grads.append(coord[1]/coord[0])

    for coord in top_edge[1:]:
        top_grads.append(coord[1]/coord[0])

    av_bot_grad = sum(bottom_grads)/len(bottom_grads)
    av_top_grad = sum(top_grads)/len(top_grads)


    grid = [['.' for i in range(2100)] for j in range(2100)]
    coord_list = []
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if j > 1000 and i > 1000:
                adjustment = 0.1 if i < 100 or j < 100 else 0.05
                mt = av_top_grad - adjustment
                mb = av_bot_grad + adjustment
                if i == 0 and j == 0:
                    coord_list.append((i,j))
                elif i == 0 or j == 0:
                    pass
                elif is_between(mt,mb,i,j):
                    coord_list.append((i,j))
    print(len(coord_list))

    for p,coord in enumerate(coord_list):
        if p % 1000 == 0:
            print('progress: {0:.2f}%'.format((p/len(coord_list))*100))

        inputs = []
        outputs = []
        position = 0
        relbase = 0
        ops = orig_ops[:]

        inputs.append(coord[0])
        inputs.append(coord[1])

        while position >= 0:
            position, relbase = intcode.operate(position,relbase,ops,inputs,outputs)

        grid[coord[1]][coord[0]] = '#' if outputs[0] == 1 else '.'
        if outputs[0] == 1:
            count += 1

    with open('grid_file_new','w') as f:
        for row in grid:
            f.write(''.join(row)+'\n')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
