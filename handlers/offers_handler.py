from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin

from base.base_handler import BankExObjectHandler, TemplateMixin
from base.base_server_error import BankExServerError
from models.offer import Offer
from models.user import Admin
from settings import options
from utils import gen_path, mkdir


class OffersHandler(AuthMixin, TemplateMixin, BankExObjectHandler):
    MODEL_CLS = Offer

    @property
    def queryset(self):
        return Offer.objects.all().order_by('-creation_date')

    @property
    def put_fields(self):
        return {
            'type': {'field_type': 'str'},
            'description': {'field_type': 'str'},
            'price': {'field_type': 'str'}
        }

    @property
    def auth_classes(self):
        return [Admin]

    @need_role([Admin.role])
    def get_object(self):
        return super(OffersHandler, self).get_object()

    @need_role([Admin.role])
    def put_object(self, updated_object=None):
        super(OffersHandler, self).put_object(updated_object)

    def save_logic(self, some_object):
        some_object.save(validate=False)
        self.send_success_response(data=some_object.to_dict())
