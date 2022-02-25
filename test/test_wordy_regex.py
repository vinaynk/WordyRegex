

import sys
import os
import unittest


moduleDir = os.path.abspath( os.path.dirname( __file__ ) + '/../src/' )
sys.path.insert(0, moduleDir)
from WordyRegex import WordyRegexArgError, Pattern, Special, CharSet


class TestStringMethods(unittest.TestCase):

    def test_then(self):
        p1  = Pattern('hello').then(' world').then('!')
        rp1 = p1.getPattern()
        self.assertEqual(rp1, r'hello\ world!')


    def test_lineStartEnd(self):
        p1  = Pattern('hello').lineEnd()
        rp1 = p1.getPattern()
        self.assertEqual(rp1, 'hello$')

        p1  = Pattern.lineStart().then('hello').lineEnd()
        rp1 = p1.getPattern()
        self.assertEqual(rp1, '^hello$')


    def test_lookahead(self):
        p1  = Pattern('hello').succeededBy(' world')
        rp1 = p1.getPattern()
        self.assertEqual(rp1, r'hello(?=\ world)')

        p1  = Pattern('hello').succeededByNot(' world')
        rp1 = p1.getPattern()
        self.assertEqual(rp1, r'hello(?!\ world)')

        p1  = Pattern('world').preceededBy('hello ')
        rp1 = p1.getPattern()
        self.assertEqual(rp1, r'(?<=hello\ )world')

        p1  = Pattern('world').preceededByNot('hello ')
        rp1 = p1.getPattern()
        self.assertEqual(rp1, r'(?<!hello\ )world')


    def test_repeat(self):
        ptstr = 'hel'
        p0  = Pattern(ptstr)
        char = '*+?'
        for fn, fnch in zip([ p0.zeroOrMore, p0.oneOrMore, p0.zeroOrOne ], '*+?'):
            for grd, grdch in zip([ True, False ], [ '', '?' ]):
                res = fn(greedy=grd).then('o').getPattern()
                exp = f'{ptstr}{fnch}{grdch}o'
                self.assertEqual(res, exp)


    def test_group(self):
        p0 = Pattern('hello')
        p1 = p0.group(catch=False)
        self.assertEqual(str(p1), '(?:hello)')
        p1 = p0.group(catch=True)
        self.assertEqual(str(p1), '(hello)')
        p1 = p0.group(name='word')
        self.assertEqual(str(p1), '(?P<word>hello)')
        p2 = Pattern.backrefByName(name='word')
        self.assertEqual(str(p2), '(?P=word)')
        p3 = Pattern.backrefById(2)
        self.assertEqual(str(p3), r'\2')
        p4 = Pattern.condGroupMatch('word', 'a+b', 'c*d')
        self.assertEqual(str(p4), r'(?(word)a\+b|c\*d)')


    def test_charset(self):
        pat = CharSet.charset('_', alphanum=True)
        self.assertEqual(str(pat), '[0-9a-zA-Z_]')
        pat = CharSet.charset('-', digit=True, reverse=True)
        self.assertEqual(str(pat), r'[^0-9\-]')
        pat = CharSet.charset('-^_', lower=True)
        self.assertEqual(str(pat), r'[a-z\-\^_]')


    def test_repeat(self):
        p1 = Pattern('hello').group()
        self.assertEqual(str(p1), '(hello)')
        p2 = p1.repeat(exact=3)
        self.assertEqual(str(p2), '(hello){3}')
        p2 = p1.repeat(min=3, greedy=False)
        self.assertEqual(str(p2), '(hello){3-}?')
        p2 = p1.repeat(max=4)
        self.assertEqual(str(p2), '(hello){-4}')


    def test_common(self):
        # phone number of kind
        # (8776) 786-7823 # brackets, - are optional
        part1 = Pattern('(').group(name='opbrkt').optional() \
                    .then(Special.digit.repeat(exact=4)) \
                    .then(Pattern.condGroupMatch('opbrkt', ')',''))
        part2 = Special.digit.repeat(exact=3) \
                    .then(Pattern('-').optional()) \
                    .then(Special.digit.repeat(exact=4))
        combined = Pattern.lineStart().then(part1) \
                    .then(Pattern(' ').optional()) \
                    .then(part2).lineEnd()
        comb = combined.compile()
        testset = [ '(7653) 789-8706', '73657768899', '9891 2312828',
                   '(0999)222-4444' , '4567 222-3300' ]
        for test in testset:
            m = comb.search(test)
            if m:
                g = m.group(0)
                self.assertEqual(g, test)
        testset = [ '(7653 789-8706', '736578768899', '9891 231 2828',
                    '0999)222-4444' , '0 4567 222-3300',
                    '(7653) 789=8706', '736577688990', '9891 (2312)828',
                    '(0999)222-44440' , '4567  222-3300',
                    '(7653) 789 8706', '7365.776.8899', '0(9891) 231-2828' ]
        for test in testset:
            m = comb.search(test)
            self.assertEqual(None, m)




if __name__ == '__main__':
    unittest.main()



