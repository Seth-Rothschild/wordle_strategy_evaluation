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


def test_filter_all(game):
    words = st.filter_all(game)
    assert len(words) == 7


def test_get_letter_freq(game):
    apple_freqs = [{"a": 1}, {"p": 1}, {"p": 1}, {"l": 1}, {"e": 1}]
    assert apple_freqs == st.get_letter_freq(["apple"])
    total = st.get_letter_freq(game.words_list)
    assert total[0]["a"] == 141
    assert total[1]["a"] == 304
    assert total[2]["a"] == 307
    assert total[3]["a"] == 163
    assert total[4]["a"] == 64
