import contextlib
import re
import sys


class Content(object):

    def __init__(self, group, name, value):
        self.group = group
        self.name = name
        self.params = []
        self.values = [value]

    def vcard_lines(self, card):
        yield card.eoll('%s%s%s:%s' % (
            ('%s.' % self.group) if self.group else '',
            self.name,
            ''.join(';%s=%s' % param for param in self.params),
            self.values[0],
        ))
        for val in self.values[1:]:
            yield card.eoll(' %s' % val)

    def to_json(self):
        return ('%s%s' % (('%s.' % self.group) if self.group else '',
                          self.name
                          ),
                tuple(self.params), 'text', ''.join(self.values))


class Card(object):
    alpha_digit_dash = re.compile('[A-Za-z0-9-]')
    multi_alpha_digit_dash = re.compile('(%s)+' % alpha_digit_dash.pattern)
    start_with_group = re.compile(r'^(%s)\.' % alpha_digit_dash.pattern)
    start_with_name = re.compile(r'^(%s)' % alpha_digit_dash.pattern)
    param_value = re.compile(r'"[^"]*"|[^:;]*')
    param = re.compile(r';(%s)=(%s)' % (multi_alpha_digit_dash.pattern, param_value.pattern))
    start_with_param = re.compile(r'^(%s)' % param.pattern)
    line = re.compile(r'^((%(m)s)\.)?(%(m)s)((%(p)s)*):(.*)$' % {
        'm': multi_alpha_digit_dash.pattern,
        'p': param.pattern,
    })

    current_content = None
    end = None

    def __init__(self, begin, eol):
        self.begin = begin
        self.eol = eol
        self.contents = []

    def got(self, line):
        assert line.endswith(self.eol)
        line = line[:-len(self.eol)]
        if line == 'END:VCARD':
            del self.current_content
            self.end = line
            return self
        self.parse_content_line(line)

    def parse_content_line(self, line):
        if line.startswith(' '):
            return self.continuation(line[1:])
        match = self.line.match(line)
        group = match.group(2)
        name = match.group(4)
        params = match.group(6)
        value = match.group(11)
        self.current_content = Content(group, name, self.parse_value(value))
        while params:
            match = self.start_with_param.match(params)
            name = match.group(2)
            value = match.group(4)
            params = params[len(match.group(0)):]
            self.current_content.params.append((name, value))
        self.contents.append(self.current_content)

    def continuation(self, value):
        self.current_content.values.append(self.parse_value(value))

    @staticmethod
    def parse_value(value):
        return value

    def vcard_lines(self):
        yield self.eoll(self.begin)
        for content in self.contents:
            yield from content.vcard_lines(self)
        yield self.eoll(self.end)

    def eoll(self, line):
        return '%s%s' % (line, self.eol)

    def to_json(self, names=None):
        return ("vcard",
                tuple(sorted(content.to_json() for content in self.contents if not names or content.name in names))
                )


@contextlib.contextmanager
def nullcontext(o):
    yield o


def gen_cards(lines):
    card = None
    for line in lines:
        if card:
            ret = card.got(line)
            if ret:
                yield ret
                card = None
        elif line == 'BEGIN:VCARD\r\n':
            card = Card(line.rstrip(), '\r\n')
        elif line == 'BEGIN:VCARD\n':
            card = Card(line.rstrip(), '\n')
        else:
            raise Exception('no current card and not begin: %r' % line)


def main(path):
    with open(path, 'r') if path else nullcontext(sys.stdin) as f:
        print(''.join(''.join(vcard.vcard_lines()) for vcard in gen_cards(f)), end='')


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
