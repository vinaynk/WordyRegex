#!/usr/bin/env python

import re
from WordyRegex import WordyRegexArgError, Pattern, CharSet

testData0 = '345 -345 +678 2.56 -1e3 +3.4563E8 -8.2 +3124 +3.1415 -0.4782377E-8'
testData1 = \
'''Hello World!
That is what we say, we programmers.
Whenever we learn something new,
and we do that quite often
0 1 2 3 4 5
Did you notice that zero?
We don't forget that zero,
that is the amount of life we have'''

emails = \
'''
hello8799@gmail.com
mail-me@hotmail.co.uk
Big_Bang@t-online.de
BOOM@abc.k-x.de
ding.dong@mmm-NN.CO.in
'''


def searchPrintResults(pat, text, flags=re.MULTILINE):
    cpat = pat.compile(flags)
    for gr in re.finditer(cpat, text):
        print(gr.span(), gr.group())


def egAnchor():
    '''
    Examples of use of anchor
    '''
    ## lineStart - anchroing pattern to the start of line
    print('lineStart - starting with lowercase')
    lineStartsWithLowerCase = CharSet.lineStart.then(
                                CharSet.charset(lower=True) \
                                    .then(CharSet.nonSpace.zeroOrMore())
                              )
    searchPrintResults(lineStartsWithLowerCase, testData1)

    ## lineEnd - anchroing pattern to the end of line
    print('lineEnd - maching , at the end of line')
    endingWithComma = Pattern(',').lineEnd()
    searchPrintResults(endingWithComma, testData1)

    ## strStart - anchroing pattern to the starting of a string
    print('strStart - first word of a string')
    firstWord = CharSet.strStart.then(CharSet.space.zeroOrMore()) \
                                .then(CharSet.nonSpace.oneOrMore()) \
                                .then(CharSet.wordBoundary)
    searchPrintResults(firstWord, testData1)

    ## stdEnd - anchroing pattern to the end of a string
    print('strEnd - last word of a string')
    lastWord = CharSet.wordBoundary.then(CharSet.nonSpace.oneOrMore()) \
                                   .then(CharSet.strEnd)
    searchPrintResults(lastWord, testData1)


def emailCheck():
    # gmail, t-online, yahoo etc
    domainMain = CharSet.charset('_-', alphanum=True).oneOrMore()
    # .com, .co.in, .co.uk, .de etc
    domainRpt  = Pattern('.').then(CharSet.charset(alphanum=True) \
                             .repeat(min=2,max=4)) \
                             .group() \
                             .oneOrMore()
    # gmail.com, t-online.de, hotmail.co.uk etc
    domain     = domainMain.then(domainRpt)
    # this is the part before @
    username   = CharSet.charset('-_.', alphanum=True).oneOrMore()
    # full email
    fullemail  = username.then('@').then(domain)
    searchPrintResults(fullemail, emails)


def wordlike(pattern):
    '''
    restricts match to patterns sandwitched between spaces
    adds condition to match line start/end to take care of either ends
    '''
    # either line start or a space (which will not be consumed)
    start = Pattern.anyOf(CharSet.lineStart, Pattern.preceededBy(CharSet.space))
    # either line end or a space (which will not be consumed)
    end   = Pattern.anyOf(CharSet.lineEnd, Pattern().succeededBy(CharSet.space))
    return start.then(pattern).then(end)


def egNumbers():
    sign     = CharSet.charset('+-').optional()
    number   = CharSet.digit.oneOrMore()
    decimal  = Pattern('.').then(number)
    # ----------------------------------------------------------------------
    # int, with optional +/- (eg: 234 +78465 -7386)
    # ----------------------------------------------------------------------
    intWithSignPat = sign.then(number)
    # this will match -1 and 3 in -1e3
    print('Without word like match')
    for gr in re.finditer(intWithSignPat.compile(), testData0):
        print('  ', gr)
    # makes sure that the match a word
    intWithSignPat = wordlike(intWithSignPat)
    print('With word like match')
    for gr in re.finditer(intWithSignPat.compile(), testData0):
        print('  ', gr)
    # ----------------------------------------------------------------------
    # basic floats with optional +/-
    # ----------------------------------------------------------------------




def main():
    # egAnchor()
    emailCheck()



if __name__ == '__main__':
    main()


