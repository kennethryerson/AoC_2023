import re

def get_overlap(r1, r2):
    if r2.start in r1 or (r2.stop - 1) in r1 or r1.start in r2:
        start = r1.start if (r1.start > r2.start) else r2.start
        stop = r1.stop if (r1.stop < r2.stop) else r2.stop
        return range(start, stop)

def get_non_overlap(r1, r2):
    non_overlaps = []
    if r2.start in r1 or (r2.stop - 1) in r1 or r1.start in r2:
        if r1.start < r2.start:
            start = r1.start
            stop = r2.start
            non_overlaps.append(range(start, stop))
        if r1.stop > r2.stop:
            start = r2.stop
            stop = r1.stop
            non_overlaps.append(range(start, stop))
    else:
        non_overlaps.append(r1)
    return non_overlaps

def get_all_non_overlaps(r1, ranges):
    if ranges:
        non_overlaps = []
        for r in r1:
            no = get_non_overlap(r, ranges[0])
            if no:
                non_overlaps.extend(no)
        return get_all_non_overlaps(non_overlaps, ranges[1:])
    else:
        return r1

def get_matching_dest(sources, dests, new_sources):
    new_dests = []
    for ns in new_sources:
        for s,d in zip(sources, dests):
            if ns.start in s:
                dstart = d.start + ns.start - s.start
                dstop = d.stop + ns.stop - s.stop
                new_dests.append(range(dstart, dstop))
                break
    return new_dests

class Map:
    def __init__(self, source, dest, data):
        self.source = source
        self.dest = dest
        self.dest_ranges = []
        self.source_ranges = []
        for line in data:
            d,s,l = [int(x) for x in line.strip().split(" ")]
            self.dest_ranges.append(range(d, d+l))
            self.source_ranges.append(range(s, s+l))

    def map(self, source):
        for i,r in enumerate(self.source_ranges):
            if source in r:
                return self.dest_ranges[i][r.index(source)]
        return source

    def combine(self, next_map):
        m = Map(self.source, next_map.dest, [])
        for nsr, ndr in zip(next_map.source_ranges, next_map.dest_ranges):
            # print("next map: {} --> {}".format(nsr, ndr))
            for dr,sr in zip(self.dest_ranges, self.source_ranges):
                overlap = get_overlap(nsr, dr)
                if overlap:
                    # print("combining overlapping ranges {} {} --> {}".format(nsr, dr, overlap))
                    # print("sr: {}, ndr: {}".format(sr, ndr))
                    m.source_ranges.append(range(sr[dr.index(overlap.start)], sr[dr.index(overlap.stop-1)]+1))
                    m.dest_ranges.append(range(ndr[nsr.index(overlap.start)], ndr[nsr.index(overlap.stop-1)]+1))
        # print("self non overlaps")
        for dr,sr in zip(self.dest_ranges, self.source_ranges):
            non_overlaps = get_all_non_overlaps([sr], m.source_ranges)
            m.source_ranges.extend(non_overlaps)
            non_overlaps_dest = get_matching_dest(self.source_ranges, self.dest_ranges, non_overlaps)
            m.dest_ranges.extend(non_overlaps_dest)
            # if len(non_overlaps) != len(non_overlaps_dest):
            #     print("non_overlaps:      {}".format(non_overlaps))
            #     print("non_overlaps_dest: {}".format(non_overlaps_dest))
            assert(len(non_overlaps) == len(non_overlaps_dest))
            for s,d in zip(non_overlaps,non_overlaps_dest):
                # print("s: {}, d: {}".format(s,d))
                assert(len(s) == len(d))
        # print("next non overlaps")
        for dr,sr in zip(next_map.dest_ranges, next_map.source_ranges):
            non_overlaps = get_all_non_overlaps([sr], m.source_ranges)
            # print("non_overlaps: {}".format(non_overlaps))
            m.source_ranges.extend(non_overlaps)
            non_overlaps_dest = get_matching_dest(next_map.source_ranges, next_map.dest_ranges, non_overlaps)
            m.dest_ranges.extend(non_overlaps_dest)
            assert(len(non_overlaps) == len(non_overlaps_dest))
            for s,d in zip(non_overlaps,non_overlaps_dest):
                # print("s: {}, d: {}".format(s,d))
                assert(len(s) == len(d))
        # print("len(sources) = {}  len(dests) = {}".format(len(m.source_ranges), len(m.dest_ranges)))
        for s,d in zip(m.source_ranges,m.dest_ranges):
            # print("s: {}, d: {}".format(s,d))
            assert(len(s) == len(d))

        return m

    def check_ranges(self):
        for i in range(len(self.source_ranges)):
            r1 = self.source_ranges[i]
            for j in range(i + 1, len(self.source_ranges)):
                r2 = self.source_ranges[j]
                m = "{}-{} source {} {}".format(self.source,self.dest,r1,r2)
                assert (r1.start not in r2), m
                assert ((r1.stop - 1) not in r2), m
                assert (r2.start not in r1), m
        for i in range(len(self.dest_ranges)):
            r1 = self.dest_ranges[i]
            for j in range(i + 1, len(self.dest_ranges)):
                r2 = self.dest_ranges[j]
                m = "{}-{} dest {} {}".format(self.source,self.dest,r1,r2)
                assert (r1.start not in r2), m
                assert ((r1.stop - 1) not in r2), m
                assert (r2.start not in r1), m

    def sort_ranges(self):
        new_sources = []
        new_dests = []
        for s,d in zip(self.source_ranges, self.dest_ranges):
            inserted = False
            for i,nd in enumerate(new_dests):
                if d.start < nd.start:
                    new_dests.insert(i, d)
                    new_sources.insert(i, s)
                    inserted = True
                    break
            if not inserted:
                new_sources.append(s)
                new_dests.append(d)
        self.source_ranges = new_sources
        self.dest_ranges = new_dests

    def lowest_dest_in_range(self, r):
        for sr in self.source_ranges:
            if r.start in sr:
                return self.map(r.start)
            if sr.start in r:
                return self.map(sr.start)
            if (r.stop - 1) in sr:
                return self.map(sr.start)
        return self.map(r.start)

    def __repr__(self):
        return "Map(source={}, dest={}, source_ranges={}, dest_ranges={})".format(self.source,self.dest,self.source_ranges,self.dest_ranges)

seed_pat = re.compile("seeds:\s*(.+)")
map_pat = re.compile("(\w+)-to-(\w+) map:")

with open("input", "r") as f:
    maps = {}
    seeds = []
    seeds_ranges = []
    map_lines = []
    map_source = None
    map_dest = None
    for line in f:
        line = line.strip()
        sm = seed_pat.match(line)
        mm = map_pat.match(line)
        if sm:
            seeds = [int(x) for x in sm.group(1).split(" ")]
            seeds_ranges = [range(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
        elif mm:
            map_source = mm.group(1)
            map_dest = mm.group(2)
            map_lines = []
        elif line == "":
            # create map
            if map_source:
                maps[map_source] = Map(map_source, map_dest, map_lines)
            map_source = None
            map_dest = None
        else:
            map_lines.append(line)
    if map_source:
        maps[map_source] = Map(map_source, map_dest, map_lines)


    cmap = maps["seed"]
    while cmap.dest != "location":
        # print()
        # print("#### COMBINE {0}-{1} with {1}-{2} #############################".format(cmap.source, cmap.dest, maps[cmap.dest].dest))
        cmap = cmap.combine(maps[cmap.dest])
        # print(cmap)
        cmap.check_ranges()
    cmap.sort_ranges()
    # print(cmap)

    # part 1

    lowest_location = None
    for seed in seeds:
        location = cmap.map(seed)
        if not lowest_location or location < lowest_location:
            lowest_location = location
    print(lowest_location)

    # part 2

    lowest_location = None

    for seedr in seeds_ranges:
        location = cmap.lowest_dest_in_range(seedr)
        if not lowest_location or location < lowest_location:
            lowest_location = location
    print(lowest_location)
