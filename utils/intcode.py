import time
# takes current position and list of ops, returns new position 

def get_position(param_mode, index, ops, relbase):
    if param_mode == '0':
        return ops[index]
    elif param_mode == '1':
        return index
    elif param_mode == '2':
        return relbase + ops[index]

def bounds(pos,ops):
    if pos >= 0 and pos < len(ops):
        return ops[pos]
    else:
        return 0

def write(pos,ops,value):
    if pos >= len(ops):
        # write to new memory location
        # get dist to new location
        n_append = pos - (len(ops)-1)
        for i in range(n_append):
            ops.append(0)
        ops[pos] = value
    else:
        ops[pos] = value

def operate(position,relbase,ops,inputs=[],outputs=[],threaded=False):
    instruction = ops[position]
    opcode = int(str(instruction)[-2:])
    param_modes = str(instruction)[:-2]

    if opcode == 99:
        # as 99 is halt
        return -1, -1
    elif opcode == 1:
        # Addition
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        first = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        second = bounds(pos,ops)

        plus = first + second

        to_write_pos = get_position(param_modes[2],position+3,ops,relbase)
        write(to_write_pos,ops,plus)

        return position + 4, relbase

    elif opcode == 2:
        # Multiplication
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        first = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        second = bounds(pos,ops)

        mult = first * second

        to_write_pos = get_position(param_modes[2],position+3,ops,relbase)
        write(to_write_pos,ops,mult)
        return position + 4, relbase

    elif opcode == 3:
        # Input and store, (dont need to check param mode)
        if threaded == True:
            while len(inputs) == 0:
                pass
        input_val = inputs.pop(0)

        param_modes = '0'*(1-len(param_modes)) + param_modes
        to_write_pos = get_position(param_modes[0],position+1,ops,relbase)

        write(to_write_pos,ops,input_val)

        return position + 2, relbase

    elif opcode == 4:
        # Output
        param_modes = '0'*(1-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        out_val = bounds(pos,ops)

        outputs.append(out_val)
        return position + 2, relbase

    elif opcode == 5:
        # Jump if true
        param_modes = '0'*(2-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        determine_jump = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        new_ip = bounds(pos,ops)

        if not determine_jump == 0:
            return new_ip, relbase
        else:
            return position + 3, relbase

    elif opcode == 6:
        # Jump if false
        param_modes = '0'*(2-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        determine_jump = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        new_ip = bounds(pos,ops)

        if determine_jump == 0:
            return new_ip, relbase
        else:
            return position + 3, relbase

    elif opcode == 7:
        # Less than
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        first = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        second = bounds(pos,ops)

        if first < second:
            to_store = 1
        else:
            to_store = 0

        to_write_pos = get_position(param_modes[2],position+3,ops,relbase)
        write(to_write_pos,ops,to_store)

        return position + 4, relbase

    elif opcode == 8:
        # Equals
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        first = bounds(pos,ops)

        pos = get_position(param_modes[1],position+2,ops,relbase)
        second = bounds(pos,ops)

        if first == second:
            to_store = 1
        else:
            to_store = 0

        to_write_pos = get_position(param_modes[2],position+3,ops,relbase)
        write(to_write_pos,ops,to_store)
        return position + 4, relbase

    elif opcode == 9:
        param_modes = '0'*(1-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        pos = get_position(param_modes[0],position+1,ops,relbase)
        relbase_move = bounds(pos,ops)

        return position + 2, relbase+relbase_move
