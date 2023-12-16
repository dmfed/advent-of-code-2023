import sys
sys.path.append('../lib')

import tools, re

class Card(object):
    card_re = re.compile(r'Card +(\d+): ')
    def __init__(self, inp):
        m = self.card_re.search(inp)
        if not m:
            print(inp)
        self.card_num = m.group(1)
        inp = inp.replace(m.group(0), '')
        winning, have = inp.split('|')
        self.winning = [int(x) for x in winning.split()]
        self.have = [int(x) for x in have.split()]

    def __str__(self):
        s = 'card number: ' + self.card_num + '\n'
        s += 'winning: ' + ' '.join(str(x) for x in self.winning) + '\n'
        s += 'have: ' + ' '.join(str(x) for x in self.have) + '\n'
        return s

    def _count_winning_in_have(self):
        count = 0
        for x in self.winning:
            if x in self.have:
                count += 1
        return count

    def count_card_worth_points(self):
        n = self._count_winning_in_have()
        if n == 0:
            return 0
        worth = 1
        for _ in range(n-1):
            worth *= 2
        return worth
            

class CardSet(object):
    def __init__(self, inp):
        self.cards = []
        self.cards.extend([Card(l) for l in inp])

    def __str__(self):
        out = [str(card) for card in self.cards]
        return ''.join(out)

    def count_cards_worth(self) -> int:
        w = [c.count_card_worth_points() for c in self.cards]
        return sum(w)

    def count_total_copies(self):
        copies = [0 for _ in range(len(self.cards))]
        for i in range(len(self.cards)):
            copies[i] += 1
            matching = self.cards[i]._count_winning_in_have()
            if i + matching > len(self.cards):
                matching = len(self.cards) - 1 - i
            for j in range(1, matching+1):
                copies[i+j] += 1 * copies[i]
        return sum(copies)

if __name__ == '__main__':
    r = tools.Reader('input.txt')
    lines = r.read()

    cs = CardSet(lines)
    x = cs.count_cards_worth()
    print(x)

    y = cs.count_total_copies()
    print(y)

    
