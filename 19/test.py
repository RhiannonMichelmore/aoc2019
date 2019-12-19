with open('grid_file_new','r') as f:
    contents = f.read().strip().split('\n')

grid = []
for line in contents:
    grid.append(list(line))

size = 99
for j in range(len(grid)):
    f = False
    for i in range(len(grid[0])):
        if grid[j][i] == '#':
            if i+size < len(grid[0]) and j+size < len(grid) and grid[j+size][i] == '#' and grid[j][i+size] == '#':
                print(i,j)
                print((i*10000)+j)
                f = True
                break
    if f == True:
        break
