import sys
sys.path.append('../lib')

import tools

class History(object):
    def __init__(self, nums: list[int]):
        self.history = nums

    def __str__(self):
        return ' '.join(str(n) for n in self.history)

    def extrapolate_forward(self):
        ends = list()
        curr = self.history.copy()
        while not all([True if n == 0 else False for n in curr]):
            ends.append(curr[-1])
            curr = [curr[i+1] - curr[i] for i in range(len(curr)-1)]
        new_val = sum(ends)
        self.history.append(new_val)

    def extrapolate_backward(self):
        starts = list()
        curr = self.history.copy()
        while not all([True if n == 0 else False for n in curr]):
            starts.append(curr[0])
            curr = [curr[i+1] - curr[i] for i in range(len(curr)-1)]
        new_val = 0
        for n in reversed(starts):
            new_val = n - new_val
        self.history.insert(0, new_val)

    def get_last_value(self):
        return self.history[-1]
            
    def get_first_value(self):
        return self.history[0]
            
        

class Report(object):
    def __init__(self, lines):
        self.histories = list()
        for line in lines:
            values = [int(n) for n in line.split()]
            h = History(values)
            self.histories.append(h)

    def __str__(self):
        out = f'Histories:\n'
        for h in self.histories:
            out += str(h) + '\n'
        return out

    def extrapolate_all_forward(self):
        for h in self.histories:
            h.extrapolate_forward()

    def extapolate_all_backwards(self):
        for h in self.histories:
            h.extrapolate_backward()

    def get_sum_of_last_values(self) -> int:
        total = sum([h.get_last_value() for h in self.histories])
        return total

    def get_sum_of_first_values(self) -> int:
        total = sum([h.get_first_value() for h in self.histories])
        return total


if __name__ == '__main__':
    r = tools.Reader('test_input.txt')
    lines = r.read()

    r = Report(lines)
    r.extrapolate_all_forward()
    r.extapolate_all_backwards()
    print(r)

    x = r.get_sum_of_last_values()
    print(x)

    y = r.get_sum_of_first_values()
    print(y)

    r = tools.Reader('input.txt')
    lines = r.read()

    r = Report(lines)
    r.extrapolate_all_forward()
    r.extapolate_all_backwards()

    x = r.get_sum_of_last_values()
    print(x)
    y = r.get_sum_of_first_values()
    print(y)

