import re

class Pull:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return "Pull({},{},{})".format(self.red, self.green, self.blue)

class Game:
    def __init__(self, id):
        self.id = id
        self.pulls = []

    def add_pull(self, pull):
        self.pulls.append(pull)

    def possible(self, red=0, green=0, blue=0):
        poss = True
        for p in self.pulls:
            poss = poss and (p.red <= red) and (p.green <= green) and (p.blue <= blue)
        return poss

    def get_power(self):
        mr = 0
        mg = 0
        mb = 0
        for p in self.pulls:
            if p.red > mr:
                mr = p.red
            if p.green > mg:
                mg = p.green
            if p.blue > mb:
                mb = p.blue
        return mr*mg*mb

    def __repr__(self):
        return "Game({}, pulls={})".format(self.id, self.pulls)


in_data = []
pattern = re.compile("Game (\d+)\:(.+)")
rpattern = re.compile(".*?(\d+) red")
gpattern = re.compile(".*?(\d+) green")
bpattern = re.compile(".*?(\d+) blue")

bag = (12, 13, 14)

with open("input", "r") as f:
    games = []
    for line in f:
        m = pattern.match(line.strip())
        if m:
            gid = int(m.group(1))
            games.append(Game(gid))
            for pull in m.group(2).strip().split(";"):
                r = rpattern.match(pull)
                g = gpattern.match(pull)
                b = bpattern.match(pull)
                r = int(r.group(1)) if r else 0
                g = int(g.group(1)) if g else 0
                b = int(b.group(1)) if b else 0
                games[-1].add_pull(Pull(r,g,b))

    # part 1

    idsum = 0
    for g in games:
        # print("{} {}".format(g, g.possible(*bag)))
        if g.possible(*bag):
            idsum += g.id

    print(idsum)

    # part 2

    sumpower = 0
    for g in games:
        sumpower += g.get_power()

    print(sumpower)
