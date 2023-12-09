def get_diffs(seq):
    return [y - x for x,y in zip(seq[:-1], seq[1:])]

def get_next(seq):
    if not any(seq):
        return 0
    
    d = get_next(get_diffs(seq))
    return seq[-1] + d

def get_prev(seq):
    if not any(seq):
        return 0
    
    d = get_prev(get_diffs(seq))
    return seq[0] - d

in_data = []

with open("input", "r") as f:
    for line in f:
        in_data.append([int(x) for x in line.strip().split(" ")])

    # part 1

    total = 0
    for seq in in_data:
        n = get_next(seq)
        total += n

    print(total)

    # part 2

    total = 0
    for seq in in_data:
        n = get_prev(seq)
        total += n

    print(total)
