import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField
from tornkts.base.mongodb import BaseDocument
from datetime import datetime
from pytz import timezone
from models.offer import Offer


class Deal(BaseDocument):
    STEP_NEW = 0
    STEP_BLOCKCHAIN = 1
    STEP_QIWI = 2
    STEP_WAIT_SALEMAN = 3

    offer = ReferenceField(Offer, reverse_delete_rule=mongoengine.NULLIFY, required=True)
    user = ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY, required=True)
    step = IntField(default=STEP_NEW)
    bc_hash = StringField(default=None)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Deal, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'user': self.user.to_dict() if self.user else None,
            'offer': self.offer.to_dict() if isinstance(self.offer, Offer) else None,
            'salesman': self.offer.salesman.to_dict() if isinstance(self.offer, Offer) and self.offer.salesman else None,
            'bc_hash': self.bc_hash,
            'creation_date': self.creation_date
        }
