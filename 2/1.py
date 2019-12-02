import sys

def main(in_string):
    ops = list(map(int,in_string.strip().split(',')))
    print(ops)
    position = 0

    while not ops[position] == 99:
        if ops[position] == 1:
            first = ops[ops[position+1]]
            second = ops[ops[position+2]]
            plus = first + second
            ops[ops[position+3]] = plus
        elif ops[position] == 2:
            first = ops[ops[position+1]]
            second = ops[ops[position+2]]
            mult = first * second
            ops[ops[position+3]] = mult
        position = position + 4

    print(ops)
    print(ops[0])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
