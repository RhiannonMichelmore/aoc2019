with open('input', 'r') as f:
    l = f.read()

l = l.split('\n')[:-1]

tot = 0
for mass in l:
    ttot = 0
    t = int(int(mass)/3)-2
    ttot += t

    #print(tot)

    past = ttot
    while past > 0:
        past = int(past/3)-2
        if past > 0:
            ttot += past

    tot += ttot

print(tot)
