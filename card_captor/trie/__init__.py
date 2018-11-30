import pickle
import json

class TrieNode:
    def __init__(self):
        self.nodes = dict()
        self.exists = False

    def add_word(self, word):
        if len(word) == 0:
            self.exists = True
        else:
            c = word[0]
            if not c in self.nodes:
                self.nodes[c] = TrieNode()
            self.nodes[c].add_word(word[1:])

    def exists_dist(self, word, c, prev_dists, maxdist, acc):
        new_dists = []
        exists_valid = False
        new_word = acc + c
        for i in range(len(word) + 1):
            if i == 0:
                dist = len(acc) + 1
            else:
                diff_cost = 0 if c.upper() == word[i - 1] else 1
                dist = min(prev_dists[i - 1] + diff_cost,
                           prev_dists[i] + 1,
                           new_dists[i - 1] + 1)
            new_dists.append(dist)
            if dist <= maxdist:
                exists_valid = True
        if not exists_valid:
            return ""
        if new_dists[-1] <= maxdist and self.exists:
            return new_word
        for c in self.nodes:
            res = self.nodes[c].exists_dist(word, c, new_dists,
                                                  maxdist, new_word)
            if res:
                return res
        return ""

class Trie:
    def __init__(self, dict_path=None, save_path=None):
        self.root = TrieNode()
        assert(dict_path is None or save_path is None)
        if dict_path:
            self.read_dict(dict_path)
        elif save_path:
            self.load_file(save_path)

    def read_dict(self, path):
        with open(path, "r") as f:
            try:
                # Assuming a json format similar to http://mtgjson.com/
                data = json.load(f)
                for card in data.keys():
                    self.root.add_word(card.upper())
            except:
                for line in f:
                    self.root.add_word(line.upper())

    def save_file(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.root, f, pickle.HIGHEST_PROTOCOL)

    def load_file(self, path):
        with open(path, "rb") as f:
            self.root = pickle.load(f)


    def _exists_dist(self, word, maxdist):
        first_dists = list(range(len(word) + 1))
        for c in self.root.nodes:
            res = self.root.nodes[c].exists_dist(word, c, first_dists,
                                                 maxdist, "")
            if res:
                return res

    def find_closest(self, word, max_iter=3):
        word = word.upper()
        for i in range(max_iter + 1):
            res = self._exists_dist(word, i)
            if res:
                return res
        return ""
