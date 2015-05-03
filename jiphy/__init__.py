"""jiphy/__init__.py.

Write your client side code in a Jiphy! Jiphy is a two-way Python->Javascript converter. It's not meant to create
runnable Python code from comlex JavaScript files, or runnable JavaScript from comples Python projects. Instead,
Jiphy enables Python programmers to more easily write JavaScript code by allowing them to use more familiar syntax,
and JavaScript developers to more easily write Python code.

Jiphy's Design Objectives:

- Reduce the context switching necessary for a Python developer to write JavaScript code and vice versa.
- Always output 1:1 line mappings (a line of Python produces a line of JavaScript) so source maps are not necessary.
- Be usable for a single developer on a project (Shouldn't require all developers to switch to using Jiphy).
- Should be easy to write text-editor plugins that expose Jiphy within IDEs for on-the-spot conversion.

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
from __future__ import absolute_import, division, print_function, unicode_literals

from . import to

__version__ = "1.1.0"
