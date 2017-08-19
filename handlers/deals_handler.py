from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin
from base.base_handler import BankExObjectHandler, TemplateMixin
from models.deal import Deal
from models.user import Admin


class DealsHandler(AuthMixin, TemplateMixin, BankExObjectHandler):
    MODEL_CLS = Deal

    @property
    def queryset(self):
        return Deal.objects.all().order_by('-creation_date')

    @property
    def put_fields(self):
        return {
            'title': {'field_type': 'str'},
            'description': {'field_type': 'str'},
            'location': {'field_type': 'str'},
            'price': {'field_type': 'str'}
        }

    @property
    def auth_classes(self):
        return [Admin]

    @need_role([Admin.role])
    def get_object(self):
        return super(DealsHandler, self).get_object()

    @need_role([Admin.role])
    def put_object(self, updated_object=None):
        super(DealsHandler, self).put_object(updated_object)
