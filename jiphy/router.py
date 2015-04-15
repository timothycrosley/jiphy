from collections import OrderedDict

class Router(object):
    __slots__ = ('routes', )

    def __init__(self, *routes):
        self.routes = OrderedDict()
        for route in routes:
            self.add(*route[1:])(route[0])

    def add(self, *match):
        def decorator(handler):
            if isinstance(handler.start_on, (str, unicode)):
                handler.start_on = (handler.start_on, )
            if isinstance(handler.end_on, (str, unicode)):
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
