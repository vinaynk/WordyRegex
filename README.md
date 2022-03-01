# WordyRegex

We often hate regex for being too terse. WordyRegex aims to change that. With WordyRegex, we can now hate regex for being too wordy.

The key idea is to provide functions to do most (if not all) of the regex related functions.

#### Note
I wrote this library as a training tool for regex. This library is not something one should add to any production system, even when they are drunk or high.

## Examples

Here is an example check for email-ids (well, for most email-ids anyway):

```python
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
print(str(fullemail))
```

## Classes
This module exposes the following classes.

1. `Pattern` - The main class that deals with creating and chaining different patterns
2. `CharSet` - A support class to create character set used in regex

Checkout the `example/` directory to see how these classes are used.

### class Pattern

`Pattern(pattern, escape)`: This is the constructor. `pattern`(str) specifies the non-regex pattern to be used.

For the ease of use, some functions are provided as static functions of the `Pattern` class. These will be called directly as a class member (not on object). Other functions are normal functions and have to be called with the objects. Following code shows the difference.

```python
ob = Pattern.lineStart() # static function lineStart
ob.then('abc').lineEnd() # normal functions `then` and `lineEnd` called with objects
```

`Pattern` objects are immutable. All operations create a new object.

`str(ob)` returns the underlying regex pattern inside a `Pattern` object.

Here is the list of all functions in this class. Note that `pat` stands for a pattern that can be a string or a `Pattern` object. A `:` is used to indicate that the function is a static function. `:func()` should be called as `Pattern.func()`

Additional reference notes in `[]`.

- `then(pat)` : appends `pat` to the current pattern and returns the new one
- `:lineStart()`: returns a `Pattern` object that matches the line start (`^`)
- `lineEnd()` : attaches a line end (`$`) to the current object and returns the new one
- `:anyChar()` : return a `Pattern` object that matches any (single) char (`.`)
- `group()` : group the pattern together using `()`. can specify an optional argument `name` if needed
- `zeroOrMore()` : repeats the pattern zero or more times (`*`)[1]
- `oneOrMore()` : repeats the pattern one or more times (`+`)[1]
- `zeroOrOne()` : repeats the pattern zero or one times (`?`)[1]
- `optional()` : similar to `zeroOrOne`
- `repeat(exact,min,max)`: repeats the pattern `exact` times if it is given. else repeats based on `min` and `max` (`{min,max}`)[1]
- `:seq(pat1, pat2, ...)` : concatenates multiple patterns in sequence
- `:anyOf(pat1, pat2, ...)` : creates a new pattern that matches any of pat1, pat2, ...
- `:preceededBy(pat)` : look-back match pattern `pat`. Does not consume `pat`
- `:preceededByNot(pat)` : reverse of the above
- `succeededBy(pat)` : look-ahead match pattern `pat`. Does not consume `pat`
- `succeededByNot(pat)` : reverse of the above
- `backrefByName(name)` : back-reference by name
- `backrefById(id)` : back-reference by id (discouraged)
- `condGroupMatch(name, pat1, pat2)` : conditionally match `pat1` or `pat2` based on whether a group with name `name` is found
- `getPattern()` : returns the underlying pattern. `str(pat)` also works
- `compile()` : compiles the regex from the `Pattern` object

Notes:

1. These functions accept a keyword `greedy` which can be used to control the greedy behaviour. Must be used after group() to work as expected.


### class CharSet

This class creates a CharSet (`[]`). Following is the constructor:

`CharSet(pat='', digit=False, lower=False, upper=False, reverse=False, alphanum=False)`

- `pat` : string of characters that need to be added to the charset
- `digit` : if True, adds `0-9` to charset
- `lower` : if True, adds `a-z` to charset
- `upper` : if True, adds `A-Z` to charset
- `alphanum` : if True, adds `0-9a-zA-Z` to charset
- `reverse` : if True, charset is reversed by adding `^` at the start

Additionally, this class also provides builtin special patterns. These are two types. First type maches empty string (but has 'special' meaning) and the second type matches 1 char.

Following matches start, end, or boundaries. Matches only empty string.

- `lineStart` (`^`) start of line
- `lineEnd` (`$`) end of line
- `strStart` (`\A`) start of string
- `strEnd` (`\Z`) end of string
- `wordBoundary` (`\b`) a word boundary
- `nonWordBoundary` (`\B`) not a word boundary

Following matches a single char.

- `anyChar` (`.`) matches any char
- `digit` (`\d`) for digit
- `nonDigit` (`\D`) reverse of the above
- `space` (`\s`) for space (inc. tabs, newline etc)
- `nonSpace` (`\S`) reverse of the above
- `wordChar` (`\w`) part of word
- `nonWordChar` (`\W`) reverse of the above

