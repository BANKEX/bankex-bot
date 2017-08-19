from base.base_handler import BankExObjectHandler
from models.user import Admin, User
from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin


class UsersHandler(AuthMixin, BankExObjectHandler):
    MODEL_CLS = User

    @property
    def queryset(self):
        return User.objects.all().order_by('-creation_date')

    @property
    def auth_classes(self):
        return [Admin]

    @need_role([Admin.role])
    def get_object(self):
        return super(UsersHandler, self).get_object()
