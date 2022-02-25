#!/usr/bin/env python

import re
from WordyRegex import WordyRegexArgError, Pattern, Special, CharSet


def wordlike(pattern):
    '''
    this allows to match a pattern sandwitched between spaces
    adds condition to match line start/end to take care of either ends
    '''
    # either line start or a space (which will not be consumed)
    start = Pattern.anyOf(Special.lineStart, Pattern.preceededBy(Special.space))
    # either line end or a space (which will not be consumed)
    end   = Pattern.anyOf(Special.lineEnd, Pattern().succeededBy(Special.space))
    return start.then(pattern).then(end)


def egNumbers():
    data    = '345 -345 +678 2.56 -1e3 +3.4563E8 -8.2 +3124 +3.1415 -0.4782377E-8'
    sign    = CharSet.charset('+-').optional()
    number  = Special.digit.oneOrMore()
    decimal = Pattern('.').then(number)
    # ----------------------------------------------------------------------
    # int, with optional +/- (eg: 234 +78465 -7386)
    # ----------------------------------------------------------------------
    intWithSignPat = sign.then(number)
    # this will match -1 and 3 in -1e3
    print('Without word like match')
    for gr in re.finditer(intWithSignPat.compile(), data):
        print('  ', gr)
    # makes sure that the match a word
    intWithSignPat = wordlike(intWithSignPat)
    print('With word like match')
    for gr in re.finditer(intWithSignPat.compile(), data):
        print('  ', gr)
    # ----------------------------------------------------------------------
    # basic floats with optional +/-
    # ----------------------------------------------------------------------




def main():
    egNumbers()



if __name__ == '__main__':
    main()


