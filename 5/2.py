
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    print(ops)
    position = 0
    inputs = [5]
    outputs = []

    while not position == -1:
        position = intcode.operate(position,ops,inputs,outputs)

    print(outputs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
