import sys, re
sys.path.append('../lib')

import tools

LEFT = 'L'
RIGHT = 'R'


class Instructions(object):
    def __init__(self, inp: str):
        self.curr = 0
        self.instructions = list(inp)

    def __iter__(self):
        return self

    def __next__(self):
        instruction = self.instructions[self.curr]
        self.curr = (self.curr + 1) % len(self.instructions)
        return instruction

    def reset(self):
        self.curr = 0
        

class Node(object):
    def __init__(self, value, left, right):
        self.value = value
        self.l = left
        self.r = right


class Network(object):
    def __init__(self):
        self.m = dict()
        self.curr = None
        for l in lines:
            pass
            
    def add(self, n: Node):
        self.m[n.value] = n

    def get(self, name: str) -> Node:
        n = self.m[name]
        return n

    def get_starting_nodes(self) -> list[Node]:
        n = list()
        for name, node in self.m.items():
            if name.endswith('A'):
                n.append(node)
        return n
 
    
class Solver(object):
    def __init__(self, lines):
        instr = Instructions(lines[0])
        self.instructions = instr
        self.network = Network()

        r = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
        for l in lines[2:]:
            m = r.search(l)
            n = Node(m.group(1), m.group(2), m.group(3))
            self.network.add(n)

    def find_num_steps(self, start: str, end: str) -> int:
        steps = 0
        self.instructions.reset()
        curr = self.network.get(start)
        for instr in self.instructions:
            if curr.value == end:
                break
            if instr == LEFT:
                curr = self.network.get(curr.l)
            elif instr == RIGHT:
                curr = self.network.get(curr.r)
            steps += 1
        return steps

    def find_num_steps_for_all(self) -> int:
        steps = 0
        self.instructions.reset()
        curr_list = self.network.get_starting_nodes()
        for instr in self.instructions:
            done = 0
            for i in range(len(curr_list)):
                if curr_list[i].value.endswith('Z'):
                    done += 1
            if len(curr_list) == done:
                break
            for i in range(len(curr_list)):
                if instr == LEFT:
                    curr_list[i] = self.network.get(curr_list[i].l)
                elif instr == RIGHT:
                    curr_list[i] = self.network.get(curr_list[i].r)
            steps += 1

        return steps
                
                        

            

if __name__ == '__main__':
    r = tools.Reader('test_input.txt')
    lines = r.read()

    slvr = Solver(lines)
    x = slvr.find_num_steps('AAA', 'ZZZ')
    print(x)

    y = slvr.find_num_steps_for_all()
    print(y)


    r = tools.Reader('input.txt')
    lines = r.read()

    slvr = Solver(lines)
    x = slvr.find_num_steps('AAA', 'ZZZ')
    print(x)

    # y = slvr.find_num_steps_for_all()
    # print(y)

