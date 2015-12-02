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


def two_way_conversion_test(python_code, javascript_code, expect_python=None, expect_javascript=None):
    """Tests that the given Python_code will turn into the specified JavaScript and visa versa in a Jiphy.
       Additionaly, ensures that if the python code is passed into the python converter it stays as Python
       and if the given JavaScript code is passed into the javascript converter they get return unmodified
    """
    expect_javascript = expect_javascript or javascript_code
    expect_python = expect_python or python_code

    assert jiphy.to.javascript(python_code) == expect_javascript
    print(repr(jiphy.to.python(javascript_code)))
    assert jiphy.to.python(javascript_code) == expect_python

    assert jiphy.to.javascript(javascript_code) == javascript_code
    assert jiphy.to.python(python_code) == python_code


def test_import_conversion():
    """Tests to ensure that converting Python imports to JavaScript imports and vice versa works in a Jiphy."""
    two_way_conversion_test("import something\n"
                            "import underscore as _\n",
                            "var something = require('something');\n"
                            "var _ = require('underscore');\n",
                            "var something = require('something')\n"
                            "var _ = require('underscore')\n")


def test_noop_function_conversion():
    """Tests to ensure that converting Javascript require statements to Python imports works in a Jiphy."""
    two_way_conversion_test(("def my_function(): pass\n"),
                            ("function my_function() {}\n"))


def test_simple_indented_function_conversion():
    """Tests to ensure that converting Javascript require statements to Python imports works in a Jiphy."""
    two_way_conversion_test("def my_function(test):\n"
                            "    some_other_function(test)\n"
                            "\n",
                            "function my_function(test) {\n"
                            "    some_other_function(test);\n"
                            "}\n")


def test_print_statement():
    """Tests to ensure print statements have a simple convesion applied to them"""
    two_way_conversion_test("print('something')\n",
                            "console.log('something');\n")


def boolean_test():
   """Tests to ensure boolean statements have a simple convesion applied to them in a jiphy"""
   two_way_conversion_test("a = (True and False) or (None and Unset)\n",
                           "a = (true && false) or (null and undefined);\n")


def test_condition():
    """Test to ensure basic while loop gets converted in a jiphy"""
    two_way_conversion_test("if something is True:\n"
                            "    do_something()\n"
                            "\n",
                            "if (something === true) {\n"
                            "    do_something();\n"
                            "}\n")


def test_while_loop():
    """Test to ensure basic conditionals get converted in a jiphy"""
    two_way_conversion_test("while something is True:\n"
                            "    do_something()\n"
                            "\n",
                            "while (something === true) {\n"
                            "    do_something();\n"
                            "}\n")


def test_is():
    """Test to ensure === gets changed to is in a jiphy"""
    two_way_conversion_test("True is True\n",
                            "true === true;\n")


def test_not():
    """Test to nesure not statements are correct handled in a jiphy"""
    two_way_conversion_test("True is not True\n"
                            "True = not True\n",
                            "true !== true;\n"
                            "true = !true;\n")

def test_for_loop():
    """Test to ensure that for loops will convert correctly"""
    two_way_conversion_test("for var x = 0; x < 10; x++:\n"
                            "    var y = x\n"
                            "\n",
                            "for (var x = 0; x < 10; x++) {\n"
                            "    var y = x;\n"
                            "}\n")


def test_variables():
    """Test to ensure that vars will be correctly handled"""
    two_way_conversion_test("var x = 10\n", "var x = 10;\n")


def test_delete():
    """Test to ensure deletion works as expected"""
    two_way_conversion_test("del x\n", "delete x;\n")


def test_elif():
    """Test to ensure elif works as expected"""
    two_way_conversion_test("if x == y:\n"
                            "    print('one')\n"
                            "elif True:\n"
                            "    print('two')\n"
                            "\n",
                            "if (x == y) {\n"
                            "    console.log('one');\n"
                            "} else if (true) {\n"
                            "    console.log('two');\n"
                            "}\n")


def test_pass():
    """Test to ensure pass is correctly converted"""
    two_way_conversion_test("if x:\n"
                            "    pass\n"
                            "\n"
                            "\n",
                            "if (x) {\n"
                            "    \n"
                            "\n"
                            "}\n")


def test_comments():
    """Test to ensure comments will work as expected"""
    two_way_conversion_test('"""Test comment\n'
                            '    line two\n'
                            '"""\n',
                            '/* Test comment\n'
                            '    line two\n'
                            ' */\n')
    two_way_conversion_test("# comment\n",
                            "// comment\n")
    two_way_conversion_test('""""\n'
                            '    Test Comment\n'
                            '"""\n',
                            '/**\n'
                            '    Test Comment\n'
                            ' */\n')


def test_multi_line_string():
    """Test to ensure multi line strings work as expected"""
    two_way_conversion_test("print('''line one\n"
                            "         line two''')\n",
                            "console.log('line one\\n' +\n"
                            "'         line two');\n",
                            "print('line one\\n' +\n"
                            "'         line two')\n")


def test_assigned_function():
    """Test to ensure assigning a function works as expected"""
    two_way_conversion_test("exports.schema = def(argument1, argument2):\n"
                            "  print(argument1)\n"
                            "\n",
                            "exports.schema = function(argument1, argument2) {\n"
                            "  console.log(argument1);\n"
                            "};\n")
    two_way_conversion_test("exports.schema = def(argument1, argument2):\n"
                            "  print(argument1)\n"
                            "\n",
                            "exports.schema = function(argument1, argument2) {\n"
                            "  console.log(argument1);\n"
                            "};\n")


def test_magic_function():
    """Test to ensure assigning a function works as expected"""
    two_way_conversion_test("=def schema(argument1, argument2):\n"
                            "  print(argument1)\n"
                            "\n",
                            "module.exports.schema = function(argument1, argument2) {\n"
                            "  console.log(argument1);\n"
                            "};\n",
                            "module.exports.schema = def(argument1, argument2):\n"
                            "  print(argument1)\n"
                            "\n")


def test_decorator():
    """Test to ensure decorators get converted in the expected way"""
    two_way_conversion_test("@decorate\n"
                            "def my_action(arguments):\n"
                            "   do_something()\n"
                            "\n",
                            "my_action = decorate(my_action);\n"
                            "function my_action(arguments) {\n"
                            "   do_something();\n"
                            "}\n",
                            "my_action = decorate(my_action)\n"
                            "def my_action(arguments):\n"
                            "   do_something()\n"
                            "\n",
                            )


def test_str():
    """Test to ensure strings get converted in the expected way"""
    two_way_conversion_test("x = str(1)\n",
                            "x = String(1);\n")


def test_int():
    """Test to ensure ints get converted in the expected way"""
    two_way_conversion_test("y = int('1')\n",
                            "y = Number('1');\n")


def test_bool():
    """Test to ensure booleans get converted in the expected way"""
    two_way_conversion_test("z = bool(1)\n",
                            "z = Boolean(1);\n")


def test_breakpoint():
    """Test to ensure breakpoints get converted in the expected way"""
    two_way_conversion_test("import pdb; pdb.set_trace()\n",
                            "debugger;\n")


def test_last_construct_single_line_comment():
    """Test to ensure correct behaviour when the last construct is a single line comment"""
    two_way_conversion_test("def my_utility(argument):\n"
                            "   do_something()\n"
                            "   # comment\n"
                            "\n",
                            "function my_utility(argument) {\n"
                            "   do_something();\n"
                            "   // comment\n"
                            "}\n")


def test_except_conversion():
    """Test to ensure excepts / catches get converted successfully"""
    two_way_conversion_test("try:\n"
                            "   do_something()\n"
                            "except Exception as e:\n"
                            "   do_something_else(e)\n"
                            "\n",
                            "try {\n"
                            "   do_something();\n"
                            "} catch (e) {\n"
                            "   do_something_else(e);\n"
                            "}\n")
    two_way_conversion_test("try:\n"
                            "   do_something()\n"
                            "except:\n"
                            "   do_something_else()\n"
                            "\n",
                            "try {\n"
                            "   do_something();\n"
                            "} catch () {\n"
                            "   do_something_else();\n"
                            "}\n")


def test_append_conversion():
    """Tests to ensure append/push get converted in desired mannor"""
    two_way_conversion_test("[].append('item')\n",
                            "[].push('item');\n")


def test_raise_conversion():
    """Tests to ensure append/push get converted in desired mannor"""
    two_way_conversion_test("raise 'error'\n",
                            "throw 'error';\n")


def test_for_loop_in_function_conversion():
    """Tests to ensure a for loop within a function gets converted as expected"""

    two_way_conversion_test('def clear():\n'
                            '    grid = []\n'
                            '    for i in range(0, config.SIZE):\n'
                            '        grid.append(0)\n\n\n\n\n',
                            'function clear() {\n'
                            '    grid = [];\n'
                            '    for (i in range(0, config.SIZE)) {\n'
                            '        grid.push(0);\n'
                            '    }\n'
                            '}\n\n\n',
                            'def clear():\n'
                            '    grid = []\n'
                            '    for i in range(0, config.SIZE):\n'
                            '        grid.append(0)\n'
                            '    \n\n\n\n')
