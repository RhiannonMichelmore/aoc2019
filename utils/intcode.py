# takes current position and list of ops, returns new position 
def operate(position,ops):
    op = ops[position]
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
