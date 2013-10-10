from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import pyramid.httpexceptions as exc


def main():
    config = Configurator()
    config.add_route('models', '/')
    config.add_route('model', '/{key}/')
    config.scan()
    simple_app = config.make_wsgi_app()
    return simple_app


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
@view_config(route_name='models', request_method='GET', renderer='json')
def get_models(request):
    return Model.models


@view_config(route_name='models', request_method='POST', renderer='json')
def create_model(request):
    model = Model(request.json['key'], request.json['value'])
    model.save()
    return model


@view_config(route_name='model', request_method='GET', renderer='json')
def get_model(request):
    return request.context.model


@view_config(route_name='model', request_method='PUT', renderer='json')
def put_model(request):
    request.context.model.update(request.json)
    return request.context.model


@view_config(route_name='model', request_method='DELETE', renderer='json')
def delete_model(request):
    request.context.model.delete()
    return exc.HTTPNoContent()


@view_config(context=exc.HTTPError, renderer='json')
def on_error(exception, request):
    request.response.status_int = exception.status_int
    return dict(
        status=exception.status,
        errors=repr(exception))


if __name__ == '__main__':
    simple_app = main()
    httpd = make_server('', 8000, simple_app)
    httpd.serve_forever()
