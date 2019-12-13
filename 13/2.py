
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def print_grid(grid,score):
    for idx,row in enumerate(grid):
        for value in row:
            if value == 0:
                print(' ',end='')
            elif value == 1:
                print('█',end='')
            elif value == 2:
                print('#',end='')
            elif value == 3:
                print('=',end='')
            elif value == 4:
                print('O',end='')
        if idx == len(grid)-1:
            print('     Score:',score)
        else:
            print()

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    # part 2, need to set ops[0] = 2
    ops[0] = 2
    position = 0
    relbase = 0
    # initial input is neutral joystick
    inputs = [0]
    outputs = []
    grid_x = 10
    grid_y = 10
    grid = [[0 for x in range(grid_x)] for y in range(grid_y)]

    score = 0
    first_input = False
    ball_x = None
    ball_dir = 0
    bat_x = 0
    left_bound = 0
    right_bound = 0

    while position >= 0:
        # read in grid until the program wants first input, here we can get bounds etc
        if first_input == False:
            instruction = ops[position]
            opcode = int(str(instruction)[-2:])
            if opcode == 3:
                first_input = True
                right_bound = len(grid[0])-1
                for row in grid:
                    if 4 in row:
                        ball_x = row.index(4)
                    if 3 in row:
                        bat_x = row.index(3)
        else:
            instruction = ops[position]
            opcode = int(str(instruction)[-2:])
            if opcode == 3:
                old_x = ball_x
                for row in grid:
                    if 4 in row:
                        ball_x = row.index(4)
                    if 3 in row:
                        bat_x = row.index(3)
                if ball_dir == 0:
                    ball_dir = 1 if ball_x > old_x else -1
                elif ball_x + ball_dir == left_bound or ball_x + ball_dir == right_bound:
                    ball_dir *= -1

                if bat_x < ball_x:
                    inputs.append(1)
                elif bat_x > ball_x:
                    inputs.append(-1)
                else:
                    inputs.append(ball_dir)

        position, relbase = intcode.operate(position,relbase,ops,inputs,outputs)
        if len(outputs) == 3:
            from_left = outputs.pop(0)
            from_top = outputs.pop(0)
            tile_id = outputs.pop(0)
            if from_left == -1 and from_top == 0:
                score = tile_id
            else:
                if from_left >= len(grid[0]):
                    # extend right
                    extension = (from_left+1-len(grid[0]))
                    for row in grid:
                        for i in range(extension):
                            row.append(0)
                if from_top >= len(grid):
                    # extend down
                    for i in range((from_top+1-len(grid))):
                        grid.append([0 for x in range(len(grid[0]))])

                grid[from_top][from_left] = tile_id

    print_grid(grid,score)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
