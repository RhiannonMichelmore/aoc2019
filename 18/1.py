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
    def __init__(self,key,x,y,door_list,list_door,key_list,list_key,steps):
        self.key = key
        self.x = x
        self.y = y
        self.door_list = door_list
        self.list_door = list_door
        self.key_list = key_list
        self.list_key = list_key
        self.steps = steps
        self.children = []

def main(in_string):
    rows = in_string.split('\n')
    grid = [list(row) for row in rows]
    x = None
    y = None
    key_list = dict()
    list_key = dict()
    door_list = dict() # letter key
    list_door = dict() # coord key

    G = nx.Graph()

    print('Reading and generating graph.')
    for yy,row in enumerate(grid):
        for xx,item in enumerate(row):
            if item == '@':
                x = xx
                y = yy
            elif item in string.ascii_lowercase:
                key_list[item] = (xx,yy)
                list_key[(xx,yy)] = item
            elif item in string.ascii_uppercase:
                door_list[item] = (xx,yy)
                list_door[(xx,yy)] = item

            if not item == '#':
                if xx - 1 >= 0 and not grid[yy][xx-1] == '#':
                    G.add_edge((xx,yy),(xx-1,yy))
                if xx + 1 < len(grid[0]) and not grid[yy][xx+1] == '#':
                    G.add_edge((xx,yy),(xx+1,yy))
                if yy - 1 >= 0 and not grid[yy-1][xx] == '#':
                    G.add_edge((xx,yy),(xx,yy-1))
                if yy + 1 < len(grid) and not grid[yy+1][xx] == '#':
                    G.add_edge((xx,yy),(xx,yy+1))

    pretty_print(grid)
    print('Edges:',G.edges())
    print('Doors:', door_list)
    print('Keys:', key_list)
    print('num keys:',len(key_list.values()))
    print('Start:',x,y)

    orig_keys = list(key_list.keys())

    # make grid into graph WITHOUT DOORS

    key_to_key = dict()
    # from each key, what doors are in the way of every other key
    for key_name in key_list:
        key_to_key[key_name] = dict()
        key_x = key_list[key_name][0]
        key_y = key_list[key_name][1]
        for target_name in key_list:
            if not key_name == target_name:
                key_to_key[key_name][target_name] = []
                target_x = key_list[target_name][0]
                target_y = key_list[target_name][1]
                # get path to target from key, and all doors it goes through
                path = nx.shortest_path(G,(key_x,key_y),(target_x,target_y))
                dist = len(path)-1
                doors = []
                for p in path:
                    if p in list_door:
                        doors.append(list_door[p].lower())
                key_to_key[key_name][target_name] = [dist,doors]
    # state = [(key_gotten,x,y,door_list,key_list,steps_taken),[child states]]
    root = Node(None,x,y,copy.deepcopy(door_list),copy.deepcopy(list_door),copy.deepcopy(key_list),copy.deepcopy(list_key),0)
    current_leaves = [root]


    while len(current_leaves) > 0:
        paths = dict()
        new_leaves = []
        for leaf in current_leaves:
            x = leaf.x
            y = leaf.y
            expansion_list = [(x,y)]
            visited = [(x,y)]
            possible_keys = []

            if leaf.key == None:
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
                current_name = leaf.key[-1]
                possible_keys = [((key_list[target][0],key_list[target][1]),key_to_key[current_name][target][0]) for target in key_to_key[current_name] if all(x in list(leaf.key) for x in key_to_key[current_name][target][1]) and target not in list(leaf.key)]

            new_children = []
            for (k,dist) in possible_keys:
                key_name = leaf.list_key[k]
                if leaf.key == None:
                    key_path = key_name
                    sorted_key_path = key_name
                else:
                    kc = list(leaf.key[:])
                    kc.sort()
                    kc = ''.join(kc)
                    sorted_key_path = kc + key_name
                    key_path = leaf.key + key_name
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
                        new_node = Node(key_path,loc_x,loc_y,n_door_list,n_list_door,n_key_list,n_list_key,leaf.steps + dist)
                        new_leaves.append(new_node)
                        new_children.append(new_node)
                        
                else:
                    if leaf.key == None:
                        print('initial dist to first key:',dist)
                    new_node = Node(key_path,loc_x,loc_y,n_door_list,n_list_door,n_key_list,n_list_key,leaf.steps + dist)
                    paths[sorted_key_path] = (sorted_key_path,leaf.steps + dist)
                    new_leaves.append(new_node)
                    new_children.append(new_node)
            leaf.children = new_children
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
    for c in current_leaves:
        if c.steps < min_steps:
            min_steps = c.steps
            min_name = c.key
    print('Min steps:',min_steps)
    print('Min route:',min_name)
    for i,k in enumerate(list(min_name)):
        if i < len(min_name)-1:
            print('dist between',k,min_name[i+1],'=',key_to_key[k][min_name[i+1]])


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
