#! /usr/bin/env python
"""jiphy/main.py

Defines the terminal interface for Jiphy

Copyright (C) 2015 Timothy Edmund Crosley

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

import argparse
import os
import sys
from argparse import RawTextHelpFormatter
from datetime import datetime
from difflib import unified_diff

import jiphy

from .pie_slice import *


INTRO = """
 /##########################################################\\
 ............................................................
 ...................................................... .....
 ...7$$$$.............$$$$$........MM.M:.MMMM. M,..M:MM .MM..
 .I$I~~=~$$.7M$$$M$7$$?====$$......MM.M:.M...M.M,..M: M .M ..
 I$~~~~~~~$NZ$$$$$$8$=~~~~~~~$.....MM.M:.MMMMM.MMMMM:..MM ...
 $=~~~~~~=$$$M$$$NZ$$7~=~~~~~=$.MM.MM.M:.M.....M,..M:..MM....
 7~~~~~~~$$$/_$$$_\$$$~~~~~~==$. MMO .M:.M ....M,..M:..MM....
 $~~~~~~~$$$$$Z$$Z7$$$=~~~~~~~$..............................
 $=~~~~~~$$$$$$$$$$$$$=~~~~~~$.. ....... ....................
  $$~~~~~$$|$$$$$$$$|$~~~~=$.7777777...... ..................
 ...$$$$$$$M\$$$$$$/M$$$$$7,$77777777:..YOUR CLIENTSIDE DONE.
 . .......$$D\$$$$/M$~. ..=777777777?.... .. ........ .......
 ...........,7$$$$$7777777777777..................... .......
 ..............777777777777777......... ............... .....
 ...............77777777777................VERSION 1.0.......
 ........ ...................................................
 ............................................................
 \##########################################################/

 Copyright (C) 2015 Timothy Edmund Crosley
 Under the MIT License

"""


def iter_source_code(paths, in_ext="py"):
    """Iterate over all Python source files defined in paths."""
    for path in paths:
        if os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.' + in_ext):
                        yield os.path.join(dirpath, filename)
        else:
            yield path


def main():
    parser = argparse.ArgumentParser(description=INTRO, formatter_class=RawTextHelpFormatter)
    parser.add_argument('files', nargs='+', help='One or more source files that you would like converted.')
    parser.add_argument('-o', '--out-lang', help='Specify the desired output language. Defaults to JavaScript.',
                        dest='out_lang', type=str, choices=("py", "js"), default="js")
    parser.add_argument('-e', '--out-ext', help='Specify the desired output files extension (such as py or js). '
                        'Default is baesd on lang', dest='out_ext', type=str,)
    parser.add_argument('-i' '--in-ext', help='Specify the extension of the files to parse. Defualt is .jiphy',
                        default="jiphy", dest="in_ext")
    parser.add_argument('-rc', '--recursive', dest='recursive', action='store_true',
                        help='Recursively look for files to convert')
    parser.add_argument('-od', '--out-dir', dest='out_dir', default="",
                        help="Specify in which directory files should be outputed")
    parser.add_argument('-d', '--diff', dest='diff', default=False, action='store_true',
                        help="Produce a diff that would result in running jiphy, "
                             "without actually performing any changes")
    
    arguments = dict((key, value) for (key, value) in itemsview(vars(parser.parse_args())))
    arguments['out_ext'] = arguments['out_ext'] or arguments['out_lang']

    file_names = arguments.pop('files', [])
    if file_names == ['-']:
        input_code = sys.stdin.read()
        if arguments['out_lang'] == "py":
            sys.stdout.write(jiphy.to.python(input_code))
        else:
            sys.stdout.write(jiphy.to.javascript(input_code))
    else:
        if not arguments['diff']:
            print(INTRO)
        wrong_sorted_files = False
        if arguments.get('recursive', False):
            file_names = iter_source_code(file_names, arguments['in_ext'])
        for file_name in file_names:
            with open(file_name) as input_file:
                input_code = input_file.read()
                if arguments['out_lang'] == 'py':
                    output_code = jiphy.to.python(input_code)
                else:
                    output_code = jiphy.to.javascript(input_code)

                stripped_code = []
                for line in output_code.split("\n"):
                    stripped_code.append(line.rstrip())
                output_code = '\n'.join(stripped_code)

                file_name_parts = file_name.split('.')
                output_file_name = "{0}{1}.{2}".format(arguments['out_dir'],
                                                       ".".join(file_name_parts[:-1]), arguments['out_ext'])
                if arguments['diff']:
                    for line in unified_diff(input_code.splitlines(1),
                                             output_code.splitlines(1),
                                             fromfile=file_name + ':before',
                                             tofile=output_file_name + ':after',
                                             fromfiledate=datetime.fromtimestamp(os.path.getmtime(file_name)),
                                             tofiledate=datetime.now()):
                        sys.stdout.write(line)
                else:
                    print("   |-> [{2}]: Converting '{0}' -> '{1}' in a Jiphy!".format(file_name, output_file_name,
                                                                                       arguments['out_lang'].upper()))
                    with open(output_file_name, 'w') as output_file:
                        output_file.write(output_code)

        if not arguments['diff']:
            print("   |")
            print("   |                 >>> Done! :) <<<")
            print("")


if __name__ == "__main__":
    main()
