
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
        '''
        Creates a pattern object
        - `pattern` (str) input (usually non-regex)
        - escape (bool) whether to escape pattern using re.escape
        '''
        if not isinstance(pattern, str):
            raise WordyRegexArgError('Expects input to be a `str` object')
        if escape:
            pattern   = re.escape(pattern)
        self._pattern = pattern


    def then(self, pat):
        'returns a new pattern concatenating current one with `pat`'
        return Pattern(self._pattern + _pattern2str(pat), 0)


    @staticmethod
    def lineStart():
        'creates a pattern that matches line start'
        return Pattern('^', 0)


    def lineEnd(self):
        'adds a line end'
        return Pattern(self._pattern + '$', 0)


    @staticmethod
    def anyChar():
        'creates a pattern that match any single char'
        return Pattern('.', 0)


    def getPattern(self):
        'get the regex patten of this Pattern object'
        return self._pattern


    def __str__(self):
        return self._pattern


    def succeededBy(self, pat):
        '''
        specifies that current pattern should be succeeded by `pat`
        - does not absorb `pat` in matching
        '''
        pat = _pattern2str(pat)
        return Pattern(self._pattern + f'(?={pat})', 0)


    def succeededByNot(self, pat):
        '''
        specifies that current pattern should not be succeeded by `pat`
        - does not absorb `pat` in matching
        '''
        pat = _pattern2str(pat)
        return Pattern(self._pattern + f'(?!{pat})', 0)


    @staticmethod
    def preceededBy(pat):
        '''
        specifies that current pattern should be preceeded by `pat`
        - does not absorb `pat` in matching
        '''
        pat = _pattern2str(pat)
        return Pattern(f'(?<={pat})', 0)


    @staticmethod
    def preceededByNot(pat):
        '''
        specifies that current pattern should not be preceeded by `pat`
        - does not absorb `pat` in matching
        '''
        pat = _pattern2str(pat)
        return Pattern(f'(?<!{pat})', 0)


    def group(self, name=None, catch=True):
        'groups the current pattern'
        if not catch:
            return Pattern(f'(?:{self._pattern})', 0)
        tgn = ''
        if name:
            tgn = f'?P<{name}>'
        return Pattern(f'({tgn}{self._pattern})', 0)


    @staticmethod
    def backrefByName(name):
        'back reference a group by name'
        return Pattern(f'(?P={name})', 0)


    @staticmethod
    def backrefById(bid):
        'back reference a group by id'
        return Pattern(f'\\{bid}', 0)


    @staticmethod
    def condGroupMatch(name, pat1, pat2=''):
        'conditionally match group with given `name` to `pat1` or `pat2`'
        pat1 = _pattern2str(pat1)
        pat2 = _pattern2str(pat2)
        return Pattern(f'(?({name}){pat1}|{pat2})', 0)


    def zeroOrMore(self, greedy=True):
        'zero or more repeats of current pattern (if grouped)'
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}*{qm}', 0)


    def oneOrMore(self, greedy=True):
        'one or more repeats of current pattern (if grouped)'
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}+{qm}', 0)


    def zeroOrOne(self, greedy=True):
        'zero or one repeats of current pattern (if grouped)'
        qm = '' if greedy else '?'
        return Pattern(f'{self._pattern}?{qm}', 0)


    def optional(self, greedy=True):
        'current pattern (if groupd) is optional'
        return self.zeroOrOne(greedy)


    def repeat(self, exact='', min='', max='', greedy=True):
        if min != '' and max != '' and int(min) >= int(max):
            raise WordyRegexArgError(f'{min=} should be smaller than {max=}')
        qm = '' if greedy else '?'
        if exact :
            return Pattern(f'{self._pattern}{{{exact}}}', 0)
        return Pattern(f'{self._pattern}{{{min},{max}}}{qm}', 0)


    @staticmethod
    def anyOf(*args, group=True):
        'create regex that matches any of the supplied patterns'
        parts = [ _pattern2str(it) for it in args ]
        joined = '|'.join(parts)
        if group:
            joined = f'({joined})'
        return Pattern(joined, 0)


    @staticmethod
    def seq(*args):
        'concatenates supplied patterns'
        parts = [ _pattern2str(it) for it in args ]
        return Pattern(''.join(parts), 0)


    def compile(self, flags=0):
        'compile the current pattern'
        return re.compile(self._pattern, flags)


class CharSet:

    strStart = Pattern(r'\A', 0)
    strEnd   = Pattern(r'\Z', 0)
    digit    = Pattern(r'\d', 0)
    nonDigit = Pattern(r'\D', 0)
    space    = Pattern(r'\s', 0)
    nonSpace = Pattern(r'\S', 0)
    wordChar    = Pattern(r'\w', 0)
    nonWordChar = Pattern(r'\W', 0)
    wordBoundary    = Pattern(r'\b', 0)
    nonWordBoundary = Pattern(r'\B', 0)
    lineStart       = Pattern('^', 0)
    lineEnd = Pattern('$', 0)
    anyChar = Pattern('.', 0)

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
        'creates a charset'
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



