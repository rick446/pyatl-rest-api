from pyramid.view import view_config
import pyramid.httpexceptions as exc

from .model import Model


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
    return request.context


@view_config(route_name='model', request_method='PUT', renderer='json')
def put_model(request):
    request.context.update(request.json)
    return request.context


@view_config(route_name='model', request_method='DELETE', renderer='json')
def delete_model(request):
    request.context.delete()
    return exc.HTTPNoContent()


@view_config(context=exc.HTTPError, renderer='json')
def on_error(exception, request):
    request.response.status_int = exception.status_int
    return dict(
        status=exception.status,
        errors=repr(exception))
