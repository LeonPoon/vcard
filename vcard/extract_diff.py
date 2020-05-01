import sys

from .vcard import nullcontext


def main(argv):
    path = argv[0] if argv else None
    state = None
    with open(path, 'r') if path else nullcontext(sys.stdin) as f:
        for line in f:
            if state == '-' and line.startswith(state):
                print(line[1:], end='')
            elif line.startswith('@'):
                state = line[2 + line[2:].find('@@') + 3]


if __name__ == '__main__':
    main(sys.argv[1:])
