
import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):
    width = 25
    height = 6
    split = width*height
    layers = [in_string[i:i+split] for i in range(0,len(in_string),split)]
    final_image = []
    for p in range(split):
        final_image.append(-1)
        for l in range(len(layers)):
            if not layers[l][p] == '2':
                final_image[p] = layers[l][p]
                break

    counter = 0
    for y in range(height):
        for x in range(width):
            if final_image[counter] == '1':
                print('█',end='')
            else:
               print(' ',end='')
            counter += 1
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
