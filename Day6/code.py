def get_dist(hold_time, duration):
    return (duration - hold_time)*hold_time

def get_wins(t, d):
    t0 = 0
    t1 = t
    d0 = get_dist(t0, t)
    while d0 <= d and t0 < t:
        t0 += 1
        d0 = get_dist(t0, t)

    d1 = get_dist(t1, t)
    while d1 <= d and t1 > t0:
        t1 -= 1
        d1 = get_dist(t1, t)

    return t1 - t0 + 1

in_data = []

with open("input", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            label, data = line.split(":")
            data = data.strip()
            data2 = data.replace(" ", "")
            data = [int(x) if x else None for x in data.split(" ")]
            
            while None in data:
                data.remove(None)
            if label == "Time":
                times = data
                time2 = int(data2)
            elif label == "Distance":
                dists = data
                dist2 = int(data2)

# part 1

margin = 1
for t,d in zip(times,dists):
    w = get_wins(t,d)
    margin *= w

print(margin)

# part 2

w = get_wins(time2, dist2)
print(w)
