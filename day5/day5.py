import sys
sys.path.append('../lib')

import tools

class Range(object):
    def __init__(self, dst_start, src_start, lenght):
        self.dst = dst_start
        self.src = src_start
        self.len = lenght

    def __str__(self):
        return f'range: {self.dst}, {self.src}, {self.len}'

    def map(self, n: int) -> int:
        if n < self.src or n > (self.src + self.len - 1):
            return None
        return self.dst - self.src + n   


class Map(object):
    def __init__(self, name):
        self.name = name
        self.ranges = []

    def __str__(self):
        out = f'map "{self.name}"\n'
        for r in self.ranges:
            out += str(r) + '\n'
        return out

    def append_range(self, r):
        self.ranges.append(r)

    def map(self, inp: int) -> int:
        for r in self.ranges:
            mapped = r.map(inp)
            if mapped is not None:
                return mapped
        return inp
            

class Almanac(object):
    def __init__(self, lines):
        self.seeds = [int(n) for n in lines[0].replace('seeds: ', '').split()]
        self.maps = list()
        m = None
        for line in lines[2:]:
            if line == '':
                self.maps.append(m)
                continue
            if line[0].isalpha():
                m = Map(line)
                continue
            a, b, c = [int(n) for n in line.split()]
            r = Range(a, b, c)
            m.append_range(r)
        self.maps.append(m)

    def __str__(self):
        out = 'The latest Island Island Almanac\n'
        out += f'Seeds: {", ".join([str(n) for n in self.seeds])}\n'
        for m in self.maps:
            out += str(m)
        return out

    def _map_seed_to_location(self, seed: int) -> int:
        for m in self.maps:
            seed = m.map(seed)
        return seed

    def find_closest_location_for_seed_nums(self) -> int:
        result = float('inf')
        for seed in self.seeds:
            loc = self._map_seed_to_location(seed)
            if loc < result:
                result = loc
        return result

    def find_closest_location_for_seed_ranges(self) -> int:
        closest = float('inf')
        for i in range(0, len(self.seeds), 2):
           for n in range(self.seeds[i], self.seeds[i]+self.seeds[i+1]):
                loc = self._map_seed_to_location(n)
                if loc < closest:
                    closest = loc
        return closest
        

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    al = Almanac(lines)

    x = al.find_closest_location_for_seed_nums()
    print(x)

    y = al.find_closest_location_for_seed_ranges()
    print(y)


    
