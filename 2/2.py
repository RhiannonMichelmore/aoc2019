import sys
import copy

# does operation on ops, returns new starting position
def operate(op,position,ops):
    if op == 99:
        # as 99 is halt
        return -1
    elif op == 1:
        first = ops[ops[position+1]]
        second = ops[ops[position+2]]
        plus = first + second
        ops[ops[position+3]] = plus
        return position + 4
    elif op == 2:
        first = ops[ops[position+1]]
        second = ops[ops[position+2]]
        mult = first * second
        ops[ops[position+3]] = mult
        return position + 4


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
                current_op = ops[position]
                position = operate(current_op,position,ops)

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
