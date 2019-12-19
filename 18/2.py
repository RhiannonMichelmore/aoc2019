import string
import collections
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import copy
import networkx as nx

def get_expand(grid,visited,x,y,door_list):
    l = []
    if x-1 >= 0 and not grid[y][x-1] in door_list and not grid[y][x-1] == '#' and not (x-1,y) in visited:
        l.append((x-1,y))
    if x+1 < len(grid[0]) and not grid[y][x+1] in door_list and not grid[y][x+1] == '#' and not (x+1,y) in visited:
        l.append((x+1,y))
    if y-1 >= 0 and not grid[y-1][x] in door_list and not grid[y-1][x] == '#' and not (x,y-1) in visited:
        l.append((x,y-1))
    if y+1 < len(grid) and not grid[y+1][x] in door_list and not grid[y+1][x] == '#' and not (x,y+1) in visited:
        l.append((x,y+1))
    return l

def pretty_print(grid):
    for row in grid:
        for item in row:
            print(item,end='')
        print()

class Node:
    def __init__(self,keys,path,r_locs,door_list,list_door,key_list,list_key,steps):
        self.keys = keys
        self.path = path
        self.r_locs = r_locs
        self.door_list = door_list
        self.list_door = list_door
        self.key_list = key_list
        self.list_key = list_key
        self.steps = steps
        self.children = []

def get_quadrant(grid,x,y):
    if x <= len(grid[0])/2 and y <= len(grid)/2:
        return 0
    elif x > len(grid[0])/2 and y <= len(grid)/2:
        return 1
    if x <= len(grid[0])/2 and y > len(grid)/2:
        return 2
    if x > len(grid[0])/2 and y > len(grid)/2:
        return 3

def main(in_string):
    rows = in_string.split('\n')
    grid = [list(row) for row in rows]

    # 0 = top left, 1 = top right, 2 = bottom left, 3 = bottom right
    r_locs = [None,None,None,None]

    key_list = dict()
    list_key = dict()
    door_list = dict() # letter key
    list_door = dict() # coord key

    quad_graphs = [nx.Graph(),nx.Graph(),nx.Graph(),nx.Graph()]
    keys_in_quad = [[],[],[],[]]

    print('Reading and generating graph.')
    for yy,row in enumerate(grid):
        for xx,item in enumerate(row):
            quad = get_quadrant(grid,xx,yy)

            if item == '@':
                r_locs[quad] = (xx,yy)
            elif item in string.ascii_lowercase:
                key_list[item] = (xx,yy)
                list_key[(xx,yy)] = item
                keys_in_quad[quad].append(item)
            elif item in string.ascii_uppercase:
                door_list[item] = (xx,yy)
                list_door[(xx,yy)] = item

            if not item == '#':
                if xx - 1 >= 0 and not grid[yy][xx-1] == '#':
                    quad_graphs[quad].add_edge((xx,yy),(xx-1,yy))
                if xx + 1 < len(grid[0]) and not grid[yy][xx+1] == '#':
                    quad_graphs[quad].add_edge((xx,yy),(xx+1,yy))
                if yy - 1 >= 0 and not grid[yy-1][xx] == '#':
                    quad_graphs[quad].add_edge((xx,yy),(xx,yy-1))
                if yy + 1 < len(grid) and not grid[yy+1][xx] == '#':
                    quad_graphs[quad].add_edge((xx,yy),(xx,yy+1))

    pretty_print(grid)
    print(keys_in_quad)
    '''
    for g in quad_graphs:
        print(g.edges())
    '''

    print('Doors:', door_list)
    print('Keys:', key_list)
    print('num keys:',len(key_list.values()))

    orig_keys = list(key_list.keys())


    # key_to_key per quadrant
    key_to_key = []
    # from each key, what doors are in the way of every other key
    for quadrant in range(4):
        key_to_key.append(dict())
        for key_name in key_list:
            key_x = key_list[key_name][0]
            key_y = key_list[key_name][1]
            if get_quadrant(grid,key_x,key_y) == quadrant:
                key_to_key[quadrant][key_name] = dict()
                for target_name in key_list:
                    target_x = key_list[target_name][0]
                    target_y = key_list[target_name][1]
                    if not key_name == target_name and get_quadrant(grid,target_x,target_y) == quadrant:
                        key_to_key[quadrant][key_name][target_name] = []
                        # get path to target from key, and all doors it goes through
                        path = nx.shortest_path(quad_graphs[quadrant],(key_x,key_y),(target_x,target_y))
                        dist = len(path)-1
                        doors = []
                        for p in path:
                            if p in list_door:
                                doors.append(list_door[p].lower())
                        key_to_key[quadrant][key_name][target_name] = [dist,doors]
    # state = [(key_gotten,x,y,door_list,key_list,steps_taken),[child states]]

    root = Node([None,None,None,None],None,r_locs,copy.deepcopy(door_list),copy.deepcopy(list_door),copy.deepcopy(key_list),copy.deepcopy(list_key),0)

    # todo: take into account the doors removed by other quads

    current_leaves = [root]
    while len(current_leaves) > 0:
        paths = dict()
        new_leaves = []
        for leaf in current_leaves:
            for idx,robot in enumerate(leaf.r_locs):
                x = robot[0]
                y = robot[1]
                expansion_list = [(x,y)]
                visited = [(x,y)]
                possible_keys = []

                if leaf.keys[idx] == None:
                    count = 1
                    while len(expansion_list) > 0:
                        new_list = []
                        for e in expansion_list:
                            l = get_expand(grid,visited,e[0],e[1],leaf.door_list)
                            possible_keys += [(k,count) for k in l if k in leaf.list_key]
                            visited += l
                            new_list += l
                        expansion_list = new_list
                        count += 1
                else:
                    current_name = leaf.keys[idx][-1]
                    quad = get_quadrant(grid,x,y)
                    flat_keys = []
                    for ik in leaf.keys:
                        if not ik == None:
                            flat_keys += list(ik)
                    possible_keys = [((key_list[target][0],key_list[target][1]),key_to_key[quad][current_name][target][0]) for target in key_to_key[quad][current_name] if all(x in flat_keys for x in key_to_key[quad][current_name][target][1]) and target not in flat_keys]

                new_children = []
                for (k,dist) in possible_keys:
                    key_name = leaf.list_key[k]
                    if leaf.keys[idx] == None:
                        key_path = key_name
                        sorted_key_path = key_name
                    else:
                        kc = list(leaf.path[:])
                        kc.sort()
                        kc = ''.join(kc)
                        sorted_key_path = kc + key_name
                        key_path = leaf.keys[idx] + key_name
                    loc_x = k[0]
                    loc_y = k[1]
                    n_door_list = leaf.door_list.copy()
                    n_list_door = leaf.list_door.copy()
                    if key_name.upper() in n_door_list:
                        loc = n_door_list[key_name.upper()]
                        del n_door_list[key_name.upper()]
                        del n_list_door[loc]
                    n_key_list = leaf.key_list.copy()
                    del n_key_list[key_name]
                    n_list_key = leaf.list_key.copy()
                    del n_list_key[k]

                    if sorted_key_path in paths:
                        other_paths = [paths[sorted_key_path]]
                    else:
                        other_paths = []
                    if len(other_paths) > 0:
                        lower = True
                        for op in other_paths:
                            if leaf.steps + dist >= op[1]:
                                lower = False
                        if lower == True:
                            paths[sorted_key_path] = (sorted_key_path,leaf.steps + dist)
                            old_keys = leaf.keys[:]
                            old_keys[idx] = key_path
                            old_locs = leaf.r_locs[:]
                            old_locs[idx] = (loc_x,loc_y)
                            n = key_name if leaf.path == None else leaf.path + key_name
                            new_node = Node(old_keys,n,old_locs,n_door_list,n_list_door,n_key_list,n_list_key,leaf.steps + dist)
                            new_leaves.append(new_node)
                            new_children.append(new_node)
                            
                    else:
                        if leaf.path == None:
                            print('initial dist from',leaf.r_locs[idx],'=',leaf.steps+dist)
                        old_keys = leaf.keys[:]
                        old_keys[idx] = key_path
                        old_locs = leaf.r_locs[:]
                        old_locs[idx] = (loc_x,loc_y)
                        n = key_name if leaf.path == None else leaf.path + key_name
                        new_node = Node(old_keys,n,old_locs,n_door_list,n_list_door,n_key_list,n_list_key,leaf.steps + dist)
                        paths[sorted_key_path] = (sorted_key_path,leaf.steps + dist)
                        new_leaves.append(new_node)
                        new_children.append(new_node)
                    leaf.children.append(new_children)
        if len(new_leaves) == 0:
            break
        print(len(current_leaves))
        current_leaves = new_leaves
        '''
        steplist = []
        for c in current_leaves:
            steplist.append(c.steps)
        minimum = min(steplist)
        maximum = max(steplist)
        print('min max',minimum,',',maximum)
        current_leaves = [cl for cl in current_leaves if cl.steps - int((maximum-minimum)/1) <= minimum]
        '''
        

    min_steps = 100000000
    min_name = None
    m = None
    for c in current_leaves:
        if c.steps < min_steps:
            min_steps = c.steps
            min_name = c.path
            m = c
    print('Min steps:',min_steps)
    print('Min route:',min_name)

    for keypath in m.keys:
        for i,k in enumerate(list(keypath)):
            min_name = keypath
            loc = key_list[k]
            quad = get_quadrant(grid,loc[0],loc[1])
            if i < len(min_name)-1:
                print('dist between',k,min_name[i+1],'=',key_to_key[quad][k][min_name[i+1]])
        print()


def print_tree(root):
    expand = [root]
    while len(expand) > 0:
        node = expand.pop()
        print(node.key,node.x,node.y,node.steps)
        expand += node.children

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
