tab1 = {0: [1, 2, 3], 1:[2, 3, 4]}
tab2 = [1, 2, 3]

for t in tab1.values():
    if t == tab2:
        print("equal")