import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import networkx as nx

def main(in_string):
    orbits = in_string.strip().split('\n')
    orbits = [(o.split(')')[0],o.split(')')[1]) for o in orbits]

    system = nx.Graph()
    for o in orbits:
        system.add_edge(*o)

    path = nx.shortest_path(system,'YOU','SAN')
    print(len(path)-3)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
