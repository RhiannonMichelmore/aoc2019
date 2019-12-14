import sys
import math
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def total_ore(l):
    return sum([pair[1] for pair in l])

def main(in_string):
    react_strings = in_string.split('\n')
    # reacts[CHEM] = (AMOUNT MADE, [(REACTANT,QUANTITIY)])
    reacts = dict()
    for r in react_strings:
        items = r.split(' => ')
        reactant_strings = items[0].split(', ')
        product_string = items[1] # never more than one product
        product = product_string.split(' ')[1]
        product_amount = int(product_string.split(' ')[0])
        reactants = []
        for re in reactant_strings:
            reactant = re.split(' ')[1]
            reactant_amount = int(re.split(' ')[0])
            reactants.append((reactant,reactant_amount))
        reacts[product] = (product_amount,reactants)

    ore_limit = 1000000000000
    count = 8845200

    while True:
        needed = [['FUEL',count]]
        ores = []
        
        leftovers = dict()
        for key in reacts:
            leftovers[key] = 0

        while len(needed) > 0:
            current = needed.pop()
            name_needed = current[0]
            amount_needed = current[1]

            if name_needed == 'ORE':
                ores.append([name_needed,amount_needed])
            else:
                # check if we have any leftover already
                leftover = leftovers[name_needed]
                if amount_needed - leftover <= 0:
                    # great, we already had enough leftover
                    leftovers[name_needed] = leftover-amount_needed
                    amount_needed = 0
                elif leftover > 0:
                    # we had some leftover but not quite enough
                    amount_needed = amount_needed - leftover
                    leftovers[name_needed] = 0

                if amount_needed > 0:
                    formula = reacts[name_needed]
                    reactants = formula[1]
                    product_amount = formula[0]
                    # work out the number of times we need to do this reaction to have enough
                    reaction_repeats = math.ceil(amount_needed/product_amount)
                    # work out how many left over we will have
                    extra = (reaction_repeats*product_amount) - amount_needed
                    # add the right amount of reactants to the list 
                    for re in reactants:
                        pair = [re[0],re[1]*reaction_repeats]
                        needed.append(pair)

                    leftovers[name_needed] += extra

        ore_amount = total_ore(ores)
        if count % 10000 == 0:
            print(count)
        if ore_amount > ore_limit:
            print(count-1)
            break
        count += 1

            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
