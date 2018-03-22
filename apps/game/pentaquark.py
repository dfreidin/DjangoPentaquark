from random import shuffle, random

class Quark(object):
    COLOR_LOOKUP = {
        1: "red",
        2: "green",
        4: "blue"
    }
    # no "top" quarks in the base game
    FLAVORS = [
        "up",
        "down",
        "charm",
        "strange",
        "bottom"
    ]
    def __init__(self, color, flavor):
        self.color = color
        self.flavor = flavor
        self.anti = False
    def flip(self):
        self.anti = not self.anti
    def type(self):
        # for use in templates
        return "Quark"

class Hadron(object):
    def __init__(self, quarks):
        self.quarks = quarks[:]
    def type(self):
        # for use in templates
        return "Hadron"

class Annihilator(object):
    def __init__(self):
        pass
    def flip(self):
        pass

class Deck(object):
    def __init__(self):
        self.deck = []
        for f in Quark.FLAVORS:
            for c in Quark.COLOR_LOOKUP.iterkeys:
                self.deck.append(Quark(c, f))
        shuffle(self.deck)
        if random >= 0.5:
            for q in self.deck[:8]:
                q.flip()
        else:
            for q in self.deck[:7]:
                q.flip()
        shuffle(self.deck)
        self.discard = []
    def draw(self):
        return self.deck.pop()
    def discard(self, quark):
        self.discard.append(quark)
    def is_empty(self):
        return len(deck) == 0
    def shuffle(self):
        self.deck = self.discard
        self.discard = []
        for q in self.deck:
            q.flip()
        shuffle(self.deck)
    def top(self):
        return 

class Game(object):
    def __init__(self):
        self.deck = Deck()
        self.beam = []
        self.background = []
        self.detector = []
    def check_confine(self, quarks):
        if len(quarks) == 2:
            if quarks[0].color == quarks[1].color and quarks[0].anti != quarks[1].anti:
                return True
            else:
                return False
        elif len(quarks) == 3:
            if sum(q.color for q in quarks) == 7 and quarks[0].anti == quarks[1].anti and quarks[0].anti == quarks[2].anti:
                return True
            else:
                return False
        else:
            return False
    def draw_phase(self):
        # while beam size < 3
        while len(self.beam) < 3:
            # draw a card
            new_card = self.deck.draw()
            # check for annihilate cards
            if isinstance(new_card, Annihilator):
                # TODO: annihilate a free quark
                self.deck.discard(new_card)
            else:
                self.beam.append(new_card)
            # check for empty
            if self.deck.is_empty():
                # refresh phase
                # discard free quarks at the detector
                for q in self.detector:
                    if isinstance(q, Quark):
                        self.detector.remove(q)
                        self.deck.discard(q)
                # discard confined quarks in background
                # annihilate remaining free quarks
                for h in self.background:
                    self.background.remove(h)
                    if not isinstance(h, Quark):
                        for q in h:
                            self.deck.discard(q)
                # check for loss
                # add 1 annihilate card, then shuffle/flip
                self.deck.discard(Annihilator())
                self.deck.shuffle()
                pass

    # move from beam
    def collider_phase(self, background_idx, detector_idx, discard_idx):
        self.background.append(self.beam[background_idx])
        self.detector.append(self.beam[detector_idx])
        self.deck.discard(self.beam[discard_idx])
        self.beam = []
    # check for annihilations in background or detector
    # adjust confinements (create or break hadrons)