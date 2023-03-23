import itertools

products = ['pi', 'wa', 'sn', 'sh']
rates = {'pi-pi': 1, 'pi-wa': 0.5, 'pi-sn': 1.45, 'pi-sh': 0.75, 'wa-pi': 1.95, 'wa-wa': 1, 'wa-sn': 3.1, 'wa-sh': 1.49, 'sn-pi': 0.67, 'sn-wa': 0.31, 'sn-sn': 1, 'sn-sh': 0.48, 'sh-pi': 1.34, 'sh-wa': 0.64, 'sh-sn': 1.98, 'sh-sh': 1}


combos = [x for x in itertools.product(products, repeat=4)]
money = 2000000
combs = []

for combo in combos:
    combo = ('sh',) + combo + ('sh',)
    combs.append(combo)

moneys = []

for combo in combs:
    for i in range(len(combo)):
        if i != len(combo) - 1:
            money *= rates[f'{combo[i]}-{combo[i+1]}']
    print(combo, money)
    moneys.append(money)
    money = 2000000

print(max(moneys))