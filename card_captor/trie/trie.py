from pathlib import Path
import json
import logging
import mtgsdk
import pickle

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TrieNode:
    def __init__(self):
        self.nodes = dict()
        self.card = None

    def add_word(self, word, card):
        if len(word) == 0:
            self.card = card
        else:
            c = word[0]
            if not c in self.nodes:
                self.nodes[c] = TrieNode()
            self.nodes[c].add_word(word[1:], card)

    def card_dist(self, word, c, prev_dists, maxdist, acc):
        new_dists = []
        card_valid = False
        new_word = acc + c
        for i in range(len(word) + 1):
            if i == 0:
                dist = len(acc) + 1
            else:
                diff_cost = 0 if c == word[i - 1] else 1
                dist = min(prev_dists[i - 1] + diff_cost,
                           prev_dists[i] + 1,
                           new_dists[i - 1] + 1)
            new_dists.append(dist)
            if dist <= maxdist:
                card_valid = True
        if not card_valid:
            return None
        if new_dists[-1] <= maxdist and self.card is not None:
            return self.card
        for c in self.nodes:
            res = self.nodes[c].card_dist(word, c, new_dists,
                                                  maxdist, new_word)
            if res:
                return res
        return None

class Trie:
    def __init__(self, cache_path=Path(Path.home(),
                                       ".cache/card_captor_magica/cards")):
        self.root = TrieNode()
        cache = Path(cache_path)
        if cache.is_file():
            logger.info("Loading card data from {}".format(cache))
            self._load_file(cache)
            logger.info("Cards loaded")
        else:
            logger.info("Downloading cards data...")
            self._load_mtg()
            logger.info("Saving to {}".format(cache))
            cache.parents[0].mkdir(exist_ok=True, parents=True)
            self._save_file(cache)

    def _load_mtg(self):
        for card in mtgsdk.card.Card.where().iter():
            self._add_card(card)

    def _save_file(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.root, f, pickle.HIGHEST_PROTOCOL)

    def _load_file(self, path):
        with open(path, "rb") as f:
            self.root = pickle.load(f)

    def _add_card(self, card):
        self.root.add_word(card.name, card)
        if card.foreign_names:
            for foreign in card.foreign_names:
                self.root.add_word(foreign["name"], card)


    def _card_dist(self, word, maxdist):
        first_dists = list(range(len(word) + 1))
        for c in self.root.nodes:
            res = self.root.nodes[c].card_dist(word, c, first_dists,
                                                 maxdist, "")
            if res:
                return res

    def find_closest(self, word, max_iter=2):
        word = word
        for i in range(max_iter + 1):
            res = self._card_dist(word, i)
            if res:
                return res
        return None


if __name__ == "__main__":
    t = Trie()
    assert(t.find_closest("Frissaon rampat") == "Frisson rampant")
