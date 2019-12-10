import copy
from string import ascii_lowercase
import sys
from fractions import Fraction
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def pretty_print(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x],end='')
        print()

    print()

def sign(num):
    if num < 0:
        return -1
    else:
        return 1

def main(in_string):
    grid = list(map(list,in_string.strip().split('\n')))
    pretty_print(grid)

    # . = empty, # = asteroid
    # (0,0) top left

    # for each asteroid, take a copy of the grid
    # order all the other asteroids by distance to the current one
    # keep track of current letter
    # iterate through other asteroids, if location has been covered already, skip
    # if not, then give it a capital letter and update the current letter
    # increment the count of visible asteroids
    # now block out all the other squares it blocks with a lowercase version of the same letter
    # do this by getting the smallest ratio of distance from the original, and stepping until edges
    # e.g if asteroid1 is in (0,0) and asteroid2 is in (2,4), then smallest integer ratio is:
    # (1,2) so block out (2,4) + (1,2), (2,4)+(1,2)+(1,2)... etc until edge
    # simplest fraction form
    # keep going until done with this asteroid, record total seen, and move on
    # pick highest total seen


    # get list of asteroids
    asteroids = [(i,j) for j in range(len(grid)) for i in range(len(grid[0])) if grid[j][i] == '#']

    view_maps = []

    sight_count = dict()

    count = 0
    target = 1
    for asteroid in asteroids:
        view_map = copy.deepcopy(grid)
        '''
        if count == target:
            pretty_print(view_map)
        '''
        sight_count[asteroid] = 0
        # get all other asteroids
        as_tmp = copy.deepcopy(asteroids)
        # order all asteroids by manhat distance to current, and remove first since it will
        # be the current one
        as_tmp.sort(key = lambda a: abs(a[0]-asteroid[0]) + abs(a[1]-asteroid[1]))
        as_tmp = as_tmp[1:]
        for a in as_tmp:
            if view_map[a[1]][a[0]] == '#':
                # its in sight!
                sight_count[asteroid] += 1
                view_map[a[1]][a[0]] = 'B'
                lit_x_diff = a[0] - asteroid[0]
                lit_y_diff = a[1] - asteroid[1]
                if lit_x_diff == 0:
                    rel_y = 1*sign(lit_y_diff)
                    rel_x = 0
                elif lit_y_diff == 0:
                    rel_y = 0
                    rel_x = 1*sign(lit_x_diff)
                else:
                    simplified_frac = Fraction(lit_x_diff,lit_y_diff)
                    rel_x = sign(lit_x_diff)*abs(simplified_frac.numerator)
                    rel_y = sign(lit_y_diff)*abs(simplified_frac.denominator)

                next_x = a[0] + rel_x
                next_y = a[1] + rel_y
                while next_x < len(view_map[0]) and next_x >= 0 and next_y < len(view_map) and next_y >= 0:
                    view_map[next_y][next_x] = 'b'
                    next_x = next_x + rel_x
                    next_y = next_y + rel_y


        view_maps.append(view_map)
        '''
        if count == target:
            pretty_print(view_map)
            break
        count += 1
        '''

    max_detected = 0
    max_asteroid = None
    for key in sight_count:
        if sight_count[key] > max_detected:
            max_detected = sight_count[key]
            max_asteroid = key

    print(max_asteroid,max_detected)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
