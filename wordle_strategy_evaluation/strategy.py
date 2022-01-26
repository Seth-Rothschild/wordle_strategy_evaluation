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

    filtered = words_list
    filtered = filter_greens(game, game.greens[-1], filtered)
    filtered = filter_yellows(game, game.yellows[-1], filtered)
    filtered = filter_greys(game, game.greys[-1], filtered)
    return filtered


def _add_to_dict(dictionary, character):
    if character not in dictionary.keys():
        dictionary[character] = 1
    else:
        dictionary[character] += 1
    return dictionary


def get_letter_freq(words_list):
    position_counts = [{} for _ in range(5)]
    for word in words_list:
        for i, char in enumerate(word):
            position_counts[i] = _add_to_dict(position_counts[i], char)

    return position_counts
