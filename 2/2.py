import sys
import copy

sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    start_ops = copy.deepcopy(ops)

    for noun in range(100):
        for verb in range(100):
            position = 0
            ops = copy.deepcopy(start_ops)
            ops[1] = noun
            ops[2] = verb

            while not position == -1:
                position = intcode.operate(position,ops)

            if ops[0] == 19690720:
                print('found target')
                print('noun:',noun,'verb:',verb)
                print('answer:',(100*noun)+verb)
                return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
