import pytest
from wordle_strategy_evaluation.game import Game


def test_init():
    """When the Game class is initialized
    There should be a target_word
    There should be a words_list
    There should be a game_over flag
    There should be a move_counter
    """
    game = Game()
    assert len(game.target_word) == 5
    assert len(game.words_list) == 2315
    assert game.game_over is False
    assert game.move_counter == 0


def test_passed_arguments():
    """When the Game class is initialized with arguments
    Those arguments should be attributes of the class
    """
    target_word = "apple"
    words_list = ["apple", "pears", "peach", "grape"]
    game = Game(target_word=target_word, words_list=words_list)
    assert game.target_word == target_word
    assert game.words_list == words_list


def test_word_in_words_list():
    """When a target_word is passed not in the words list
    There should be a ValueError
    """
    with pytest.raises(ValueError):
        Game(target_word="aaaaa")


def test_result():
    """When guess is called
    Letters that match should be green, in word yellow, else grey
    """
    game = Game(target_word="awake")
    result = game.guess("pears")
    assert result == ["grey", "yellow", "green", "grey", "grey"]
    assert game.results[0] == result


def test_increment():
    """When guess is called
    The move_counter should increment on guess
    """
    game = Game()
    game.guess("awake")
    assert game.move_counter == 1


def test_solve():
    """When guess is called
    The game_over flag should be set if the guess is correct
    """
    game = Game(target_word="awake")
    game.guess("awake")
    assert game.game_over


def test_color_arrays():
    """Check that arrays of what has been found are properly constructed
    Note that we want to hold on to the history of what is known at each guess
    to make analysis easier later.

    1. The last element of each color array represents the best knowledge to use
    for a guess.

    2. This is a slightly bad data structure for greys, but it's easier to remember
    how to use these if they all match.

    """
    game = Game(target_word="awake")
    game.guess("pears")
    assert game.greys == [["p", "", "", "r", "s"]]
    assert game.yellows == [["", "e", "", "", ""]]
    assert game.greens == [["", "", "a", "", ""]]

    game.guess("grape")
    assert game.greys[-1] == ["pg", "r", "", "rp", "s"]
    assert game.yellows[-1] == ["", "e", "", "", ""]
    assert game.greens[-1] == ["", "", "a", "", "e"]

    game.guess("awake")
    assert game.greys[-1] == ["pg", "r", "", "rp", "s"]
    assert game.yellows[-1] == ["", "e", "", "", ""]
    assert game.greens[-1] == ["a", "w", "a", "k", "e"]
