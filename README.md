![jiphy](https://raw.github.com/timothycrosley/jiphy/master/logo.png)

=====
[![PyPI version](https://badge.fury.io/py/jiphy.png)](http://badge.fury.io/py/jiphy)
[![Build Status](https://travis-ci.org/timothycrosley/jiphy.png?branch=master)](https://travis-ci.org/timothycrosley/jiphy)
[![Coverage Status](https://coveralls.io/repos/timothycrosley/jiphy/badge.svg?branch=develop&service=github)](https://coveralls.io/github/timothycrosley/jiphy?branch=develop)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/jiphy/)
[![Join the chat at https://gitter.im/timothycrosley/jiphy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/timothycrosley/jiphy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Write your client side code in a Jiphy! Jiphy is a two-way Python->JavaScript converter. It's not meant to create
executable Python code from complex JavaScript files, or runnable JavaScript from complex Python projects. Instead,
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

```python
import underscore as _

def my_function(argument1, argument2):
    if argument1:
        del argument2
    elif argument2:
        print(argument2)

    if somevar is someothervar And x is not b: pass
```


Get:

```javascript
var _ = require('_');

function my_function(argument1, argument2) {
    if (argument1) {
        delete argument2;
    } else if (argument2) {
        console.log(argument2);
    }
    if (somevar === someothervar && x !== b) {}
}
```

in a jiphy.


Why jiphy?
======================

jiphy (pronounced: jiffy) simply stands for JavaScript In, Python Out.

Jiphy is very different from other attempts at Python -> JavaScript conversion for the following reasons:
 -  Converts in both directions (JavaScript -> Python, Python -> JavaScript).
 -  Allows intermixing of code. You can add a Python function to a JavaScript file and then convert it all to JavaScript.
 -  Converts lines 1:1, so you always know which source line causes which output line. No source mapping needed.
 -  Doesn't require any extra JavaScript files to be loaded.
 -  Can be used by a single developer without team buy-in.

Jiphy only supports syntax, but with ES6 around the corner should one day support Classes, default arguments, etc.


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
|:----------------------------|:------------------|:-----------------------:|:-------------------:|
| def (...):                  | function(...) {}  |  ✓                      |  ✓                  |
| if ...:                     | if (...) {}       |  ✓                      |  ✓                  |
| while ...:                  | while (...) {}    |  ✓                      |  ✓                  |
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
| try:                        | try {             |  ✓                      |  ✓                  |
| except                      | catch             |  ✓                      |  ✓                  |
| except Exception as e       | catch(e)          |  ✓                      |  ✓                  |
| .append(...)                | .push(...)        |  ✓                      |  ✓                  |
| raise 'error'               | throw 'error';    |  ✓                      |  ✓                  |
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

--------------------------------------------

Thanks and I hope you find jiphy useful!

~Timothy Crosley
