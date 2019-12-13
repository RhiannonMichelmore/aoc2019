
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    position = 0
    relbase = 0
    inputs = []
    outputs = []
    grid_x = 10
    grid_y = 10
    grid = [[0 for x in range(grid_x)] for y in range(grid_y)]

    while position >= 0:
        position, relbase = intcode.operate(position,relbase,ops,inputs,outputs)
        if len(outputs) == 3:
            from_left = outputs.pop(0)
            from_top = outputs.pop(0)
            tile_id = outputs.pop(0)
            if from_left >= len(grid[0]):
                # extend right
                extension = (from_left+1-len(grid[0]))*2
                for row in grid:
                    for i in range(extension):
                        row.append(0)
            if from_top >= len(grid):
                # extend down
                for i in range((from_top+1-len(grid))*2):
                    grid.append([0 for x in range(len(grid[0]))])

            grid[from_top][from_left] = tile_id

    # count block tiles (number 2)
    count = 0
    for row in grid:
        for tile in row:
            if tile == 2:
                count += 1

    print("Block tiles:",count)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
