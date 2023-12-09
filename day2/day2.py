import sys
sys.path.append('../lib')

import tools, re

COLORS = ['red', 'green', 'blue']

class Game(object):
    def __init__(self, inp):
        s = inp.split(':')
        self.id = int(s[0].split()[1])
        matches = s[1].split(';')
        self.matches = []
        for match_desc in matches:
            m = Match(match_desc)
            self.matches.append(m)

    def __str__(self):
        out = f'Game ID: {self.id}\n'
        for m in self.matches:
            out += m.__str__()
        return out

    def get_id(self) -> int:
        return self.id

    def possible_for_limits(self, limits: dict) -> bool:
        for m in self.matches:
            if not m.possible_for_limits(limits):
                return False
        return True

    def get_fewest_possible_power(self) -> int:
        required = self._get_fewest_possible_cubes()
        power = 1
        for c in COLORS:
            try:
                n = required[c]
            except KeyError:
                continue
            if n > 0:
                power *= n
        return power
        

    def _get_fewest_possible_cubes(self):
        required = dict(zip(COLORS, [0 for _ in range(len(COLORS))]))
        for m in self.matches:
            for c in COLORS:
                try:
                    need = m.cubes[c]
                except KeyError:
                    continue
                required[c] = max(required[c], need)
        return required
        

class Match(object):
    def __init__(self, inp):
        self.cubes = dict()        
        for s in inp.split(', '):
            s = s.split()
            self.cubes[s[1]] = int(s[0])

    def __str__(self):
        out = 'Match: '
        for k, v in self.cubes.items():
            out += f'{k}: {v} '
        out += '\n'
        return out

    def possible_for_limits(self, limits: dict) -> bool:
        for color, want in self.cubes.items():
            try:
                have = limits[color]
            except KeyError:
                return False
            if have < want:
                return False
        return True


            

def solve1(lines):
    total = 0
    limits = dict(zip(COLORS, [12, 13, 14])) 
    for l in lines:
        game = Game(l)
        if game.possible_for_limits(limits):
            total += game.get_id()
    return total

def solve2(lines):
    total = 0
    for l in lines:
        g = Game(l)
        power = g.get_fewest_possible_power()
        total += power
    return total


if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    x = solve1(lines)
    print(x)

    y = solve2(lines)
    print(y)

    
