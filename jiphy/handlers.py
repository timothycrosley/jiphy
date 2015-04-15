from .router import Router

routes = Router()


class Handler(object):
    """A Handler encapsulates both the node / position information in the produced AST alongside the code used
       to generate the nodes contained within it"""
    start_on = ()
    end_on = ()
    accept_children = routes
    back_track = 0

    def __init__(self, parser, started_on='', started_at=0, parent=None):
        self.parser = parser
        self.parent = parent
        self.children = []
        self.started_on = started_on
        self.started_at = started_at
        self.ended_on = ''
        self.ended_at = 0
        if isinstance(self.end_on, (str, unicode)):
            self.end_on = (self.end_on, )

        self.start()

    def start(self):
        if not self.end_on:
            return

        while self.parser.more:
            (text, matched) = self.parser.text_till(self.end_on + self.accept_children.match_on)
            self.children.append(PassThrough(text))
            if matched in self.end_on:
                self.parser += len(matched) - 1
                self.ended_on = matched
                break

            if not matched:
                break

            handler = self.accept_children.get(matched, None)
            if handler:
                self.parser += len(matched) - 1
                self.children.append(handler(self.parser, matched, self.parser.index - 1, parent=self))
                handler.ended_at = self.parser.index
            else:
                raise NotImplementedError('There is no support to handle ' + parser)

        self.parser -= self.back_track
        self.ended_at = self.parser.index

    @property
    def javascript_content(self):
        return "".join((child.javascript for child in self.children))


    def _javascript(self):
        return (self.started_on or '') + self.javascript_content + (self.ended_on or '')

    @property
    def javascript(self):
        return self._javascript()

    @property
    def python_content(self):
        return "".join((child.python for child in self.children))

    def _python(self):
        return (self.started_on or '') + self.python_content + (self.ended_on or '')

    @property
    def python(self):
        return self._python()

    def behind(self, amount=1):
        return self.parser.behind(self.started_at, amount)

    def ahead(self, amount=1):
        return self.parser.ahead(self.started_at, amount)


class RootHandler(Handler):

    def start(self):
        while self.parser.more:
            (text, matched) = self.parser.text_till(self.accept_children.match_on)
            self.children.append(PassThrough(text))
            if matched in self.end_on:
                self.ended_on = self.end_on
                break

            if not matched:
                break

            handler = self.accept_children.get(matched, None)
            if handler:
                self.parser += len(matched) - 1
                self.children.append(handler(self.parser, matched, self.parser.index - 1, parent=self))
            else:
                raise NotImplementedError('There is no support to handle ' + parser)

        self.parser -= self.back_track
        self.ended_at = self.parser.index

class PassThrough(object):
    __slots__ = ('code', )

    def __init__(self, code):
        self.code = code

    @property
    def javascript(self):
        return self.code

    @property
    def python(self):
        return self.code


routes.add('\\')
class Escape(Handler):

    def start(self):
        self.children.append(PassThrough(self.parser.pop()))


class MultiLineComment(Handler):
    accept_children = Router((Escape, '/'))

    def _javascript(self):
        return '/* {0} */'.format(self.javascript_content)

    def _python(self):
        return '"""{0}"""'.format(self.python_content)


@routes.add('"""')
class PythonComment(MultiLineComment):
    end_on = '"""'


@routes.add('/* ')
class JavaScriptComment(MultiLineComment):
    end_on = ' */'


@routes.add("'''")
class String(Handler):
    accept_children = Router((Escape, '\\'))
    end_on = "'''"

    def _javascript(self):
        content = self.javascript_content.split("\n")
        if len(content) <= 1:
            return Handler._javascript(self)

        output = []
        for line in content[:-1]:
             output.append("'{0}\n' + ".format(line))

        output.append(content[-1])
        return "\n".join(output)


@routes.add('# ', '// ')
class SingleLineComment(Handler):
    accept_children = Router()
    end_on = "\n"

    def _javascript(self):
        return '// {0}\n'.format(self.javascript_content)

    def _python(self):
        return '# {0}\n'.format(self.python_content)


@routes.add("import ")
class PythonImport(Handler):
    end_on = ("\n", " #", " //")

    @property
    def back_track(self):
        if self.ended_on == " #":
            return 1
        return 0

    def _javascript(self):
        content = self.python_content.split(" ")
        to_import = content[0]
        if "as" in content:
            variable_name = content[content.index('as') + 1]
        else:
            variable_name = to_import

        if self.ended_on == " #":
            self.ended_on = " "

        return "var {0} = require('{1}.js');{2}".format(variable_name, to_import, self.ended_on)


@routes.add("): pass\n", ") {}\n")
class Pass(Handler):

    def _python(self):
        return "): pass\n"

    def _javascript(self):
        return ") {}\n"


@routes.add("True", "true")
class TrueStatement(Handler):

    def _python(self):
        return "True"

    def _javascript(self):
        return "true"


@routes.add("False", "false")
class FalseStatement(Handler):

    def _python(self):
        return "False"

    def _javascript(self):
        return "false"


@routes.add('None', 'null')
class NoneStatement(Handler):

    def _python(self):
        return "None"

    def _javascript(self):
        return "null"


@routes.add('print', 'console.log')
class PrintFunction(Handler):

    def _python(self):
        return "print"

    def _javascript(self):
        return "console.log"


@routes.add('var ')
class JavascriptSetter(Handler):
    accept_children = Router()
    end_on = (";")

    def _python(self):
        return "{0};".format(self.python_content)


@routes.add('function ', 'def ')
class Function(Handler):

    def _python(self):
        return "def "

    def _javascript(self):
        return "function "


@routes.add('del ', 'delete ')
class DeleteStatement(Handler):

    def _javascript(self):
        return "delete "

    def _python(self):
        return "del "


@routes.add('if (')
class JavascriptIfStatement(Handler):
    end_on = ') {\n'
    back_track = 4

    def _python(self):
        return "if {0}".format(self.python_content)


@routes.add('if ')
class PythonIfStatement(Handler):
    end_on = ':\n'
    back_track = 2

    def _javascript(self):
        return "if ({0}".format(self.javascript_content)


@routes.add('for (', 'for ')
class ForStatement(Handler):

    def _python(self):
        return 'for '

    def _javascript(self):
        return 'for ('


@routes.add('elif ', 'else if ')
class ElifStatement(Handler):

    def _python(self):
        return 'elif '

    def _javascript(self):
        return 'else if '



@routes.add('):\n', ':\n')
class PythonBlock(Handler):
    end_on = '\n\n'

    def _javascript(self):
        content = ") {\n" + self.javascript_content
        if self.javascript_content and not self.javascript_content.strip().endswith(";"):
            content += ";"
        return content + "\n}\n"


@routes.add(') {\n')
class javascriptBlock(Handler):
    end_on = "\n}\n"

    def _python(self):
        return ":\n{0}\n\n".format(self.python_content)


@routes.add('{')
class Dictionary(Handler):
    end_on = '}'


@routes.add(' is not ', ' !== ')
class IsNotStatement(Handler):

    def _python(self):
        return ' is not '

    def _javascript(self):
        return ' !== '


@routes.add(' is ', ' === ')
class IsStatement(Handler):

    def _python(self):
        return ' is '

    def _javascript(self):
        return ' === '


@routes.add(' not ', ' !')
class NotStatement(Handler):

    def _python(self):
        return ' not '

    def _javascript(self):
        return ' !'


@routes.add('Unset', 'undefined')
class Unset(Handler):

    def _python(self):
        return 'Unset'

    def _javascript(self):
        return 'undefined'


@routes.add('And ', '&& ')
class EndOfStatement(Handler):

    def _python(self):
        return 'And '

    def _javascript(self):
        return '&& '


@routes.add('Or ', '|| ')
class EndOfStatement(Handler):

    def _python(self):
        return 'Or '

    def _javascript(self):
        return '|| '


@routes.add('pass\n')
class PythonNoop(Handler):

    def _javascript(self):
        return '\n'


@routes.add(';\n', '\n')
class EndOfStatement(Handler):

    def _python(self):
        return '\n'

    def _javascript(self):
        if self.behind() in ('\n', ' ', '\t'):
            return '\n'

        return ';\n'
