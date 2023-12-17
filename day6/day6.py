import sys
sys.path.append('../lib')

import tools

class Race(object):
    def __init__(self, duration, distance):
        self.duration = duration
        self.distance = distance

    def __str__(self):
        return f'Time: {self.duration}, Distance: {self.distance}'

    def calc_winning_strategies(self) -> list:
        winning_press_durations = []
        for dur in range(1, self.duration):
            if ((self.duration - dur) * dur) > self.distance:
                winning_press_durations.append(dur)
        return winning_press_durations
        

class RaceSet(object):
    def __init__(self, inp, join_input=False):
        if join_input:
            times = [int(''.join([n for n in inp[0].split(':')[1].split()]))]
            distances = [int(''.join([n for n in inp[1].split(':')[1].split()]))]
        else:
            times = [int(n) for n in inp[0].split(':')[1].split()]
            distances = [int(n) for n in inp[1].split(':')[1].split()]
        assert len(times) == len(distances)

        self.races = []
        for i in range(len(times)):
            r = Race(times[i], distances[i])
            self.races.append(r)

    def __str__(self):
        out = f'Set of {len(self.races)} races:\n'
        out += "\n".join([str(r) for r in self.races])
        return out

    def calc_product_of_winning_strategies(self) -> int:
        product = 1
        for r in self.races:
            strategies = r.calc_winning_strategies()
            product *= len(strategies)
        return product
        
        

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    races = RaceSet(lines)
    print(races)

    x = races.calc_product_of_winning_strategies()
    print(x)
    
    races = RaceSet(lines, join_input=True)
    print(races)

    x = races.calc_product_of_winning_strategies()
    print(x)
    

    
