
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
