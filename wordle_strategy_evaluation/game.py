import random


def read_words(path):
    with open(path, "r") as f:
        words = f.readlines()
    words = [word[:5] for word in words]
    return words


DEFAULT_WORDS_LIST = read_words("words.txt")


class Game:
    def __init__(self, target_word=None, words_list=None):
        if words_list is None:
            words_list = DEFAULT_WORDS_LIST
        if target_word is None:
            target_word = random.choice(words_list)
        else:
            if target_word not in words_list:
                raise ValueError

        self.target_word = target_word
        self.words_list = words_list
        self.move_counter = 0
        self.game_over = False
        self.greens = []
        self.yellows = []
        self.greys = []
        self.results = []

    def _eval_guess(self, guess_char, index):
        if guess_char == self.target_word[index]:
            return "green"
        elif guess_char in self.target_word:
            return "yellow"
        else:
            return "grey"

    def _get_color_list(self, color):
        if color == "green":
            return self.greens
        if color == "yellow":
            return self.yellows
        if color == "grey":
            return self.greys

    def _update_color_list(self, attempt, result, color):
        color_list = self._get_color_list(color)
        if not len(color_list):
            new_color_list = 5 * [""]
        else:
            new_color_list = color_list[-1]

        for i, value in enumerate(result):
            if attempt[i] not in new_color_list[i] and value == color:
                new_color_list[i] = new_color_list[i] + attempt[i]
        return new_color_list

    def guess(self, attempt):
        result = [self._eval_guess(char, i) for i, char in enumerate(attempt)]
        if result == 5 * ["green"]:
            self.game_over = True

        self.greens.append(self._update_color_list(attempt, result, "green"))
        self.yellows.append(self._update_color_list(attempt, result, "yellow"))
        self.greys.append(self._update_color_list(attempt, result, "grey"))
        self.results.append(result)

        self.move_counter = len(self.results)

        return result
