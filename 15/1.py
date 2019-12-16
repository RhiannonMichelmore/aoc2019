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

def main(in_string):
    ops = list(map(int,in_string.split(',')))

    # keep a dict where key is a coordinate and value is a list of length
    # 4 that says if we have tried to go in that direction yet N, S, W, E

    # keep a stack of states, add one whenever we give an input
    # state = ((x,y),(state of ops),(state of position),(state of relbase))

    # if we find a wall, pop the top state off, look if there is still an
    # unexplored direction, if so, push the same state back on and carry on

    # if no wall, carry on
    
    # if oxygen system, halt and print len of stack

    visited = dict()
    x = 0
    y = 0
    visited[(x,y)] = [0,0,0,0]
    position = 0
    current_position = position
    relbase = 0
    current_relbase = relbase

    inputs = []
    outputs = []

    current_ops = copy.deepcopy(ops)
    stack = [((x,y),current_ops,current_position,current_relbase)]

    # NORTH = 1, SOUTH = 2, WEST = 3, EAST = 4

    # 0 = wall hit, 1 = moved in direction requested, 2 = moved and found oxygen system

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
               # backtrack 
                stack.pop()
                state = copy.deepcopy(stack[-1])
                x = state[0][0]
                y = state[0][1]
                ops = state[1]
                position = state[2]
                relbase = state[3]
                continue
            else:
                # just pick the first one in the list
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
                last_state = ((x,y),copy.deepcopy(ops),position,relbase)
                stack.append(last_state)
                # minus 1 as there is no move to get to first location
                print(len(stack)-1)
                break
            elif out == 1:
                x, y = update_coords(x,y,picked)
                visited[(x,y)] = [0,0,0,0]
                visited[(x,y)][opposite(picked)-1] = 1
                last_state = ((x,y),copy.deepcopy(ops),position,relbase)
                stack.append(last_state)
            elif out == 0:
                # backtrack
                state = copy.deepcopy(stack[-1])
                x = state[0][0]
                y = state[0][1]
                ops = state[1]
                position = state[2]
                relbase = state[3]
                continue

        position, relbase = intcode.operate(position, relbase, ops, inputs, outputs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
