from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import pyramid.httpexceptions as exc


# Define our model/resource class
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


# Define our views
def get_models(request):
    return Model.models


def create_model(request):
    model = Model(request.json['key'], request.json['value'])
    model.save()
    return model


def get_model(request):
    return request.context


def put_model(request):
    request.context.update(request.json)
    return request.context


def delete_model(request):
    request.context.delete()
    return exc.HTTPNoContent()


config = Configurator()
config.add_route('models', '/')
config.add_route('model', '/{key}/', factory=Model.lookup)
config.add_view(
    get_models, route_name='models', request_method='GET', renderer='json')
config.add_view(
    create_model, route_name='models', request_method='POST', renderer='json')
config.add_view(
    get_model, route_name='model', request_method='GET', renderer='json')
config.add_view(
    put_model, route_name='model', request_method='PUT', renderer='json')
config.add_view(
    delete_model, route_name='model', request_method='DELETE')
simple_app = config.make_wsgi_app()


httpd = make_server('', 8000, simple_app)
httpd.serve_forever()
