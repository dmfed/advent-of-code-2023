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
        l = replace_word_with_digit(l)
        total += findsum(l)
    return total


def findsum(line):
    first = find_digit(line)
    second = find_digit(line, reverse=True)
    return int(first + second)


def find_digit(line, reverse=False):
    val = ''
    start, end, step = 0, len(line), 1
    if reverse:
        start, end, step = len(line)-1, -1, -1
    for i in range(start, end, step):
        if line[i].isdigit():
            val = line[i]
            break
    return val

def replace_word_with_digit(line):
    start, end, step = 0, len(line), 1
    found = False
    for i in range(start, end, step):
        for word in digits_dict.keys():
            if line[i:].startswith(word):
                # just inserting the digit so that our
                # find_digit func can help with the rest 
                line = line[:i] + digits_dict[word] + line[i:]
                found = True
                break
        if found:
            break

    start, end, step = len(line), -1, -1
    found = False
    for i in range(start, end, step):
        for word in digits_dict.keys():
            if line[:i].endswith(word):
                line = line[:i] + digits_dict[word]+line[i:]
                found = True
                break
        if found:
            break
    return line
   

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    x = solve1(lines)
    print(x)

    r = tools.Reader('input.txt')
    lines = r.read()

    y = solve2(lines)
    print(y)


    
