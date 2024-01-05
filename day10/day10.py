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
        return f'{self.val} x: {self.x} y: {self.y}'

    def __eq__(self, obj) -> bool:
        return self.x == obj.x and self.y == obj.y

    def __hash__(self):
        return hash((self.x, self.y))

    def opposite_pipe_end(self, d: Direction) -> Direction:
        if not d in self.links:
            return None
        if d == self.links[0]:
            return self.links[1]
        else:
            return self.links[0]

    def has_link_from(self, d: Direction) -> bool:
        return (d in self.links)
        

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

    def _get(self, x, y: int) -> Tile:
        if y < 0 or x < 0 or y >= len(self.grid) or x >= len(self.grid):
            return None
        return  self.grid[y][x]

    def get_adjacent(self, t: Tile, d: Direction) -> Tile:
        x, y = t.x, t.y
        if d == E:
            x += 1
        elif d == S:
            y += 1
        elif d == W:
            x -= 1
        elif d == N:
            y -= 1
        return self._get(x, y)

        

        
class Walker(Field):
    def __init__(self, lines):
        super().__init__(lines)
        self.loop = []
        self.visited = set()
        
    def _get_start(self) -> Tile:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                t = self._get(x, y)
                if t.val == START:
                    return t
        return None

    def _find_loop(self):
        start = self._get_start()
        for d in [N, E, S, W]:
            curr = start
            dir = d
            self.loop = []
            while True:
                self.loop.append(curr)
                nxt = self.get_adjacent(curr, dir)
                if not nxt or not nxt.has_link_from(dir.opposite()):
                    break
                if nxt.val == START:
                    return
                curr = nxt
                dir = nxt.opposite_pipe_end(dir.opposite())


    def find_max_steps_in_loop(self) -> int:
        self._find_loop()
        return len(self.loop) // 2

    def find_captured_by_loop(self) -> int:
        if not self.loop:
            # this fills self.loop slice
            # with loop tiles
            self._find_loop()
        self.visited = set(self.loop)
        inside_loop = set()
        for t in self.loop:
            for d in [N, E, S, W]:
                newt = self.get_adjacent(t, d)
                if not newt or newt in self.visited:
                    continue
                if self._is_inside_loop(newt):
                    inside_loop.add(newt)
                self.visited.add(newt)
        return len(inside_loop)


    def _is_inside_loop(self, t: Tile) -> bool:
        # TODO
        return True
            

                
if __name__ == '__main__':
    r = tools.Reader('test_input.txt')
    lines = r.read()

    w = Walker(lines)
    steps = w.find_max_steps_in_loop()
    print(steps)
    n = w.find_captured_by_loop()
    print(n)

    r = tools.Reader('input.txt')
    lines = r.read()

    w = Walker(lines)
    steps = w.find_max_steps_in_loop()
    print(steps)
    # print(w.loop)

