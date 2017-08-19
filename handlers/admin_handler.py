from base.base_handler import BankExObjectHandler
from models.user import Admin
from tornkts.auth import need_role
from tornkts.mixins.auth_mixin import AuthMixin


class AdminHandler(AuthMixin, BankExObjectHandler):
    MODEL_CLS = Admin

    @property
    def auth_classes(self):
        return [Admin]

    @property
    def put_fields(self):
        return {
            'email': {'field_type': 'email'},
            'name': {'field_type': 'str'},
            'password': {'field_type': 'str', 'require_if_none': True, 'hash': True, 'length_min': 8}
        }

    @property
    def post_methods(self):
        methods = {
            'auth': self.auth,
            'logout': self.logout
        }
        methods.update(super(AdminHandler, self).post_methods)
        return methods

    @property
    def get_methods(self):
        methods = {
            "info": self.info
        }
        methods.update(super(AdminHandler, self).get_methods)
        return methods

    @need_role([Admin.role])
    def get_object(self):
        return super(AdminHandler, self).get_object()

    @need_role([Admin.role])
    def info(self):
        self.send_success_response(data={
            'items': [
                self.current_user.to_dict()
            ]
        })

    @need_role([Admin.role])
    def logout(self):
        self.session_destroy()
        self.send_success_response()