"""jiphy/routers.py

Defines how to store the routes that direct text-content to specific handlers that form the pseudo AST

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

from copy import deepcopy

from .pie_slice import *


class Router(object):
    """Routes specific text patterns to handlers that define how the content will be transformed
       creating a pseudo AST"""
    __slots__ = ('routes', )

    def __init__(self, *routes):
        self.routes = OrderedDict()
        for route in routes:
            self.add(*route[1:])(route[0])

    def add(self, *match):
        def decorator(handler):
            if isinstance(handler.start_on, str):
                handler.start_on = (handler.start_on, )
            if isinstance(handler.end_on, str):
                handler.end_on = (handler.end_on, )
            for match_on in (match + handler.start_on):
                self.routes[match_on] = handler
            return handler
        return decorator

    @property
    def match_on(self):
        return tuple(self.routes.keys())


    def __getitem__(self, item):
        return self.routes[item]

    def get(self, *args):
        return self.routes.get(*args)

    def excluding(self, *routes):
        new_router = deepcopy(self)
        for route in routes:
            del new_router.routes[route]

        return new_router
