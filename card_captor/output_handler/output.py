from mtgsdk import Card

class Output():
    def __init__(self):
            self.last_seen = None
            self.cards_set = {}

    def add_card(self, card):
        if isinstance(card, Card):
            card = card.name
        if self.last_seen == card:
            return
        self.last_seen = card
        if card in self.cards_set:
            self.cards_set[card] += 1
        else:
            self.cards_set[card] = 1

    def remove_card(self, card):
        if isinstance(card, Card):
            card = card.name
        if card in self.cards_set:
            self.cards_set[card] -= 1
            if self.cards_set[card] == 0:
                del self.cards_set[card]

    def print_list(self):
        for card, amount in self.cards_set.items():
            print(str(amount) + " " + card)
