def get_first_digit(s):
    for c in s:
        if c in '1234567890':
            return int(c)
    return 0

numbers = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'zero': 0
}

def get_first_digit_text(s):
    index = (len(s), None)
    for num in numbers:
        i = s.find(num)
        if i >= 0 and i < index[0]:
            index = (i, numbers[num])
    if index[1]:
        return index[1]
    return 0

def get_last_digit_text(s):
    index = (-1, None)
    for num in numbers:
        i = s.rfind(num)
        if i > index[0]:
            index = (i, numbers[num])
    if index[1]:
        return index[1]
    return 0

in_data = []

with open("input", "r") as f:
    for line in f:
        in_data.append(line.strip())

    # part 1

    total = 0
    for cal_line in in_data:
        d1 = get_first_digit(cal_line)
        d2 = get_first_digit(reversed(cal_line))
        total += d1*10 + d2

    print(total)

    # part 2

    total = 0
    for cal_line in in_data:
        d1 = get_first_digit_text(cal_line)
        d2 = get_last_digit_text(cal_line)
        total += d1*10 + d2

    print(total)
