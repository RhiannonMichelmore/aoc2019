import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
import copy

def update_coords(x,y,d):
    if d == 1:
        return x, y-1
    elif d == 2:
        return x, y+1
    elif d == 3:
        return x-1, y
    elif d == 4:
        return x+1, y

def opposite(d):
    if d == 1:
        return 2
    elif d == 2:
        return 1
    elif d == 3:
        return 4
    elif d == 4:
        return 3

def get_rel_dir(x,y,xx,yy):
    if x > xx:
        return 3
    elif x < xx:
        return 4
    elif y > yy:
        return 1
    elif y < yy:
        return 2

def main(in_string):
    ops = list(map(int,in_string.split(',')))

    # keep a dict where key is a coordinate and value is a list of length
    # 4 that says if we have tried to go in that direction yet N, S, W, E

    # keep a stack of positions

    # if we find a wall, pop the top state off, look if there is still an
    # unexplored direction, if so, push the same state back on and carry on

    # if no wall, carry on
    
    # if oxygen system, halt and print len of stack

    visited = dict()
    grid_size = 44
    x = 22
    y = 22
    visited[(x,y)] = [0,0,0,0]
    position = 0
    relbase = 0

    inputs = []
    outputs = []

    stack = [(x,y)]

    grid = [[' ' for i in range(grid_size)] for j in range(grid_size)]
    grid[y][x] = '.'

    # NORTH = 1, SOUTH = 2, WEST = 3, EAST = 4

    # 0 = wall hit, 1 = moved in direction requested, 2 = moved and found oxygen system

    backtrack = False

    while True:
        instruction = ops[position]
        opcode = int(str(instruction)[-2:])
        if opcode == 3:
            # needs input
            # from current location, get dirs we havent tried
            v = visited[(x,y)]
            to_try = []
            for idx,d in enumerate(v):
                if d == 0:
                    to_try.append(idx+1)

            if len(to_try) == 0:
                backtrack = True
                stack.pop()
                if len(stack) == 0:
                    break
                old_loc = stack[-1]
                d = get_rel_dir(x,y,old_loc[0],old_loc[1])
                picked = d
                inputs.append(picked)
            else:
                # just pick the first one in the list
                backtrack = False
                picked = to_try[0]
                visited[(x,y)][to_try[0]-1] = 1
                inputs.append(picked)
        elif len(outputs) > 0:
            # we have an output
            out = outputs.pop()
            if out == 2:
                x, y = update_coords(x,y,picked)
                if not (x,y) in visited:
                    visited[(x,y)] = [0,0,0,0]
                visited[(x,y)][opposite(picked)-1] = 1
                if backtrack == False:
                    stack.append((x,y))
                    grid[y][x] = 'O'
            elif out == 1:
                x, y = update_coords(x,y,picked)
                if not (x,y) in visited:
                    visited[(x,y)] = [0,0,0,0]
                visited[(x,y)][opposite(picked)-1] = 1
                if backtrack == False:
                    stack.append((x,y))
                    grid[y][x] = '.'
            elif out == 0:
                wallx, wally = update_coords(x,y,picked)
                grid[wally][wallx] = '#'

        position, relbase = intcode.operate(position, relbase, ops, inputs, outputs)

    for y,row in enumerate(grid):
        for x,item in enumerate(row):
            if item == 'O':
                source = (x,y)
            print(item,end='')
        print()
    print()

    expansion_list = [source]
    minutes = 0
    while len(expansion_list) > 0:
        new_list = []
        for coord in expansion_list:
            if grid[coord[1]+1][coord[0]] == '.':
                grid[coord[1]+1][coord[0]] = 'O'
                new_list.append((coord[0],coord[1]+1))
            if grid[coord[1]-1][coord[0]] == '.':
                grid[coord[1]-1][coord[0]] = 'O'
                new_list.append((coord[0],coord[1]-1))
            if grid[coord[1]][coord[0]+1] == '.':
                grid[coord[1]][coord[0]+1] = 'O'
                new_list.append((coord[0]+1,coord[1]))
            if grid[coord[1]][coord[0]-1] == '.':
                grid[coord[1]][coord[0]-1] = 'O'
                new_list.append((coord[0]-1,coord[1]))

        # remove dups
        new_list = list(set(new_list))

        # remove unexpandable stuff
        final_list = []
        for coord in new_list:
            if not grid[coord[1]+1][coord[0]] == '.' and not grid[coord[1]-1][coord[0]] == '.' and not grid[coord[1]][coord[0]+1] == '.' and not grid[coord[1]][coord[0]-1] == '.':
                pass
            else:
                final_list.append(coord)

        expansion_list = copy.deepcopy(final_list)
        minutes += 1

    print(minutes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
