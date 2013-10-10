from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def simple_get(request):
    return Response('Got something')


def simple_post(request):
    return Response('Posted something')


def simple_put(request):
    return Response('Put something')


def simple_delete(request):
    return Response('Deleted something')


config = Configurator()
config.add_route('root', '/')
config.add_view(simple_get, route_name='root', request_method='GET')
config.add_view(simple_post, route_name='root', request_method='POST')
config.add_view(simple_put, route_name='root', request_method='PUT')
config.add_view(simple_delete, route_name='root', request_method='DELETE')
simple_app = config.make_wsgi_app()


httpd = make_server('', 8000, simple_app)
httpd.serve_forever()
