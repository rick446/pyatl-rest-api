from pyramid.config import Configurator

from .model import Model


def main(global_settings, **local_settings):
    config = Configurator()
    config.add_route('models', '/')
    config.add_route('model', '/{key}/', factory=Model.lookup)
    config.scan('pyramid_decorators.views')
    simple_app = config.make_wsgi_app()
    return simple_app
