import sys
sys.path.append('../lib')

import tools
from functools import total_ordering

HIGH = 1
PAIR = 2
TPAIR = 3
THREE = 4
FHOUSE = 5
FOUR = 6
FIVE = 7 


DEFAULT_DECK = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
JOKER_DECK = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    

# using decorator for sorting
@total_ordering
class Hand(object):
    def __init__(self, cards, bid, deck=DEFAULT_DECK):
        self.cards = cards
        self.bid = bid
        self.card_values = deck
        self.power = 0

    def __str__(self):
        return f'cards: {self.cards}, bid: {self.bid}, power: {self.power}'

    def __lt__(self, obj):
        if self.power < obj.power:
            return True
        elif self.power == obj.power:
            for i in range(len(self.cards)):
                if self.card_values.index(self.cards[i]) < self.card_values.index(obj.cards[i]):
                    return True
                elif self.card_values.index(self.cards[i]) > self.card_values.index(obj.cards[i]):
                    return False
        return False

    def __eq__(self, obj):
        if self.power != obj.power:
            return False
        return self.cards == obj.cards



class HandDefaultDeck(Hand):
    def __init__ (self, cards, bid):
        super().__init__(cards, bid, deck=DEFAULT_DECK)
        self._power()

    def _power(self):
        counter = dict()
        for i in range(1, 4):
            counter[i] = set()
        # man this is ugly :)
        for label in self.cards:
            c = self.cards.count(label) 
            if c == 5:
                self.power = FIVE
                return
            elif c == 4:
                self.power = FOUR
                return
            else:
                counter[c].add(label)
        # end even uglier :)
        if len(counter[2]) > 0 and len(counter[3]) > 0:
            self.power = FHOUSE
        elif len(counter[3]) > 0:
            self.power = THREE
        elif len(counter[2]) > 1:
            self.power = TPAIR
        elif len(counter[2]) > 0:
            self.power = PAIR
        else:
            self.power = HIGH


class HandJokerDeck(Hand):
    def __init__ (self, cards, bid):
        super().__init__(cards, bid, deck=JOKER_DECK)
        self._power()

    def _power(self):
        counter = dict()
        for i in range(1, 5):
            counter[i] = set()

        jokers_count = 0
        # man this is ugly :)
        for label in self.cards:
            if label == 'J':
                jokers_count += 1
                continue
            c = self.cards.count(label) 
            if c == 5:
                # there are five cards of same label, 
                # no jokers, good
                self.power = FIVE
                return
            # otherwise we'll just memorize the counts
            else:
                counter[c].add(label)

        if len(counter[4]) > 0:
            self.power = FOUR
        if len(counter[2]) > 0 and len(counter[3]) > 0:
            self.power = FHOUSE
        elif len(counter[3]) > 0:
            self.power = THREE
        elif len(counter[2]) > 1:
            self.power = TPAIR
        elif len(counter[2]) > 0:
            self.power = PAIR
        else:
            self.power = HIGH

        # let's apply jokers
        for _ in range(jokers_count):
            if self.power == PAIR:
                self.power = THREE 
            elif self.power == TPAIR:
                self.power = FHOUSE
            elif self.power == THREE:
                self.power = FOUR 
            else:
                self.power += 1

            if self.power == FIVE:
                break
        
  
class HandsSet(object):
    def __init__(self, inp, hand_subclass=HandDefaultDeck):
        self.hands = []
        for line in inp:
            s = line.split()
            h = hand_subclass(s[0], int(s[1]))
            self.hands.append(h)

    def __str__(self):
        return '\n'.join(str(h) for h in self.hands)

    def sort(self):
        self.hands = sorted(self.hands)

    def get_total_winnings(self):
        self.sort()
        total = 0
        for rank, hand in enumerate(self.hands, start=1):
            total += (rank * hand.bid)
        return total


if __name__ == '__main__':
    r = tools.Reader('test_input.txt')
    lines = r.read()

    hs = HandsSet(lines)

    x = hs.get_total_winnings()
    print(x)

    hs = HandsSet(lines, hand_subclass=HandJokerDeck)
    hs.sort()
    #print(hs)

    y = hs.get_total_winnings()
    print(y)

    r = tools.Reader('input.txt')
    lines = r.read()

    hs = HandsSet(lines)

    x = hs.get_total_winnings()
    print(x)

    hs = HandsSet(lines, hand_subclass=HandJokerDeck)
    hs.sort()
    #print(hs)

    y = hs.get_total_winnings()
    print(y)
