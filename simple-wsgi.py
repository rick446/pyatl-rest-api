from wsgiref.simple_server import make_server


def simple_app(environ, start_response):
    for k, v in sorted(environ.items()):
        print '%s: %s...' % (k, repr(v)[:40])
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['WSGI server here\n']

httpd = make_server('', 8000, simple_app)
httpd.serve_forever()
