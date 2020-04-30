import json
import sys

from .vcard import gen_cards, nullcontext


def main(path):
    with open(path, 'r') if path else nullcontext(sys.stdin) as f:
        print(json.dumps([vcard.to_json() for vcard in gen_cards(f)], indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
