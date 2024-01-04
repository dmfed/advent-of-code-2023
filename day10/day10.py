import sys
sys.path.append('../lib')

import tools

START = 'S'

class Direction(object):
    def __init__(self, val: str):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)

    def opposite(self):
        if self == N:
            return S 
        elif self == S:
            return N
        elif self == E:
            return W
        elif self == W:
            return E
        
N = Direction('N')
E = Direction('E')
S = Direction('S')
W = Direction('W')

class Tile(object):
    def __init__(self, val: str, x, y):
        self.val = val
        self.x = x
        self.y = y
        self.links = []
        if val == '|':
            self.links = [N, S]
        elif val == '-':
            self.links = [E, W]
        elif val == 'L':
            self.links = [N, E]
        elif val == 'J':
            self.links = [N, W]
        elif val == '7':
            self.links = [W, S]
        elif val == 'F':
            self.links = [S, E]    

    def __str__(self):
        return self.val

    def opposite_end(self, d: Direction) -> Direction:
        entry = d.opposite()
        if not entry in self.links:
            return None
        if entry == self.links[0]:
            return self.links[1]
        else:
            return self.links[0]

    def has_link_from(self, d: Direction) -> bool:
        return (d.opposite() in self.links)
        

    def is_pipe(self):
        return self.val != '.'


class Field(object):
    def __init__(self, lines: list[str]):
        self.grid = [list(l) for l in lines]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.grid[y][x] = Tile(self.grid[y][x], x, y)

    def __str__(self):
        out = 'Field:\n'
        for row in self.grid:
            out += ''.join([str(tile) for tile in row]) + '\n'
        return out

    def get(self, x, y: int) -> Tile:
        if y >= len(self.grid) or x >= len(self.grid):
            return None
        return  self.grid[y][x]

        
class Walker(Field):
    def __init__(self, lines):
        super().__init__(lines)
        
    def _get_start(self) -> Tile:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                t = self.get(x, y)
                if t.val == START:
                    return t
        return None

    def _walk_to_start(self, t: Tile, direction: Direction) -> (bool, int):
        self.visited = set()
        steps = 0
        while True:
            x, y = t.x, t.y
            self.visited.add((x, y))
            if direction == E:
                x += 1
            elif direction == S:
                y += 1
            elif direction == W:
                x -= 1
            elif direction == N:
                y -= 1
            nxt = self.get(x, y)
            if (not nxt):
                break

            steps += 1
            if nxt.val == START:
                return True, steps
            if not nxt.has_link_from(direction):
                break

            t = nxt
            d = nxt.opposite_end(direction)
            direction = d
        return False, steps


    def find_max_steps_in_loop(self) -> int:
        start = self._get_start()
        for direction in [N, E, S, W]:
            found, steps = self._walk_to_start(start, direction)
            if found:
                return steps // 2

    def find_captured_by_loop(self) -> int:
        if not self.visited:
            self.find_max_steps_in_loop()
        pass

                
                
if __name__ == '__main__':
    r = tools.Reader('test_input.txt')
    lines = r.read()

    w = Walker(lines)
    print(w)
    steps = w.find_max_steps_in_loop()
    print(steps)
    print(w.visited)

    r = tools.Reader('input.txt')
    lines = r.read()

    w = Walker(lines)
    steps = w.find_max_steps_in_loop()
    print(steps)
    # print(w.visited)

