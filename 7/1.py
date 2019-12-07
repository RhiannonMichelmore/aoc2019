import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
from itertools import permutations
import copy

def main(in_string):
    ops = list(map(int,in_string.split(',')))
    original_ops = copy.deepcopy(ops)

    phase_seqs = list(permutations(list(range(5))))
    max_signal = 0

    # go through each combination of phase settings
    for phase_seq in phase_seqs:
        # go through each amplifier 0 - 4
        for i in range(5):
            # append phase setting to inputs
            inputs.append(phase_seq[i])

            # set initial input to 0
            if i == 0:
                inputs = [0]
            outputs = []

            # get a clean copy of the code
            ops = copy.deepcopy(original_ops)
            position = 0
            while position >= 0:
                position = intcode.operate(position,ops,inputs,outputs)

            # set next amplifier input
            inputs.append(outputs[0])

        # see if we got a better max
        if outputs[0] > max_signal:
            max_signal = outputs[0]


    print("Max thruster signal:",max_signal)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
