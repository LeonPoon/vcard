import json
import os
import sys
from difflib import Differ
from typing import Callable, TypeVar, Generator, Any

from . import vcard
from .sort import DEFAULT_NAMES

T = TypeVar('T')


def gen_cards(path):
    with open(path, 'r') as path:
        yield from vcard.gen_cards(path)


def apply_map(f: Callable[..., T], diff_args, *same) -> Generator[T, Any, None]:
    for args in diff_args:
        yield f(*(args + same))


def diff_header(a, b):
    print('--- %s' % a)
    print('+++ %s' % b)


def diff_section(card, prefix, names, j=None):
    print('@@ @@ %s%s' % (prefix, json.dumps(j or card.to_json(names))))


def print_whole_card(card, prefix, cards, names, j=None):
    diff_section(card, prefix, names, j)
    for line in card.vcard_lines():
        print('%s%s' % (prefix, line), end='')
    return next(cards, None)


def print_diff(card_a, card_b, j):
    diff_section(card_a, ' ', None, j)
    lines_a, lines_b = apply_map(lambda card: tuple(card.vcard_lines()), ((card_a,), (card_b,)))
    for line in Differ().compare(lines_a, lines_b):
        if not line.startswith('?'):
            print(''.join((line[0], line[2:])), end='')


def main(argv):
    path_a, path_b, names = argv[0], argv[1], argv[2:]
    if not names:
        names = DEFAULT_NAMES
    cards_a, cards_b = apply_map(gen_cards, ((path_a,), (path_b,)))
    card_a, card_b = apply_map(lambda g: next(g, None), ((cards_a,), (cards_b,)))
    h = diff_header
    while card_a or card_b:
        if h:
            h(path_a, path_b)
            h = None
        if card_a and not card_b:
            card_a = print_whole_card(card_a, '-', cards_a, names)
        elif (not card_a) and card_b:
            card_b = print_whole_card(card_b, '+', cards_b, names)
        else:
            json_a, json_b = apply_map(lambda card: card.to_json(names), ((card_a,), (card_b,)))
            if json_a < json_b:
                card_a = print_whole_card(card_a, '-', cards_a, names, json_a)
            elif json_a > json_b:
                card_b = print_whole_card(card_b, '+', cards_b, names, json_b)
            else:
                if card_a.eol != card_b.eol:
                    card_a.eol = card_b.eol = os.linesep
                print_diff(card_a, card_b, json_a)
                card_a, card_b = apply_map(lambda g: next(g, None), ((cards_a,), (cards_b,)))


if __name__ == "__main__":
    main(sys.argv[1:])
