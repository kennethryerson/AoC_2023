import re

class PartNumber:
    def __init__(self, number, row, col, end, map):
        self.number = number
        self.r1 = row - 1 if row > 0 else 0
        self.r2 = row + 1 if row + 1 < len(map) else row
        self.c1 = col - 1 if col > 0 else 0
        self.c2 = end + 1 if end + 1 < len(map[0]) else end

    def is_valid(self, map):
        valid = False
        for row in range(self.r1, self.r2+1):
            for col in range(self.c1, self.c2+1):
                if map[row][col] not in '1234567890.':
                    valid = True
        return valid

    def adjacent(self, row, col):
        return (row >= self.r1) and (row <= self.r2) and (col >= self.c1) and (col <= self.c2)

    def __repr__(self):
        return "PartNumber({}, {}, {}, {})".format(self.number, self.row, self.col, self.end)

class Gear:
    def __init__(self, ratio, row, col):
        self.ratio = ratio
        self.row = row
        self.col = col

class Schematic:
    def __init__(self, data):
        pat = re.compile("(\d+)")
        self.map = data
        self.part_numbers = []
        row = 0
        for line in self.map:
            i = 0
            while i < len(line):
                m = pat.match(line[i:])
                if m:
                    pn = PartNumber(int(m.group(1)), row, i, i+len(m.group(1))-1, self.map)
                    if pn.is_valid(self.map):
                        self.part_numbers.append(pn)
                    i += len(m.group(1))
                else:
                    i += 1
            row += 1

    def sum(self):
        total = 0
        for pn in self.part_numbers:
            total += pn.number
        return total

    def adjacent(self, pn, row, col):
        return pn.adjacent(row, col)

    def find_gears(self):
        total_ratio = 0
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == '*':
                    npn = 0
                    ratio = 1
                    for pn in self.part_numbers:
                        if pn.adjacent(row, col):
                            npn += 1
                            ratio = ratio * pn.number
                            if npn > 2:
                                break
                    if npn == 2:
                        total_ratio += ratio
        return total_ratio

    def __repr__(self):
        return "Schematic({})".format(self.part_numbers)

in_data = []

with open("input", "r") as f:
    for line in f:
        in_data.append(line.strip())

    # part 1

    schematic = Schematic(in_data)
    print(schematic.sum())

    # part 2

    print(schematic.find_gears())
