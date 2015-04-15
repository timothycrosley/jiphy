"""test_jiphy.py.

Tests all major functionality of the jiphy library
Should be ran using py.test by simply running by.test in the jiphy project directory

Copyright (C) 2013  Timothy Edmund Crosley

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

import jiphy


def two_way_conversion_test(python_code, javascript_code):
    """Tests that the given Python_code will turn into the specified JavaScript and visa versa in a Jiphy.
       Additionaly, ensures that if the python code is passed into the python converter it stays as Python
       and if the given JavaScript code is passed into the javascript converter they get return unmodified
    """
    assert jiphy.to.javascript(python_code) == javascript_code
    assert jiphy.to.python(javascript_code) == python_code

    assert jiphy.to.javascript(javascript_code) == javascript_code
    assert jiphy.to.python(python_code) == python_code


def test_import_conversion():
    """Tests to ensure that converting Python imports to JavaScript imports and vice versa works in a Jiphy."""
    two_way_conversion_test(("import something\n"
                             "import underscore as _\n"),
                            ("var something = require('something.js');\n"
                             "var _ = require('underscore.js');\n"))


def test_noop_function_conversion():
    """Tests to ensure that converting Javascript require statements to Python imports works in a Jiphy."""
    two_way_conversion_test(("def my_function(): pass\n"),
                            ("function my_function() {}\n"))


def test_simple_indented_function_conversion():
    """Tests to ensure that converting Javascript require statements to Python imports works in a Jiphy."""
    two_way_conversion_test(("def my_function(test):\n"
                             "    some_other_function(test)\n"
                             "\n"),
                            ("function my_function(test) {\n"
                             "    some_other_function(test);\n"
                             "}\n"))


def test_print_statement():
    """Tests to ensure print statements have a simple convesion applied to them"""
    two_way_conversion_test(("print('something')\n"),
                            ("console.log('something');\n"))


def boolean_test():
   """Tests to ensure boolean statements have a simple convesion applied to them in a jiphy"""
   two_way_conversion_test("a = (True and False) or (None and Unset)\n",
                           "a = (true && false) or (null and undefined);\n")


def test_condition():
    """Test to ensure basic conditionals get converted in a jiphy"""
    two_way_conversion_test(("if something is true:\n"
                             "    do_something()\n"
                             "\n"),
                            ("if (something === true) {\n"
                             "    do_something();\n"
                             "}\n"))


def test_is():
    """Test to ensure === gets changed to is in a jiphy"""
    two_way_conversion_test("True is True\n",
                            "true === true;\n")


def test_not():
    """Test to nesure not statements are correct handled in a jiphy"""
    two_way_conversion_test(("True is not True\n"
                             "true = not True\n"),
                            ("true !== true;\n"
                             "true = !true;\n"))

def test_for_loop():
    """Test to ensure that for loops will convert correctly"""
    two_way_conversion_test(("for x = 0; x < 10; x++:\n"
                             "    y = x;\n"
                             "\n"),
                            ("for (var x = 0; x = 10; x++) {\n"
                             "    var y = x;\n"
                             "}\n"))


def test_variables():
    """Test to ensure that vars will be correctly handled"""
    two_way_conversion_test("x = 10\n", "var x = 10;\n")


def test_delete():
    """Test to ensure deletion works as expected"""
    two_way_conversion_test("del x\n", "delete x;\n")


def test_elif():
    """Test to ensure elif works as expected"""
    two_way_conversion_test(("if x == y:\n"
                             "    print('one')\n"
                             "elif true:\n"
                             "    print('two')\n"
                             "\n"),
                            ("if (x == y) {\n"
                             "    console.log('one');\n"
                             "} else if (true) {\n"
                             "    console.log('two');\n"
                             "}\n"))


def test_pass():
    """Test to ensure pass is correctly converted"""
    two_way_conversion_test(("if x:\n"
                             "    pass\n"
                             "\n"),
                            ("if (x) {\n"
                             "\n"
                             "}\n"))


def test_comments():
    """Test to ensure comments will work as expected"""
    two_way_conversion_test(('"""Test comment\n'
                             '    line two\n'
                             '"""\n'),
                            ('/* Test comment\n'
                             '    line two\n'
                             '*/\n'))
    two_way_conversion_test("# comment\n",
                            "// comment\n")


def test_multi_line_string():
    """Test to ensure multi line strings work as expected"""
    two_way_conversion_test(("print('''line one\n"
                             "         line two''')\n"),
                            ("console.log('line one\\n' +\n"
                             "            'line two')\n"))

