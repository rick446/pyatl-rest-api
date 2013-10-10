from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def simple_view(request):
    return Response('Got something')


config = Configurator()
config.add_route('root', '/')
config.add_view(simple_view, route_name='root')
simple_app = config.make_wsgi_app()


httpd = make_server('', 8000, simple_app)
httpd.serve_forever()
