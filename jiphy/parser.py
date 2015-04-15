"""jiphy/parser.py

Contains the basic Jiphy code parser.

Copyright (C) 2015  Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""

class Parser(object):

    def __init__(self, code):
        self.index = 0
        self.code = code
        self.output = []

    def text_till(self, strings):
        """
            Returns all text till it encounters the given string (or one of the given strings)
        """
        if isinstance(strings, (str, unicode)):
            strings = [strings]

        text = ""
        matchedString = ""

        while self.more:
            for string in strings:
                if self.characters(len(string)) == string:
                    matchedString = string
                    break

            if matchedString:
                break

            text += self.pop()

        self += 1
        return (text, matchedString)

    def pop(self):
        """
            removes the current character then moves to the next one, returning the current character
        """
        char = self.code[self.index]
        self.index += 1
        return char

    def characters(self, numberOfCharacters):
        """
            Returns characters at index + number of characters
        """
        return self.code[self.index:self.index + numberOfCharacters]

    def __iadd__(self, other):
        self.index += other
        return self

    def __isub__(self, other):
        self.index -= other
        return self

    @property
    def more(self):
        """
            Returns true if there is more html to parse
        """
        return self.index < len(self)

    def __len__(self):
        return len(self.code)

    def behind(self, start, difference):
        return self.code[start - difference: start]

    def ahead(self, start, difference):
        return self.code[start: start + difference]

    def __str__(self):
        return "".join(self.output)
