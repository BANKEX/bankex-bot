import traceback

import mongoengine
from mongoengine import StringField, IntField, DateTimeField, ReferenceField, DictField
from roboman.keyboard import ReplyKeyboard, ReplyKeyboardHide
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClient
from tornkts import utils
from tornkts.base.mongodb import BaseDocument
from datetime import datetime
from pytz import timezone
from tornkts.utils import PasswordHelper, mkdir
from models.content import Text
from utils import get_screenshot_img_url, gen_path
from settings import options


class Offer(BaseDocument):
    TYPE_CREDIT = 'credit'
    TYPE_FUTURES = 'futures'
    TYPE_FACTORING = 'factoring'

    salesman = ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY, default=None)
    type = StringField(choices=(TYPE_CREDIT, TYPE_FUTURES, TYPE_FACTORING), default=None)

    description = StringField(default=None)
    zip_code = StringField(default=None)
    reg_service = StringField(default=None)
    options = DictField(default={})
    price = IntField(default=None)

    bc_hash = StringField(default=None)

    ru_card = DictField(default=None)
    en_card = DictField(default=None)

    creation_date = DateTimeField()
    update_date = DateTimeField()

    @property
    def fprice(self):
        try:
            return '{:,}'.format(self.price).replace(',', ' ')
        except:
            return ''

    def process(self, bot):
        offer_type = bot.match_command(bot.t(['SELL_CREDIT', 'SELL_FUTURES', 'SELL_FACTORING']))
        if offer_type and self.type is None:
            self.set_type(bot, offer_type.get('command'))
            if self.type == self.TYPE_CREDIT:
                return bot.send(
                    bot.t('CREDIT_ENTER_DESC'),
                    reply_markup=ReplyKeyboardHide()
                )
            elif self.type == self.TYPE_FUTURES:
                return bot.send(
                    bot.t('FUTURES_ENTER_DESC'),
                    reply_markup=ReplyKeyboardHide()
                )
            elif self.type == self.TYPE_FACTORING:
                return bot.send(
                    bot.t('FACTORING_ENTER_DESC'),
                    reply_markup=ReplyKeyboardHide()
                )

        if self.type == self.TYPE_CREDIT:
            self._process_credit(bot)
        elif self.type == self.TYPE_FUTURES:
            self._process_futures(bot)
        elif self.type == self.TYPE_FACTORING:
            self._process_factoring(bot)

    def _process_credit(self, bot):
        if self.description is None:
            self.description = bot.text
            bot.send(bot.t('CREDIT_ENTER_ZIP'))
        elif self.zip_code is None:
            self.zip_code = bot.text
            bot.send(bot.t('CREDIT_ENTER_REG_SERVICE'))
        elif self.reg_service is None:
            self.reg_service = bot.text
            bot.send(bot.t('CREDIT_ENTER_LOAN_ID'))
        elif self.options.get('loan_id') is None:
            self.options['loan_id'] = bot.text
            bot.send(bot.t('CREDIT_ENTER_LOAN_AMOUNT'))
        elif self.options.get('loan_amount') is None:
            self.options['loan_amount'] = utils.to_int(bot.text, None)
            if self.options['loan_amount'] is None:
                return bot.send(bot.t('ENTER_NUMBER'))
            bot.send(bot.t('CREDIT_ENTER_INTEREST_RATE'))
        elif self.options.get('interest_rate') is None:
            self.options['interest_rate'] = bot.text
            bot.send(bot.t('CREDIT_ENTER_LOAN_LENGTH'))
        elif self.options.get('loan_length') is None:
            self.options['loan_length'] = bot.text
            bot.send(
                bot.t('CREDIT_ENTER_LOAN_STATUS'),
                reply_markup=ReplyKeyboard(
                    [
                        [bot.t('LOAN_STATUS_EARLY')],
                        [bot.t('LOAN_STATUS_NORMAL')],
                        [bot.t('LOAN_STATUS_LATE')]
                    ]
                )
            )
        elif self.options.get('loan_status') is None:
            self.options['loan_status'] = bot.text
            bot.send(
                bot.t('CREDIT_ENTER_SELLERS_WARRANTY'),
                reply_markup=ReplyKeyboard(
                    [
                        [bot.t('WARRANTY_FULL'), bot.t('WARRANTY_PARTLY'), bot.t('WARRANTY_NONE')]
                    ],
                    one_time_keyboard=True
                )
            )
        elif self.options.get('sellers_warranty') is None:
            self.options['sellers_warranty'] = bot.text
            bot.send(
                bot.t('CREDIT_ENTER_PRICE'),
                reply_markup=ReplyKeyboardHide()
            )
        elif self.price is None:
            self.price = utils.to_int(bot.text, None)
            if self.price is None:
                return bot.send(bot.t('ENTER_NUMBER'))
            self._create_contract_send(bot)
        else:
            self._create_contract_process(bot)

    def _process_futures(self, bot):
        if self.description is None:
            self.description = bot.text
            bot.send(bot.t('FUTURES_ENTER_ZIP'))
        elif self.zip_code is None:
            self.zip_code = bot.text
            bot.send(bot.t('FUTURES_ENTER_REG_SERVICE'))
        elif self.reg_service is None:
            self.reg_service = bot.text
            bot.send(bot.t('FUTURES_ENTER_LOAN_ID'))
        elif self.options.get('loan_id') is None:
            self.options['loan_id'] = bot.text
            bot.send(
                bot.t('FUTURES_CHOOSE_CONTRACT_TYPE'),
                reply_markup=ReplyKeyboard(
                    [
                        [bot.t('FUTURES_TYPE_SETTLEMENT')],
                        [bot.t('FUTURES_TYPE_DELIVERABLE')],
                    ],
                    one_time_keyboard=True
                )
            )
        elif self.options.get('contract_type') is None:
            self.options['contract_type'] = bot.text
            bot.send(
                bot.t('FUTURES_ENTER_CONTRACT_SIZE'),
                reply_markup=ReplyKeyboardHide()
            )
        elif self.options.get('contract_size') is None:
            self.options['contract_size'] = bot.text
            bot.send(bot.t('FUTURES_CONTRACT_MATURITY'))
        elif self.options.get('contract_maturity') is None:
            self.options['contract_maturity'] = bot.text
            bot.send(bot.t('FUTURES_ENTER_DELIVERY_DATE'))
        elif self.options.get('delivery_date') is None:
            self.options['delivery_date'] = bot.text
            bot.send(bot.t('FUTURES_PRICE'))
        elif self.price is None:
            self.price = utils.to_int(bot.text, None)
            if self.price is None:
                return bot.send(bot.t('ENTER_NUMBER'))
            self._create_contract_send(bot)
        else:
            self._create_contract_process(bot)

    def _process_factoring(self, bot):
        if self.description is None:
            self.description = bot.text
            bot.send(bot.t('FACTORING_ENTER_ZIP'))
        elif self.zip_code is None:
            self.zip_code = bot.text
            bot.send(bot.t('FACTORING_ENTER_REG_SERVICE'))
        elif self.reg_service is None:
            self.reg_service = bot.text
            bot.send(bot.t('FACTORING_ENTER_LOAN_ID'))
        elif self.options.get('loan_id') is None:
            self.options['loan_id'] = bot.text
            bot.send(
                bot.t('FACTORING_PAY_REQS'),
                reply_markup=ReplyKeyboard(
                    [
                        [bot.t('FACTORING_REGRESS')],
                        [bot.t('FACTORING_NO_REGRESS')],
                    ],
                    one_time_keyboard=True
                )
            )
        elif self.options.get('pay_reqs') is None:
            self.options['pay_reqs'] = bot.text
            bot.send(
                bot.t('FACTORING_TITLE_SUPPLIER'),
                reply_markup=ReplyKeyboardHide()
            )
        elif self.options.get('title_supplier') is None:
            self.options['title_supplier'] = bot.text
            bot.send(bot.t('FACTORING_SUM_REQS'))
        elif self.options.get('sum_reqs') is None:
            self.options['sum_reqs'] = bot.text
            bot.send(bot.t('FACTORING_DATE_REQS_PAY'))
        elif self.options.get('date_reqs_pay') is None:
            self.options['date_reqs_pay'] = bot.text
            bot.send(bot.t('FACTORING_PRICE'))
        elif self.price is None:
            self.price = utils.to_int(bot.text, None)
            if self.price is None:
                return bot.send(bot.t('ENTER_NUMBER'))
            self._create_contract_send(bot)
        else:
            self._create_contract_process(bot)

    @gen.coroutine
    def _create_contract_send(self, bot):
        try:
            bot.send(bot.t('GENERATE_PREVIEW_START'))

            yield self.generate_img(lang=bot.user.lang)

            path = self.get_image_path(bot.user.lang)
            if not path:
                raise Exception

            with open(path, 'rb') as f:
                yield bot.send_photo(
                    files=(('photo', path, f.read()),),
                    caption=bot.t('GENERATE_PREVIEW_END')
                )
        except Exception as e:
            bot.send(bot.t('GENERATE_PREVIEW_FAIL'))
            traceback.print_exc()

        bot.send(
            bot.t('SAIL_YOU_CREATE_CONTRACT'),
            reply_markup=ReplyKeyboard(
                [[bot.t('YES_APPROVE'), bot.t('NO_FEAR'), bot.t('WHAT_IS_BLOCKCHAIN')]],
                one_time_keyboard=False
            )
        )

    @gen.coroutine
    def _create_contract_process(self, bot):
        if bot.match_command(bot.t('YES_APPROVE')):
            bot.send(
                bot.t('REGISTER_BC_BEGIN'),
                reply_markup=ReplyKeyboardHide()
            )

            # рега в реестре
            yield gen.sleep(1)
            self.bc_hash = PasswordHelper.get_hash(datetime.now().isoformat())

            # генерация картинок
            yield self.generate_img()

            self.salesman = self.salesman
            self.save()

            bot._on_start(
                welcome_text=bot.t('REGISTER_BC_END'),
                keyboard=ReplyKeyboard([[bot.t('THNX_UNDERSTAND')]])
            )
        elif bot.match_command(bot.t('NO_FEAR')):
            bot._on_start(welcome_text=bot.t('FEAR_BLOCKCHAIN_WIKI'))
        elif bot.match_command(bot.t('WHAT_IS_BLOCKCHAIN')):
            bot.send(bot.t('WHAT_IS_BLOCKCHAIN_WIKI'))

    @gen.coroutine
    def generate_img(self, sync=False, *args, **kwargs):
        if sync:
            client = HTTPClient()
        else:
            client = AsyncHTTPClient()

        if kwargs.get('lang') in [None, Text.LANG_RU]:
            # генерация русской карточки
            req = HTTPRequest(get_screenshot_img_url(self.get_id(), Text.LANG_RU))
            if sync:
                res = client.fetch(req)
            else:
                res = yield client.fetch(req)

            ru_path = gen_path()
            mkdir(ru_path.get('folder'))
            with open(ru_path.get('fullname'), "wb") as f:
                f.write(res.body)

            self.ru_card = ru_path

        if kwargs.get('lang') in [None, Text.LANG_EN]:
            # генерация английской карточки
            req = HTTPRequest(get_screenshot_img_url(self.get_id(), Text.LANG_EN))
            if sync:
                res = client.fetch(req)
            else:
                res = yield client.fetch(req)

            en_path = gen_path()
            mkdir(en_path.get('folder'))
            with open(en_path.get('fullname'), "wb") as f:
                f.write(res.body)

            self.en_card = en_path

    def get_image_path(self, lang):
        path = None

        if lang == Text.LANG_RU:
            if self.ru_card is None:
                return False
            path = self.ru_card.get('relname')
        elif lang == Text.LANG_EN:
            if self.en_card is None:
                return False
            path = self.en_card.get('relname')

        if path is None:
            return False

        return '%s/%s' % (options.upload_path, path)

    def set_type(self, bot, offer_type):
        if offer_type == bot.t('SELL_CREDIT'):
            self.type = Offer.TYPE_CREDIT
        elif offer_type == bot.t('SELL_FUTURES'):
            self.type = Offer.TYPE_FUTURES
        elif offer_type == bot.t('SELL_FACTORING'):
            self.type = Offer.TYPE_FACTORING

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now(tz=timezone('UTC'))
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Offer, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'type': self.type,
            'description': self.description,
            'creation_date': self.creation_date,
            'zip_code': self.zip_code,
            'reg_service': self.reg_service,
            'options': self.options,
            'price': self.price,
            'salesman': self.salesman.to_dict() if self.salesman else None,
            'bc_hash': self.bc_hash
        }
