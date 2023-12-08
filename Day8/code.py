import re
import numpy as np


with open("input", "r") as f:
    node_pat = re.compile("(\w{3})\s+=\s+\((\w{3}),\s*(\w{3})\)")
    directions = None
    tree = {}
    for line in f:
        line = line.strip()
        if directions is None:
            directions = line
        else:
            m = node_pat.match(line)
            if m:
                tree[m.group(1)] = (m.group(2), m.group(3))

    # part 1

    node = "AAA"
    steps = 0

    while node != "ZZZ":
        for d in directions:
            if d == 'L':
                node = tree[node][0]
                steps += 1
            elif d == 'R':
                node = tree[node][1]
                steps += 1
            if node == "ZZZ":
                break
    
    print(steps)

    # part 2

    nodes = [n if n.endswith('A') else None for n in tree]
    while None in nodes:
        nodes.remove(None)

    print("A nodes: {}".format(len(nodes)))

    cycles = [0 for n in nodes]
    for i,n in enumerate(nodes):
        steps = 0
        while not n.endswith('Z'):
            for d in directions:
                if d == 'L':
                    n = tree[n][0]
                    steps += 1
                elif d == 'R':
                    n = tree[n][1]
                    steps += 1
                if n.endswith('Z'):
                    break
        cycles[i] = steps
    
    print(cycles)

    # find LCM of all cycles

    a = cycles[0]
    for b in cycles[1:]:
        a = np.lcm(a, b)
    print(a)
