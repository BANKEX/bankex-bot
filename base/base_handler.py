from os.path import dirname

from datetime import datetime

from raven.contrib.tornado import SentryMixin
from tornkts import utils
from tornkts.handlers import BaseHandler
from tornkts.handlers.object_handler import ObjectHandler
from tornado import template
from tornado.escape import xhtml_escape
from settings import options


class BankExBaseHandler(SentryMixin, BaseHandler):
    _payload = None

    def _capture(self, call_name, data=None, **kwargs):
        if options.debug == False:
            return super(BankExBaseHandler, self)._capture(call_name, data, **kwargs)

    def get_argument(self, name, default=BaseHandler._ARG_DEFAULT, strip=True, **kwargs):
        if self.request.method == 'POST':
            if self._payload is None:
                try:
                    self._payload = utils.json_loads(self.request.body)
                except:
                    pass
            if self._payload and name in self._payload:
                return self._payload[name]
            else:
                return super(BankExBaseHandler, self).get_argument(name, default, strip)
        else:
            return super(BankExBaseHandler, self).get_argument(name, default, strip)


class BankExObjectHandler(SentryMixin, ObjectHandler):
    _payload = None

    def _capture(self, call_name, data=None, **kwargs):
        if options.debug == False:
            return super(BankExObjectHandler, self)._capture(call_name, data, **kwargs)

    def get_argument(self, name, default=BaseHandler._ARG_DEFAULT, strip=True, **kwargs):
        if self.request.method == 'POST':
            if self._payload is None:
                try:
                    self._payload = utils.json_loads(self.request.body)
                except:
                    pass
            if self._payload and name in self._payload:
                return self._payload[name]
            else:
                return super(BankExObjectHandler, self).get_argument(name, default, strip)
        else:
            return super(BankExObjectHandler, self).get_argument(name, default, strip)


class TemplateMixin(object):
    __template_loader = False

    def range(self, begin, end, min=None, max=None):
        if min is not None and begin < min:
            begin = min
        if min is not None and end > max:
            end = max
        if begin > end:
            begin = end
        return range(begin, end)

    def nl2br(self, string):
        string = xhtml_escape(string)
        return string.replace('\n\t', '<br/>').replace('\n', '<br/>')

    def capitalize(self, string):
        string = str(string)
        if len(string) > 0:
            string = string[0].upper() + string[1:]
        return string

    def create_url(self, url, params=None):
        if params is None:
            params = {}

        url_and_args = str(url).split('?', 1)
        url = url_and_args[0]
        args = {}
        if len(url_and_args) > 1:
            for arg in url_and_args[1].split('&'):
                split_arg = arg.split('=', 1)

                key = split_arg[0]
                value = None
                if len(split_arg) > 1:
                    value = split_arg[1]

                args[key] = value

        for k, v in params.items():
            args[k] = v

        if len(args) == 0:
            return url
        else:
            return '%s?%s' % (url, '&'.join(['%s=%s' % (k, v) for k, v in args.items()]))

    def get_template_loader(self):
        if not self.__template_loader:
            self.__template_loader = template.Loader(dirname(dirname(__file__)) + '/templates')
            self.__template_loader.namespace = self.get_template_namespace()
            self.__template_loader.namespace['nl2br'] = self.nl2br
            self.__template_loader.namespace['date'] = datetime.now().strftime
            self.__template_loader.namespace['range'] = self.range
            self.__template_loader.namespace['create_url'] = self.create_url
            self.__template_loader.namespace['current_user'] = self.current_user
            self.__template_loader.namespace['capitalize'] = self.capitalize
            self.__template_loader.namespace['options'] = options
        return self.__template_loader

    def render(self, template, data=None):
        if data is None:
            data = {}
        data['url'] = self.request.uri
        loader = self.get_template_loader()

        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.write(loader.load(template).generate(**data), nocontenttype=True)
