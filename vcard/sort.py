import sys

from .vcard import gen_cards, nullcontext

DEFAULT_NAMES = ('FN', 'N', 'EMAIL', 'TEL')


def vcards_sorted(f, names):
    return sorted((vcard.to_json(names=names or DEFAULT_NAMES), vcard) for vcard in gen_cards(f))


def main(names):
    with nullcontext(sys.stdin) as f:
        for vcard in tuple(zip(*vcards_sorted(f, names)))[-1]:
            print(''.join(vcard.vcard_lines()).replace('\xa0', ' '), end='')


if __name__ == "__main__":
    main(sys.argv[1:])
