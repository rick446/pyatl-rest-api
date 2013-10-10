from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import pyramid.httpexceptions as exc

models = {}


def get_models(request):
    return models


def create_model(request):
    key = request.json['key']
    value = request.json['value']
    models[key] = value
    request.response.status_int = 201
    return value


def get_model(request):
    model = models[request.matchdict['key']]
    return model


def put_model(request):
    model = models[request.matchdict['key']]
    model.update(request.json)
    return model


def delete_model(request):
    models.pop(request.matchdict['key'], None)
    return exc.HTTPNoContent()


config = Configurator()
config.add_route('models', '/')
config.add_route('model', '/{key}/')
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
