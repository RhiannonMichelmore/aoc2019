
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):
    width = 25
    height = 6
    split = width*height
    layers = [in_string[i:i+split] for i in range(0,len(in_string),split)]
    min_layer = None
    min_zeros = 1000000
    for layer in layers:
        zeros = layer.count('0')
        if zeros < min_zeros:
            min_zeros = zeros
            min_layer = layer

    print("Results:",min_layer.count('1')*min_layer.count('2'))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
