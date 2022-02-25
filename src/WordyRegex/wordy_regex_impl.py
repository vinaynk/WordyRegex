
import re


class WordyRegexArgError(Exception):
    pass


def _pattern2str(pat):
    if isinstance(pat, str):
        return re.escape(pat)
    elif isinstance(pat, Pattern):
        return pat.getPattern()
    else:
        raise WordyRegexArgError('Expected input `str` or `Pattern` object')


class Pattern:

    def __init__(self, pattern='', escape=True):
        if not isinstance(pattern, str):
            raise WordyRegexArgError('Expects input to be a `str` object')
        if escape:
            pattern   = re.escape(pattern)
        self._pattern = pattern


    @staticmethod
    def lineStart():
        return Pattern('^', 0)


    @staticmethod
    def anyChar():
        return Pattern('.', 0)


    def getPattern(self):
        return self._pattern


    def __str__(self):
        return self._pattern


    def then(self, pat):
        return Pattern(self._pattern + _pattern2str(pat), 0)


    def lineEnd(self):
        return Pattern(self._pattern + '$', 0)


    def succeededBy(self, pat):
        pat = _pattern2str(pat)
        return Pattern(self._pattern + f'(?={pat})', 0)


    def succeededByNot(self, pat):
        pat = _pattern2str(pat)
        return Pattern(self._pattern + f'(?!{pat})', 0)


    def preceededBy(self, pat):
        pat = _pattern2str(pat)
        return Pattern(f'(?<={pat})' + self._pattern, 0)


    def preceededByNot(self, pat):
        pat = _pattern2str(pat)
        return Pattern(f'(?<!{pat})' + self._pattern, 0)


    def group(self, name=None, catch=True):
        if not catch:
            return Pattern(f'(?:{self._pattern})', 0)
        tgn = ''
        if name:
            tgn = f'?P<{name}>'
        return Pattern(f'({tgn}{self._pattern})', 0)


    @staticmethod
    def backrefByName(name):
        return Pattern(f'(?P={name})', 0)


    @staticmethod
    def backrefById(bid):
        return Pattern(f'\\{bid}', 0)


    @staticmethod
    def condGroupMatch(name, pat1, pat2=''):
        pat1 = _pattern2str(pat1)
        pat2 = _pattern2str(pat2)
        return Pattern(f'(?({name}){pat1}|{pat2})', 0)


    def zeroOrMore(self, greedy=True):
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}*{qm}', 0)


    def oneOrMore(self, greedy=True):
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}+{qm}', 0)


    def zeroOrOne(self, greedy=True):
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}?{qm}', 0)


    def optional(self, greedy=True):
        return self.zeroOrOne(greedy)


    def repeat(self, exact='', min='', max='', greedy=True):
        if min != '' and max != '' and int(min) >= int(max):
            raise WordyRegexArgError(f'{min=} should be smaller than {max=}')
        qm = '' if greedy else '?'
        if exact :
            return Pattern(f'{self._pattern}{{{exact}}}', 0)
        return Pattern(f'{self._pattern}{{{min}-{max}}}{qm}', 0)


    @staticmethod
    def anyOf(*agrs):
        parts = [ _pattern2str(it) for it in args ]
        return Pattern('|'.join(parts))


    def compile(self, flags=0):
        return re.compile(self._pattern, flags)



class Special:
    strStart = Pattern(r'\A')
    strEnd   = Pattern(r'\Z')
    digit    = Pattern(r'\d')
    nonDigit = Pattern(r'\D')
    space    = Pattern(r'\s')
    nonSpace = Pattern(r'\S')
    wordchar    = Pattern(r'\w')
    nonWordchar = Pattern(r'\W')
    wordBoundary    = Pattern(r'\b')
    nonWordBoundary = Pattern(r'\B')


class CharSet:

    @staticmethod
    def _escape(pat):
        escapeNeeded = r'^-]'
        pat = pat.replace('\\', '\\\\')
        for ch in escapeNeeded:
            pat = pat.replace(ch, '\\'+ch)
        return pat


    @staticmethod
    def charset(pat='', digit=False, lower=False, upper=False,
                reverse=False, alphanum=False):
        pat  = CharSet._escape(pat)
        expr = ''
        if alphanum:
            expr += '0-9a-zA-Z'
        else:
            if digit: expr += '0-9'
            if lower: expr += 'a-z'
            if upper: expr += 'A-Z'
        rev  = '^' if reverse else ''
        expr = f'[{rev}{expr}{pat}]'
        return Pattern(expr, 0)



