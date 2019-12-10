import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode

def main(in_string):
    ops = list(map(int,in_string.split(',')))

    position = 0
    relbase = 0
    inputs = [1]
    outputs = []

    while position >= 0:
        position, relbase = intcode.operate(position,relbase,ops,inputs,outputs)

    print(outputs)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
