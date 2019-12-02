with open('input', 'r') as f:
    l = f.read()

l = l.split('\n')[:-1]

tot = 0
for mass in l:
    t = int(int(mass)/3)-2
    tot += t

print(tot)
