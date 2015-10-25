from aiohttp import web
from .trender import TRender

_templates = {}


def template(template_name):
    # register this template name
    _templates[template_name] = None

    def wrapper(func):

        async def wrapped(self, request):
            namespace = await func(self, request)
            text = _templates[template_name].render(namespace)
            return web.Response(body=text.encode('utf-8'))
        return wrapped
    return wrapper


def setup_template_loader(template_path):
    for template_name in _templates:
        _templates[template_name] = TRender(template_name, path=template_path)
