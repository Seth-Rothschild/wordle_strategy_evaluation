import random


def read_words(path):
    with open(path, "r") as f:
        words = f.readlines()
    words = [word[:5] for word in words]
    return words


DEFAULT_WORDS_LIST = read_words("solutions.txt")
DEFAULT_GUESSABLES = read_words("guessable_words.txt")


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
        self.guesses = []
        self.results = []
        self.duplicates = {}

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
            new_color_list = color_list[-1].copy()

        for i, value in enumerate(result):
            if attempt[i] not in new_color_list[i] and value == color:
                new_color_list[i] = new_color_list[i] + attempt[i]
        return new_color_list

    def _update_duplicates(self, attempt):
        if len(set(attempt)) == 5:
            return
        else:
            duplicates = {
                char: attempt.count(char) for char in attempt if attempt.count(char) > 1
            }
            for char, count in duplicates.items():
                target_count = self.target_word.count(char)

                if target_count == 0:
                    pass
                elif target_count == 1:
                    self.duplicates[char] = "exactly_one"
                elif target_count == 2 and count == 3:
                    self.duplicates[char] = "exactly_two"
                elif (target_count == 2 or target_count == 3) and count == 2:
                    self.duplicates[char] = "at_least_two"
                elif target_count == 3 and count == 3:
                    self.duplicates[char] = "exactly_three"

    def guess(self, attempt):
        result = [self._eval_guess(char, i) for i, char in enumerate(attempt)]
        if result == 5 * ["green"]:
            self.game_over = True

        self._update_duplicates(attempt)
        self.greens.append(self._update_color_list(attempt, result, "green"))
        self.yellows.append(self._update_color_list(attempt, result, "yellow"))
        self.greys.append(self._update_color_list(attempt, result, "grey"))
        self.guesses.append(attempt)
        self.results.append(result)

        self.move_counter = len(self.results)

        return result
