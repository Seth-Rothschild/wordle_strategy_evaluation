import string
import random
import math
from statistics import mean, stdev

from wordle_strategy_evaluation.game import DEFAULT_WORDS_LIST, Game


def filter_greens(game, greens, words_list=None):
    if words_list is None:
        words_list = game.words_list

    filtered = words_list
    for i, char in enumerate(greens):
        if char != "":
            filtered = [word for word in filtered if word[i] == char]
    return filtered


def filter_yellows(game, yellows, words_list=None):
    if words_list is None:
        words_list = game.words_list

    filtered = words_list
    for i, targets in enumerate(yellows):
        if len(targets) > 0:
            for char in targets:
                filtered = [
                    word for word in filtered if (word[i] != char and char in word)
                ]
    return filtered


def filter_greys(game, greys, words_list=None):
    if words_list is None:
        words_list = game.words_list

    filtered = words_list

    greys = set("".join(greys))
    for char in greys:
        filtered = [word for word in filtered if char not in word]
    return filtered


def filter_all(game, words_list=None):
    if words_list is None:
        words_list = game.words_list

    if game.move_counter == 0:
        greens = yellows = greys = 5 * [""]
    else:
        greens, yellows, greys = (game.greens[-1], game.yellows[-1], game.greys[-1])

    filtered = words_list
    filtered = filter_greens(game, greens, filtered)
    filtered = filter_yellows(game, yellows, filtered)
    filtered = filter_greys(game, greys, filtered)
    return filtered


def get_letter_freq(words_list):
    position_counts = [{char: 0 for char in string.ascii_lowercase} for _ in range(5)]
    for word in words_list:
        for i, char in enumerate(word):
            position_counts[i][char] += 1  # _add_to_dict(position_counts[i], char)
    return position_counts


def score(word, position_counts):
    score = 0
    for char, counts in zip(word, position_counts):
        score += counts[char]
    return score


def _sort_dict(dictionary):
    return {
        k: v
        for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    }


def score_words_list(words, position_counts):
    return _sort_dict({word: score(word, position_counts) for word in words})


def cheat(game):
    game.guess(game.target_word)
    return game


def cheat_more(game):
    game.game_over = True
    return game


def linear_select(game):
    for guess in DEFAULT_WORDS_LIST:
        game.guess(guess)
        if game.game_over:
            return game


def random_select(game):
    while not game.game_over:
        guess = random.choice(game.words_list)
        game.guess(guess)
    return game


def guess_by_freq(game):
    filtered = DEFAULT_WORDS_LIST
    while not game.game_over:
        filtered = filter_all(game)
        guess = list(score_words_list(filtered, DEFAULT_FREQS).keys())[0]
        game.guess(guess)
    return game


def guess_by_updating_freq(game):
    filtered = DEFAULT_WORDS_LIST
    while not game.game_over:
        filtered = filter_all(game)
        freqs = get_letter_freq(filtered)
        guess = list(score_words_list(filtered, freqs).keys())[0]
        game.guess(guess)
    return game


def run_trial(strategy, nruns=None):
    if not nruns:
        return [strategy(Game(target_word=word)) for word in DEFAULT_WORDS_LIST]
    else:
        return [strategy(Game()) for _ in range(nruns)]


def evaluate_trial(trial, stdevs=2):
    scores = [game.move_counter for game in trial]
    return mean(scores), stdevs * stdev(scores) / math.sqrt(len(scores))


DEFAULT_FREQS = get_letter_freq(DEFAULT_WORDS_LIST)
DEFAULT_SCORES = score_words_list(DEFAULT_WORDS_LIST, DEFAULT_FREQS)
STRATEGIES = [
    cheat,
    cheat_more,
    linear_select,
    random_select,
    guess_by_freq,
    guess_by_updating_freq,
]
