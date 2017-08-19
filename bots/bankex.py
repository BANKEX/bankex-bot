# coding=utf-8
from datetime import datetime

from mongoengine import Q
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornkts import utils
from tornkts.utils import PasswordHelper

from models.deal import Deal
from models.user import User, Offer
from models.content import Text
from roboman.bot import BaseBot
from roboman.keyboard import ReplyKeyboard, InlineKeyboard, InlineKeyboardButton, ReplyKeyboardHide
from settings import options
import traceback
import emoji


class BankExBot(BaseBot):
    name = 'TestBankExCustomer'
    key = options.key_bank_ex_customer
    client = AsyncHTTPClient()

    def __init__(self, user=None, chat_id=None):
        super().__init__()
        self.user = user
        self.chat_id = chat_id

    def t(self, key, *args):
        if isinstance(key, list):
            return [Text.format(item, self.user.lang, *args) for item in key]
        else:
            return Text.format(key, self.user.lang, *args)

    def _before_hook(self, data):
        try:
            user = User.objects.get(out_id=data.get('from_id'))
            user.username = data.get('from_username')
            user.save()
        except User.DoesNotExist:
            user = User(
                out_id=data.get('from_id'),
                name=data.get('from_first_name'),
                surname=data.get('from_last_name'),
                username=data.get('from_username')
            )
            user.save()

        data['user'] = user
        self.user = user
        return data

    def _on_hook(self, data):
        if self.match_command('/lang'):
            self.user.lang = None
            self.user.save()

        if self.user.lang is None and self._choose_lang():
            return

        if self.match_command('/start'):
            return self._on_start(**data)
        elif self.match_command(self.t('THNX_UNDERSTAND')):
            data['welcome_text'] = self.t('CHOOSE_DIRECTION')
            return self._on_start(**data)

        if self.match_command(self.t('DEAL_SELL')):
            self.user.current_action = User.ACTION_SELL
            self.user.save()
            return self.send(
                self.t('DEAL_SELL_INTRO'),
                reply_markup=ReplyKeyboard(
                    [
                        [self.t('SELL_CREDIT')],
                        [self.t('SELL_FUTURES')],
                        [self.t('SELL_FACTORING')]
                    ],
                    one_time_keyboard=True
                )
            )
        elif self.match_command(self.t('DEAL_BUY')):
            self.user.current_action = User.ACTION_BUY
            self.user.save()
            return self.send(
                self.t('DEAL_BUY_INTRO'),
                reply_markup=ReplyKeyboard(
                    [
                        [self.t('BUY_CREDIT')],
                        [self.t('BUY_FUTURES')],
                        [self.t('BUY_FACTORING')]
                    ],
                    one_time_keyboard=True
                )
            )

        if self.user.current_action == User.ACTION_SELL:
            self._selling(**data)
        elif self.user.current_action == User.ACTION_BUY:
            self._buying(**data)

    def _choose_lang(self):
        EN = emoji.emojize(':flag_for_United_States:') + ' English'
        RU = emoji.emojize(':flag_for_Russia:') + ' Русский'

        if self.match_command(EN):
            self.user.lang = Text.LANG_EN
        elif self.match_command(RU):
            self.user.lang = Text.LANG_RU
        else:
            self.send(
                self.t('CHOOSE_LANG'),
                reply_markup=ReplyKeyboard([[EN, RU]])
            )
            return True

        self.user.save()
        if self.user.current_action is None:
            self.text = '/start'
        else:
            return True

    def _on_start(self, **kwargs):
        self.user.reset()
        self.user.save()

        welcome_text = kwargs.get('welcome_text')
        keyboard = ReplyKeyboard([[self.t('DEAL_SELL'), self.t('DEAL_BUY')]])

        self.send(
            welcome_text if welcome_text else self.t('WELCOME'),
            reply_markup=kwargs.get('keyboard') if kwargs.get('keyboard') else keyboard
        )

    def _selling(self, **kwargs):
        current_offer = self.user.current_offer
        if current_offer is None:
            current_offer = Offer()
            current_offer.salesman = self.user
            current_offer.save()

            self.user.current_offer = current_offer
            self.user.save()

        current_offer.process(self)
        current_offer.salesman = current_offer.salesman
        current_offer.save()

    @gen.coroutine
    def _buying(self, **kwargs):
        buy_keyboard = ReplyKeyboard([[
            self.t('DEAL_BUY_PREV'),
            self.t('DEAL_BUY_NEW_SEARCH'),
            self.t('DEAL_BUY_NEXT'),
        ]], one_time_keyboard=False)

        if kwargs.get('callback_query'):
            try:
                offer = Offer.objects.get(id=kwargs.get('callback_query'))
            except Exception:
                return

            deal = Deal()
            deal.user = self.user
            deal.offer = offer
            deal.save()

            self.user.buy_step = User.STEP_BLOCKCHAIN
            self.user.current_deal = deal
            self.user.save()

            self.send(
                self.t('BUY_YOU_CREATE_CONTRACT'),
                reply_markup=ReplyKeyboard(keyboard=[[
                    self.t('YES_APPROVE'),
                    self.t('NO_FEAR'),
                    self.t('WHAT_IS_BLOCKCHAIN'),
                ]])
            )

            self.answer_callback_query(callback_query_id=kwargs.get('callback_query_id'))
            return

        if self.user.buy_step == User.STEP_BLOCKCHAIN:
            if self.match_command(self.t('YES_APPROVE')):
                self.send(
                    self.t('REGISTER_BC_BEGIN'),
                    reply_markup=ReplyKeyboardHide()
                )
                yield gen.sleep(5)

                self.user.current_deal.bc_hash = PasswordHelper.get_hash(datetime.now().isoformat())
                self.user.current_deal.user = self.user.current_deal.user
                self.user.current_deal.save()

                return self._on_start(
                    welcome_text=self.t('BEGIN_DEAL'),
                    keyboard=ReplyKeyboard([[self.t('THNX_UNDERSTAND')]])
                )
            elif self.match_command(self.t('NO_FEAR')):
                return self._on_start(welcome_text=self.t('FEAR_BLOCKCHAIN_WIKI'))
            elif self.match_command(self.t('WHAT_IS_BLOCKCHAIN')):
                return self.send(self.t('WHAT_IS_BLOCKCHAIN_WIKI'))

        offer_type = self.match_command(self.t(['BUY_CREDIT', 'BUY_FUTURES', 'BUY_FACTORING']))
        if self.user.filter_buy_type is None:
            if not offer_type:
                return self.send(self.t('ENTER_CORRECT_CONTRACT_TYPE'))

            self.user.set_filter_buy_type(self, offer_type.get('command'))
            self.user.save()

            if self.user.filter_buy_type == Offer.TYPE_CREDIT:
                return self.send(
                    self.t('DEAL_BUY_CREDIT_PRICE'),
                    reply_markup=ReplyKeyboardHide()
                )
            elif self.user.filter_buy_type == Offer.TYPE_FUTURES:
                return self.send(
                    self.t('DEAL_BUY_FUTURES_PRICE'),
                    reply_markup=ReplyKeyboardHide()
                )
            elif self.user.filter_buy_type == Offer.TYPE_FACTORING:
                return self.send(
                    self.t('DEAL_BUY_FACTORING_PRICE'),
                    reply_markup=ReplyKeyboardHide()
                )
        elif self.user.filter_price is None:
            self.user.filter_price = utils.to_int(self.text, None)
            self.user.save()

            if self.user.filter_price is None:
                return self.send(self.t('ENTER_NUMBER'))

            return self.send(self.t('DEAL_BUY_MANUAL'),reply_markup=buy_keyboard)

        if self.match_command(self.t('DEAL_BUY_PREV')):
            self._prev_item(**kwargs)
        elif self.match_command(self.t('DEAL_BUY_NEW_SEARCH')):
            self.user.reset()
            self.user.save()
            self.text = self.t('DEAL_BUY')
            self._on_hook(kwargs)
        elif self.match_command(self.t('DEAL_BUY_NEXT')):
            self._next_item(**kwargs)

    def _show_item(self, **kwargs):
        if self.user.offset < 0:
            self.send(self.t('NO_PREV'))
            return False

        condition = Q(bc_hash__ne=None) & \
                    Q(type=self.user.filter_buy_type)
        # Q(price__lte=self.user.filter_price)

        offers = Offer.objects(condition) \
            .skip(self.user.offset) \
            .limit(1)

        offer = None
        for item in offers:
            offer = item
            break

        if offer is None:
            self.send(self.t('NO_MORE'))
            return False

        try:
            path = offer.get_image_path(self.user.lang)
            if not path:
                raise Exception
            with open(path, 'rb') as f:
                inline_keyboard = InlineKeyboard(keyboard=[
                    [InlineKeyboardButton(text=self.t('BUY_CONTRACT'), callback_data=offer.get_id())]
                ])
                self.send_photo(
                    files=(('photo', path, f.read()),),
                    reply_markup=inline_keyboard
                )
        except Exception:
            if options.debug:
                traceback.print_exc()
            self.logger.error(offer.get_id())
            self.send(self.t('IMAGE_NOT_FOUND'))

        return True

    def _prev_item(self, **kwargs):
        if self.user.offset >= 0:
            self.user.offset -= 1
        self._show_item(**kwargs)
        self.user.save()

    def _next_item(self, **kwargs):
        self.user.offset += 1
        result = self._show_item(**kwargs)
        if result:
            self.user.save()
        else:
            self.user.offset -= 1
