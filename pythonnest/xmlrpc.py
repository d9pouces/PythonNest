# coding=utf-8
from functools import lru_cache
from importlib import import_module
import logging
from xmlrpc.client import loads, dumps
from xmlrpc.client import Fault
from django.conf import settings
from django.http.response import HttpResponse
from django.views.decorators.cache import never_cache

from djangofloor.decorators import Connection

logger = logging.getLogger('django.request')


class XMLRPCSite(object):
    def __init__(self):
        self.methods = {}

    # @never_cache()
    def dispatch(self, request):
        import_rpc_methods()
        rpc_call = loads(request.body.decode('utf-8'))
        rpc_args = rpc_call[0]
        method_name = rpc_call[1]
        try:
            connection = self.methods[method_name]
            src_result = connection(request, *rpc_args)
            result = src_result,
        except Exception as e:
            logger.exception('Exception in XML RPC call')
            result = Fault(e.__class__.__name__, str(e))
        data = dumps(result, method_name, True)
        return HttpResponse(data, content_type='application/xml+rpc')


@lru_cache()
def import_rpc_methods():
    """Import all `signals.py` files to register signals.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('%s.rpc_api' % app)
        except ImportError:
            pass


site = XMLRPCSite()


class XMLRPCWrapper(Connection):
    required_function_arg = 'request'

    def __init__(self, xml_rpc_site, fn, path=None):
        self.site = xml_rpc_site
        super(XMLRPCWrapper, self).__init__(fn, path=path)

    def register(self):
        self.site.methods[self.path.rpartition('.')[2]] = self

    def __call__(self, request, *args):
        return self.function(request, *args)


def register_rpc_method(fn=None, name=None):
    def wrapped(fn_):
        wrapper = XMLRPCWrapper(site, fn_, path=name)
        wrapper.register()
        return fn_
    if fn is not None:
        wrapped = wrapped(fn)
    return wrapped
