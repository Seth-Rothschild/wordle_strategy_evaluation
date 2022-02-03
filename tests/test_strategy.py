import pytest

import wordle_strategy_evaluation.strategy as st
from wordle_strategy_evaluation.game import Game


@pytest.fixture
def game():
    game = Game(target_word="apple")
    game.guess("pears")
    return game


def test_filter_greys(game):
    words = st.filter_greys(game, game.greys[-1])
    assert len(words) == 1025


def test_filter_yellows(game):
    words = st.filter_yellows(game, game.yellows[-1])
    assert len(words) == 13


def test_filter_greens(game):
    words = st.filter_greens(game, game.greens[-1])
    assert len(words) == 2315
    game.guess("areas")
    words = st.filter_greens(game, game.greens[-1])
    assert len(words) == 141


def test_filter_duplicates(game):
    words = st.filter_duplicates(game)
    assert len(words) == 2315
    game.guess("areas")
    words = st.filter_duplicates(game)
    assert len(words) == 839


def test_filter_all(game):
    words = st.filter_all(game)
    assert len(words) == 7


def test_get_letter_freq(game):
    apple_expected = [{"a": 1}, {"p": 1}, {"p": 1}, {"l": 1}, {"e": 1}]
    apple_real = st.get_letter_freq(["apple"])
    for real, expected in zip(apple_real, apple_expected):
        for key in expected.keys():
            assert real[key] == expected[key]

    total = st.get_letter_freq(game.words_list)
    assert total[0]["a"] == 141
    assert total[1]["a"] == 304
    assert total[2]["a"] == 307
    assert total[3]["a"] == 163
    assert total[4]["a"] == 64


def test_score(game):
    words_list = game.words_list
    freqs = st.get_letter_freq(words_list)
    assert st.score("apple", freqs) == 846
    assert st.score("pears", freqs) == 879
    assert st.score("peach", freqs) == 982
    assert freqs == st.DEFAULT_FREQS


def test_sort_dict():
    assert st._sort_dict({"b": 2, "c": 3}) == {"c": 3, "b": 2}


def test_score_words_list(game):
    words_list = game.words_list
    freqs = st.get_letter_freq(words_list)
    scores = st.score_words_list(words_list, freqs)
    assert len(scores) == len(words_list)
    assert scores == st.DEFAULT_SCORES


def test_cheat():
    game = Game()
    solved = st.cheat(game)
    assert solved.game_over
    assert solved.results[-1] == 5 * ["green"]
    assert solved.greens[-1] == [char for char in game.target_word]
    assert solved.move_counter == 1


def test_cheat_more():
    game = Game()
    solved = st.cheat_more(game)
    assert solved.game_over
    assert solved.move_counter == 0


def test_linear_select():
    game = Game()
    solved = st.linear_select(game)
    assert solved.game_over
    assert solved.words_list[solved.move_counter - 1] == game.target_word


def test_random_select():
    game = Game()
    solved = st.random_select(game)
    assert solved.game_over
    assert solved.move_counter > 10


def test_guess_by_freq():
    game = Game(target_word="apple")
    solved = st.guess_by_freq(game)
    assert solved.game_over
    assert solved.guesses == ["slate", "cable", "agile", "apple"]
    assert solved.move_counter == 4


def test_guess_by_updating_freq():
    game = Game(target_word="apple")
    solved = st.guess_by_updating_freq(game)
    assert solved.game_over
    print(solved.guesses)
    assert solved.guesses == ["slate", "maple", "apple"]
    assert solved.move_counter == 3


def test_run_trial():
    try_ten = st.run_trial(st.cheat, 10)
    assert len(try_ten) == 10
    score, error = st.evaluate_trial(try_ten)
    assert score == 1.0
    assert error == 0.0

    all_words = st.run_trial(st.cheat_more)
    assert len(all_words) == 2315
    score, error = st.evaluate_trial(all_words)
    assert score == 0.0
    assert error == 0.0
