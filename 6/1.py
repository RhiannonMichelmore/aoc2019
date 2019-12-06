import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import networkx as nx

def main(in_string):
    orbits = in_string.strip().split('\n')
    orbits = [(o.split(')')[0],o.split(')')[1]) for o in orbits]

    system = nx.DiGraph()
    for o in orbits:
        system.add_edge(*o)

    preds = dict()
    for node in system.nodes():
        preds[node] = []
        # every node will only have one predecessor
        curr_node = node
        while True:
            pred_list = list(system.predecessors(curr_node))
            if len(pred_list) > 0:
                curr_node = pred_list[0]
                preds[node].append(curr_node)
            else:
                break

    total = 0
    for node in preds:
        total += len(preds[node])

    print(total)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
