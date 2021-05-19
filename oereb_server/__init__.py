# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.events import NewRequest

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        # 'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        # 'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        # 'Access-Control-Allow-Credentials': 'true',
        # 'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

__version__ = '2.2.4'

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_oereb')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('wo_redirect', '/wo_redirect')
    config.add_route('version', '/version')
    config.add_route('home', '/')
    config.scan()
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    return config.make_wsgi_app()
