import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField
from tornkts.base.mongodb.user import User as BaseUser
from tornkts.base.mongodb.user import BaseAdmin
from datetime import datetime
from pytz import timezone
from models.deal import Deal
from models.offer import Offer


class Admin(BaseAdmin):
    role = 'admin'
    meta = {
        'collection': role
    }


class User(BaseUser):
    ACTION_BUY = 'buy'
    ACTION_SELL = 'sell'

    STEP_CHOOSING = 0
    STEP_BLOCKCHAIN = 1

    out_id = IntField(unique=True)
    lang = StringField(default=None)

    name = StringField()
    surname = StringField()
    username = StringField()

    filter_buy_type = StringField(choices=(Offer.TYPE_CREDIT, Offer.TYPE_FUTURES, Offer.TYPE_FACTORING), default=None)
    filter_price = IntField(default=None)
    offset = IntField(default=0)
    buy_step = IntField(default=STEP_CHOOSING)

    current_action = StringField(choices=(ACTION_BUY, ACTION_SELL), default=None)
    current_offer = ReferenceField(Offer, reverse_delete_rule=mongoengine.NULLIFY, required=False, default=None)
    current_deal = ReferenceField(Deal, reverse_delete_rule=mongoengine.NULLIFY, required=False, default=None)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    def reset(self):
        self.offset = -1
        self.current_deal = None
        self.current_action = None
        self.current_offer = None
        self.filter_buy_type = None
        self.filter_price = None
        self.buy_step = User.STEP_CHOOSING

    def set_filter_buy_type(self, bot, offer_type):
        if offer_type == bot.t('BUY_CREDIT'):
            self.filter_buy_type = Offer.TYPE_CREDIT
        elif offer_type == bot.t('BUY_FUTURES'):
            self.filter_buy_type = Offer.TYPE_FUTURES
        elif offer_type == bot.t('BUY_FACTORING'):
            self.filter_buy_type = Offer.TYPE_FACTORING

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(User, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'out_id': self.out_id,
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'creation_date': self.creation_date
        }
