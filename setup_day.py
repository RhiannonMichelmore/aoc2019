import datetime
import os
import glob
import shutil

day = datetime.datetime.today().day
if not os.path.exists(str(day)):
    os.mkdir(str(day))

template = """
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
"""

file_one = str(day)+'/1.py'
file_two = str(day)+'/2.py'
in_file = str(day)+'/input'

if not os.path.exists(file_one):
    with open(file_one,'w') as f:
        f.write(template)

if not os.path.exists(file_two):
    with open(file_two,'w') as f:
        f.write(template)

if not os.path.exists(in_file):
    open(in_file,'w').close()


