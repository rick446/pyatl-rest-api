import pyramid.httpexceptions as exc


class Model(object):
    models = {}

    def __init__(self, key, data):
        self.key = key
        self.data = data

    @classmethod
    def lookup(cls, request):
        key = request.matchdict['key']
        try:
            return cls.models[key]
        except KeyError:
            raise exc.HTTPNotFound()

    def save(self):
        if self.key in self.models:
            raise exc.HTTPConflict()
        self.models[self.key] = self

    def update(self, data):
        self.data.update(data)

    def delete(self):
        del self.models[self.key]

    def __json__(self, request=None):
        return self.data
