
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):
    digits = list(map(int,list(in_string)))

    base_pattern = [0,1,0,-1]
    base_patterns = []
    for j in range(len(digits)+1):
        curr_pattern = [[x for a in range(j+1)] for x in base_pattern]
        curr_pattern = [item for sublist in curr_pattern for item in sublist]
        head = curr_pattern.pop(0)
        curr_pattern.append(head)
        base_patterns.append(curr_pattern)
    for i in range(1,101):
        new_digits = []
        for j in range(len(digits)):
            summed = 0
            for k,d in enumerate(digits[j:]):
                index = (k+j) % len(base_patterns[j])
                summed += d*base_patterns[j][index]
            ones = int(str(summed)[-1])
            new_digits.append(ones)

        print('phase',i,'new digits (first 8):',new_digits[:8])
        digits = new_digits



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
