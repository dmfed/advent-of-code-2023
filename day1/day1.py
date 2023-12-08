import sys
sys.path.append('../lib')

import tools, re

# re_digit captures overlapping ocurrences 
re_digit = re.compile(r'(?=(one|two|three|four|five|six|seven|eight|nine))')

digits_dict = {
    'one': '1', 
    'two': '2', 
    'three': '3', 
    'four': '4', 
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def solve1(lines) -> int:
    total = 0
    for l in lines:
        total += findsum(l)
    return total


def solve2(lines) -> int:
    total = 0
    for l in lines:
        l = to_digits(l)
        total += findsum(l)
    return total


def findsum(line):
    first = find_digit(line)
    second = find_digit(line, reverse=True)
    return int(first + second)


def find_digit(line, reverse=False):
    val = ''
    idx = None
    start, end, step = 0, len(line), 1
    if reverse:
        start, end, step = len(line)-1, -1, -1
    for i in range(start, end, step):
        if line[i].isdigit():
            val = line[i]
            break
    return val

def to_digits(line):
    m = re_digit.findall(line)
    if not m:
        return line
    # since words may overlap (e.g. in 'oneight' or 'twone'), we'll 
    # replace the ocurrence of first and last (possibly overlapping) matches
    # and return combined string.
    l1 = re.sub(m[0], digits_dict[m[0]], line, count=1)
    l2 = re.sub(m[-1], digits_dict[m[-1]], line)
    return l1+l2
   

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    x = solve1(lines)
    print(x)

    r = tools.Reader('input.txt')
    lines = r.read()

    y = solve2(lines)
    print(y)

    
