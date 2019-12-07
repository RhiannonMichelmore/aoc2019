import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
from itertools import permutations
import copy
import time

# WE GOING PARALELL FRIENDS
import threading

# function to run in threads
def run_amplifier(ops, inputs, outputs, ident):
    position = 0
    while position >= 0:
        position = intcode.operate(position,ops,inputs,outputs,True)

def main(in_string):
    ops = list(map(int,in_string.split(',')))
    original_ops = copy.deepcopy(ops)

    phase_seqs = list(permutations(list(range(5,10))))
    max_signal = 0

    # stuff for progress bar
    count = 0
    max_count = len(phase_seqs)

    # go through each combination of phase settings
    for phase_seq in phase_seqs:
        # print progress bar because I'm impatient
        print(count+1,'/',max_count)
        count += 1

        # setup input arrays with phase settings in
        inputs = []
        for i in range(5):
            inputs.append([phase_seq[i]])

        # give input 0 to amp A
        inputs[0].append(0)

        # setup threading
        jobs = []
        for i in range(5):
            # get fresh copy of ops
            ops = copy.deepcopy(original_ops)

            # outputs of current is inputs of next
            # loop round from E to A
            if i == 4:
                outputs = inputs[0]
            else:
                outputs = inputs[i+1]
            # create thread and append to jobs list
            thread = threading.Thread(target=run_amplifier, args=(ops,inputs[i],outputs,i,))
            jobs.append(thread)

        # run jobs
        for j in jobs:
            j.start()

        # wait for them all to finish
        for j in jobs:
            j.join()

        # see if we got a better max signal
        if inputs[0][0] > max_signal:
            max_signal = inputs[0][0]

    print("Max thruster signal:",max_signal)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
