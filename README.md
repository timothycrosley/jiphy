![jiphy](https://raw.github.com/timothycrosley/jiphy/master/logo.png)
=====

[![PyPI version](https://badge.fury.io/py/jiphy.png)](http://badge.fury.io/py/jiphy)
[![PyPi downloads](https://pypip.in/d/jiphy/badge.png)](https://crate.io/packages/jiphy/)
[![Build Status](https://travis-ci.org/timothycrosley/jiphy.png?branch=master)](https://travis-ci.org/timothycrosley/jiphy)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/jiphy/)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/timothycrosley/jiphy/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Write your client side code in a Jiphy! Jiphy is a two-way Python->JavaScript converter. It's not meant to create
runnable Python code from complex JavaScript files, or runnable JavaScript from complex Python projects. Instead,
Jiphy enables Python programmers to more easily write JavaScript code by allowing them to use more familiar syntax,
and even JavaScript developers to more easily write Python code.

As a Python developer you can convert existing code in someone else's project from JavasScript into Python, edit it,
and then convert it back before submitting.

Jiphy's Design Objectives:

- Reduce the context switching necessary for a Python developer to write JavaScript code and vice versa.
- Always output 1:1 line mappings (a line of Python produces a line of JavaScript) so source maps are not necessary.
- Be usable for a single developer on a project (No mass buy-in needed).
- Should be easy to write text-editor plugins that expose Jiphy within IDEs for on-the-spot conversion.
- Quickly run over many files.
- Change syntax only

Write:

    import underscore as _

    def my_function(argument1, argument2):
        if argument1:
            del argument2
        elif argument2:
            print(argument2)

        if somevar is someothervar And x is not b: pass


Get:

    var _ = require('_');

    function my_function(argument1, argument2) {
        if (argument1) {
            delete argument2;
        } else if (argument2) {
            console.log(argument2);
        }
        if (somevar === someothervar && x !== b) {}
    }

in a jiphy.


Important things to know when writing Python for conversion to JavaScript
===================

- Every indented block must have a line after it.

For instance:

    if something is True:
        do_something()

    print("done")

Is valid as the if statement has a new line after it. However:

    if something is True:
        do_something()
    print("done")

is NOT valid in Jiphy. The lack of a new line makes it impossible to do a 1:1 conversion and still be nicely formatted JS code.

- Jiphy isn't smart enough to know when to create a var

For now, you still have to write var in front of new variables in Jiphy. Jiphy simply does not yet have the smarts to know when it is and when it is not required.

- Jiphy does not implement stdlib components, classes, etc. It's SYNTAX ONLY.


Syntax / Contstructs Jiphy Suppports
===================
| Python                      | JavaScript        | Supported To JavaScript | Supported To Python |
| -------------               |:-----------------:|:-----------------------:|:-------------------:|
| def (...):                  | function(...) {}  |  ✓                      |  ✓                  |
| if ...:                     | if (...) {}       |  ✓                      |  ✓                  |
| elif ...:                   | } else if (...) { |  ✓                      |  ✓                  |
| else:                       | } else {          |  ✓                      |  ✓                  |
| pass                        | {}                |  ✓                      |  ✓                  |
| print(...)                  | console.log(...)  |  ✓                      |  ✓                  |
| True                        | true              |  ✓                      |  ✓                  |
| False                       | false             |  ✓                      |  ✓                  |
| None                        | null              |  ✓                      |  ✓                  |
| Or                          | &#124;&#124;                | ✓                        |  ✓                  |
| And                         | &&                |  ✓                      |  ✓                  |
| Unset                       | undefined         |  ✓                      |  ✓                  |
| not                         | !                 |  ✓                      |  ✓                  |
| is                          | ===               |  ✓                      |  ✓                  |
| del                         | delete            |  ✓                      |  ✓                  |
| \n                          | ;\n               |  ✓                      |  ✓                  |
| # comment                   | // comment        |  ✓                      |  ✓                  |
| str(...)                    | String(...)       |  ✓                      |  ✓                  |
| bool(...)                   | Boolean(...)      |  ✓                      |  ✓                  |
| int(...)                    | Number(...)       |  ✓                      |  ✓                  |
| import pdb; pdb.set_trace() | debugger;         |  ✓                      |  ✓                  |
| import x                    | var x = require(x)|  ✓                      |                     |
| import x as _               | var _ = require(x)|  ✓                      |                     |
| "String"                    | 'String'          |  ✓                      |                     |
| """String"""                | 'Str' + 'ing'     |  ✓                      |                     |
| @decorator                  | f = decorator(f)  |  ✓                      |                     |

Installing jiphy
===================

Installing jiphy is as simple as:

    pip install jiphy

or if you prefer

    easy_install jiphy

Using jiphy
===================
**from the command line**:

    jiphy mypythonfile.py mypythonfile2.py

 or to conform all code to the specified file format

    jiphy mypythonfile.js mypythonfile2.js --conform

or recursively:

    jiphy -rc .

 *which is equivalent to*

    jiphy **/*.py

or recursively conform:

    jiphy -rc --conform .

or to see the proposed changes without applying them

    jiphy mypythonfile.py --diff

**from within Python**:

    import jiphy

    jiphy.to.javascript(python_code)
    jiphy.to.python(javascript_code)



Why jiphy?
======================

jiphy (pronounced: jiffy) simply stands for JavaScript In, Python Out.

--------------------------------------------

Thanks and I hope you find jiphy useful!

~Timothy Crosley
