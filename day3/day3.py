import sys
sys.path.append('../lib')

import tools, re

class Scheme(object):
    def __init__(self, inp):
        self.grid = []
        self.grid.append(['.' for _ in range(len(inp[0])+2)])
        for line in inp:
            self.grid.append(['.'] + list(line) + ['.'])
        self.grid.append(['.' for _ in range(len(inp[0])+2)])
        self.part_numbers = []
        self.gears = []

    def __str__(self):
        out = ''
        for row in self.grid:
            out += ''.join(row) + '\n'
        return out

    def _isdigit(self, y, x) -> bool:
        return self.grid[y][x].isdigit()

    def _issymbol(self, y, x) -> bool:
        return (not self._isdigit(y, x)) and (self.grid[y][x] != '.')

    def _find_all_symbols(self) -> list:
        all_symbols = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self._issymbol(y, x):
                    all_symbols.append((y, x))
        return all_symbols
                
    def _find_adjacent_numerals(self, y, x) -> list:
        tmp = dict()
        for yadd in [-1, 0, 1]:
            for xadd in [-1, 0, 1]:
                x_, y_ = y + yadd, x + xadd
                if self._isdigit(x_, y_):
                    num, coords = self._extend_digit_to_numeral(x_, y_)
                    # just put it in a map if we found a digit 
                    # of the same numeral 
                    tmp[coords] = num
        return list(tmp.values())

    def _extend_digit_to_numeral(self, y, x) -> int:
        found_digit = self.grid[y][x]
        x_array = [x]

        x_ = x-1
        proceed = True
        while proceed:
            if self._isdigit(y, x_):
                x_array.append(x_)
                found_digit = self.grid[y][x_] + found_digit
                x_ -= 1
                continue
            proceed = False

        x_ = x+1
        proceed = True
        while proceed:
            if self._isdigit(y, x_):
                x_array.append(x_)
                found_digit += self.grid[y][x_]
                x_ += 1
                continue
            proceed = False

        x_array.sort()
        return int(found_digit), (y,) + tuple(x_array)
     
    def _find_part_numbers(self):
        symbols = self._find_all_symbols()
        for symbol in symbols:
            found_numbers = self._find_adjacent_numerals(symbol[0], symbol[1])
            self.part_numbers.extend(found_numbers)

    def _find_all_gears(self):
        symbols = self._find_all_symbols()
        for symbol in symbols:
            if self.grid[symbol[0]][symbol[1]] == '*':
                numerals = self._find_adjacent_numerals(symbol[0], symbol[1])
                if len(numerals) == 2:
                    # there are exactly to numerals adjacent
                    # to a '*' symbol, so this is a gear
                    self.gears.append(tuple(numerals))
      
    def find_sum_part_numbers(self):
        self._find_part_numbers()
        return sum(self.part_numbers)

    def find_sum_gears(self):
        self._find_all_gears()
        total = 0
        for g in self.gears:
            ratio = g[0] * g[1]
            total += ratio
        return total
            

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    scheme = Scheme(lines)

    x = scheme.find_sum_part_numbers()
    print(x)

    y = scheme.find_sum_gears()
    print(y)

    
