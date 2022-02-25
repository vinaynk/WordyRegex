

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



if __name__ == '__main__':
    unittest.main()



