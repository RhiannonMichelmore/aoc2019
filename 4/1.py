
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
from z3 import *

def main(in_string):
    bounds = in_string.split('-')
    lower = int(bounds[0])
    upper = int(bounds[1])

    lowerVal = IntVal(lower)
    upperVal = IntVal(upper)
    targetVec = IntVector('targetVec',len(str(lower)))
    length = len(str(lower))

    # force 0 - 9
    exprs = []
    for i in range(length):
        exprs.append(And(targetVec[i] >= 0, targetVec[i] <= 9))

    singleExp = And(exprs)

    # force within input bounds
    total = 0
    for i in range(length):
        exponent = length-1-i
        total = total + ((10**exponent)*targetVec[i])

    forceExp = And(total >= lowerVal, total <= upperVal)

    # two adjacent digits rule
    exprs = []
    for i in range(length-1):
        exprs.append(targetVec[i] == targetVec[i+1])

    adjExp = Or(exprs)

    #never decrease left to right
    exprs = []
    for i in range(length-1):
        exprs.append(targetVec[i] <= targetVec[i+1])

    decExp = And(exprs)

    finalExp = And(singleExp,forceExp,adjExp,decExp)

    s = Solver()
    counter = 0
    s.add(finalExp)
    while s.check() == sat:
        s.add(Or(targetVec[0] != s.model()[targetVec[0]], targetVec[1] != s.model()[targetVec[1]], targetVec[2] != s.model()[targetVec[2]], targetVec[3] != s.model()[targetVec[3]], targetVec[4] != s.model()[targetVec[4]], targetVec[5] != s.model()[targetVec[5]]))
        counter += 1

    print(counter)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
