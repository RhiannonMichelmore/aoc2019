
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
#def operate(position,relbase,ops,inputs=[],outputs=[],threaded=False):
# return position, relbase
import threading

def run_computer(ops,inputs,outputs):
    position = 0
    relbase = 0
    while position >= 0:
        position, relbase = intcode.operate(position, relbase,ops,inputs,outputs,True)
    
    outputs.append('fin')

def get_heading(current,direction):
    if direction == 0:
        if current == 'N':
            return 'W'
        elif current == 'E':
            return 'N'
        elif current == 'S':
            return 'E'
        elif current == 'W':
            return 'S'
    elif direction == 1:
        if current == 'N':
            return 'E'
        elif current == 'E':
            return 'S'
        elif current == 'S':
            return 'W'
        elif current == 'W':
            return 'N'

def get_loc(x,y,heading):
    if heading == 'N':
        return x, y-1
    elif heading == 'E':
        return x+1, y
    elif heading == 'S':
        return x, y+1
    elif heading == 'W':
        return x-1,y

def move_robot(inputs,outputs,grid,painted):
    # reads from outputs, writes to inputs
    x = int(len(grid)/2)
    y = int(len(grid)/2)
    heading = 'N'
    count = 0
    while True:
        count += 1
        while len(outputs) < 1:
            pass
        if outputs[0] == 'fin':
            break
        while len(outputs) < 2:
            pass
        colour = outputs.pop(0)
        direction = outputs.pop(0)


        grid[y][x] = colour
        painted[y][x] = True
        heading = get_heading(heading,direction)
        x, y = get_loc(x,y,heading)
        colour_over = grid[y][x]
        inputs.append(colour_over)
        if False:
        #if count %100 == 0:
            for row in grid:
                for entry in row:
                    print(entry,end='')
                print()
            print()
    

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    grid_size = 100
    grid = [[0 for i in range(grid_size)] for j in range(grid_size)]
    painted = [[False for i in range(grid_size)] for j in range(grid_size)]

    inputs = [1]
    outputs = []
    thread_computer = threading.Thread(target=run_computer, args=(ops,inputs,outputs,))
    thread_robot = threading.Thread(target=move_robot, args=(inputs,outputs,grid,painted,))

    thread_computer.start()
    thread_robot.start()

    thread_computer.join()
    thread_robot.join()

    for row in grid:
        for entry in row:
            print(entry,end='')
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
