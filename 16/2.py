
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):
    orig_digits = list(map(int,list(in_string)))
    search_index = int(''.join([str(x) for x in orig_digits[:7]]))
    print('search index:',search_index)

    mult = 10000
    digits = []
    for i in range(mult):
        digits += orig_digits

    digits = digits[search_index:]

    for i in range(1,101): #phase iteration
        #print('phase = ',i)
        sum_from_end = 0
        for j in range(len(digits)-1,-1,-1): #index iteration
            sum_from_end += digits[j]
            ones = sum_from_end % 10
            digits[j] = ones

    print(digits[:8])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
