from base.base_handler import BankExObjectHandler
from models.user import Admin
from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin
from models.content import Text


class TextsHandler(AuthMixin, BankExObjectHandler):
    MODEL_CLS = Text

    @property
    def get_methods(self):
        methods = {
            'keys': self.keys
        }
        methods.update(super(TextsHandler, self).get_methods)
        return methods

    @property
    def queryset(self):
        return Text.objects.all().order_by('key')

    @property
    def auth_classes(self):
        return [Admin]

    @property
    def put_fields(self):
        return {
            'lang': {'field_type': 'str'},
            'key': {'field_type': 'str'},
            'value': {'field_type': 'str'},
            'comment': {'field_type': 'str'}
        }

    @need_role([Admin.role])
    def get_object(self):
        return super(TextsHandler, self).get_object()

    @need_role([Admin.role])
    def keys(self):
        keys = list(Text.defaults().keys())
        keys.sort()
        self.send_success_response(data=keys)
