card_map = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

jcard_map = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'T': 11,
    '9': 10,
    '8': 9,
    '7': 8,
    '6': 7,
    '5': 6,
    '4': 5,
    '3': 4,
    '2': 3,
    'J': 2,
}

def compare_cards(c1, c2):
    return card_map[c1] - card_map[c2]

def compare_cards_joker(c1, c2):
    return jcard_map[c1] - jcard_map[c2]

class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.rank = self.get_rank()
        self._compare = compare_cards

    def use_jokers(self):
        self.rank = self.get_joker_rank()
        self._compare = compare_cards_joker

    def get_rank(self):
        h = self.cards
        ncards = [1, 0, 0, 0, 0]
        for i in range(1, 5):
            matched = False
            for j in range(0, i):
                if h[i] == h[j]:
                    ncards[j] += 1
                    matched = True
                    break
            if not matched:
                ncards[i] += 1
        if 5 in ncards:
            return 7
        if 4 in ncards:
            return 6
        if 3 in ncards:
            if 2 in ncards:
                return 5
            return 4
        if ncards.count(2) == 2:
            return 3
        if 2 in ncards:
            return 2
        return 1

    def get_joker_rank(self):
        h = self.cards
        ncards = [0, 0, 0, 0, 0]
        jokers = 0
        for i in range(5):
            if h[i] == 'J':
                jokers += 1
            else:
                matched = False
                for j in range(0, i):
                    if h[i] == h[j]:
                        ncards[j] += 1
                        matched = True
                        break
                if not matched:
                    ncards[i] += 1
        if jokers:
            ncards[ncards.index(max(ncards))] += jokers
        if 5 in ncards:
            return 7
        if 4 in ncards:
            return 6
        if 3 in ncards:
            if 2 in ncards:
                return 5
            return 4
        if ncards.count(2) == 2:
            return 3
        if 2 in ncards:
            return 2
        return 1

    def __eq__(self, other):
        return self.cards == other.cards

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        if self.rank == other.rank:
            for i in range(5):
                diff = self._compare(self.cards[i], other.cards[i])
                if diff > 0:
                    return True
                if diff < 0:
                    return False

        return False

    def __lt__(self, other):
        return (not (self > other)) and (not (self == other))

    def __repr__(self):
        return "Hand({}, {})".format(self.cards, self.bid)

def compare_hands(h1, h2):
    drank = get_rank(h1) - get_rank(h2)

hands = []

with open("input", "r") as f:
    for line in f:
        cards, bid = line.strip().split(" ")
        bid = int(bid)
        hands.append(Hand(cards, bid))

# part 1

ordered_hands = []
for hand in hands:
    inserted = False
    for i,shand in enumerate(ordered_hands):
        if hand > shand:
            ordered_hands.insert(i, hand)
            inserted = True
            break
    if not inserted:
        ordered_hands.append(hand)

total_winnings = 0
rank = len(ordered_hands)
for h in ordered_hands:
    total_winnings += rank*h.bid
    rank -= 1

print(total_winnings)

# part 2

ordered_hands = []
for hand in hands:
    hand.use_jokers()
    inserted = False
    for i,shand in enumerate(ordered_hands):
        if hand > shand:
            ordered_hands.insert(i, hand)
            inserted = True
            break
    if not inserted:
        ordered_hands.append(hand)

total_winnings = 0
rank = len(ordered_hands)
for h in ordered_hands:
    total_winnings += rank*h.bid
    rank -= 1

print(total_winnings)
