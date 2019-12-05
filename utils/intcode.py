# takes current position and list of ops, returns new position 
def operate(position,ops,inputs,outputs):
    instruction = ops[position]
    opcode = int(str(instruction)[-2:])
    param_modes = str(instruction)[:-2]

    if opcode == 99:
        # as 99 is halt
        return -1
    elif opcode == 1:
        # Addition
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            first = ops[ops[position+1]]
        elif param_modes[0] == '1':
            first = ops[position+1]

        if param_modes[1] == '0':
            second = ops[ops[position+2]]
        elif param_modes[1] == '1':
            second = ops[position+2]

        plus = first + second

        # dont need to check param mode here since it'll always be position mode
        ops[ops[position+3]] = plus
        return position + 4

    elif opcode == 2:
        # Multiplication
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            first = ops[ops[position+1]]
        elif param_modes[0] == '1':
            first = ops[position+1]

        if param_modes[1] == '0':
            second = ops[ops[position+2]]
        elif param_modes[1] == '1':
            second = ops[position+2]

        mult = first * second

        # dont need to check param mode here since it'll always be position mode
        ops[ops[position+3]] = mult
        return position + 4

    elif opcode == 3:
        # Input and store, (dont need to check param mode)
        input_val = inputs.pop(0)

        ops[ops[position+1]] = input_val

        return position + 2

    elif opcode == 4:
        # Output
        param_modes = '0'*(1-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            out_val = ops[ops[position+1]]
        elif param_modes[0] == '1':
            out_val = ops[position+1]

        outputs.append(out_val)
        return position + 2

    elif opcode == 5:
        # Jump if true
        param_modes = '0'*(2-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            determine_jump = ops[ops[position+1]]
        elif param_modes[0] == '1':
            determine_jump = ops[position+1]

        if param_modes[1] == '0':
            new_ip = ops[ops[position+2]]
        elif param_modes[1] == '1':
            new_ip = ops[position+2]

        if not determine_jump == 0:
            return new_ip
        else:
            return position + 3

    elif opcode == 6:
        # Jump if false
        param_modes = '0'*(2-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            determine_jump = ops[ops[position+1]]
        elif param_modes[0] == '1':
            determine_jump = ops[position+1]

        if param_modes[1] == '0':
            new_ip = ops[ops[position+2]]
        elif param_modes[1] == '1':
            new_ip = ops[position+2]

        if determine_jump == 0:
            return new_ip
        else:
            return position + 3

    elif opcode == 7:
        # Less than
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            first = ops[ops[position+1]]
        elif param_modes[0] == '1':
            first = ops[position+1]

        if param_modes[1] == '0':
            second = ops[ops[position+2]]
        elif param_modes[1] == '1':
            second = ops[position+2]


        if first < second:
            to_store = 1
        else:
            to_store = 0
        # dont need to check param mode here since it'll always be position mode
        ops[ops[position+3]] = to_store
        return position + 4

    elif opcode == 8:
        # Equals
        # 3 params, pad param_modes array then reverse it
        param_modes = '0'*(3-len(param_modes)) + param_modes
        param_modes = param_modes[::-1]

        if param_modes[0] == '0':
            first = ops[ops[position+1]]
        elif param_modes[0] == '1':
            first = ops[position+1]

        if param_modes[1] == '0':
            second = ops[ops[position+2]]
        elif param_modes[1] == '1':
            second = ops[position+2]


        if first == second:
            to_store = 1
        else:
            to_store = 0
        # dont need to check param mode here since it'll always be position mode
        ops[ops[position+3]] = to_store
        return position + 4
