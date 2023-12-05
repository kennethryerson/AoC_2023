def number_wins(winning, have):
    wins = 0
    for guess in have:
        if guess in winning:
            wins += 1
    return wins

in_data = []

with open("input", "r") as f:
    for line in f:
        in_data.append(line.strip())

    # part 1

    total_points = 0
    ncards = [1 for i in range(len(in_data))]
    for ci,card in enumerate(in_data):
        winning, have = card.split(":")[1].split("|")
        winning = winning[1:-1]
        have = have[1:]
        winning = [int(winning[i:i+2]) for i in range(0, len(winning), 3)]
        have = [int(have[i:i+2]) for i in range(0, len(have), 3)]

        nwins = number_wins(winning, have)
        points = 2**(nwins - 1) if nwins else 0
        total_points += points

        for wi in range(nwins):
            ncards[ci+wi+1] += ncards[ci]

    print(total_points)

    # part 2

    print(sum(ncards))
