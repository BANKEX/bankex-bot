# coding=utf-8
import traceback
from datetime import datetime

from pytz import timezone
from tornkts.base.mongodb import BaseDocument
from mongoengine import StringField, DateTimeField, IntField


class Text(BaseDocument):
    LANG_RU = 'ru'
    LANG_EN = 'en'

    lang = StringField(required=True, choices=(LANG_EN, LANG_RU))
    key = StringField(required=True)
    value = StringField(required=True)
    comment = StringField()

    update_date = DateTimeField()

    def save(self, *args, **kwargs):
        self.update_date = datetime.now(tz=timezone('UTC'))
        return super(Text, self).save(*args, **kwargs)

    def to_dict_impl(self, **kwargs):
        return {
            'id': self.get_id(),
            'lang': self.lang,
            'key': self.key,
            'value': self.value,
            'comment': self.comment,
            'update_date': self.update_date
        }

    @staticmethod
    def get(key, lang=LANG_EN):
        try:
            return Text.objects.get(key=key, lang=lang)
        except:
            return False

    @classmethod
    def format(cls, key, lang=LANG_EN, *args):
        try:
            text = Text.get(key, lang=lang)
            if not text:
                text = cls.defaults().get(key, 'Not found')
            else:
                text = text.value
            return text.format(*args)
        except:
            traceback.print_exc()
            return ''

    @staticmethod
    def defaults():
        return {
            'CHOOSE_LANG': 'Please choose your language',
            'WELCOME': """
Здравствуйте! Я - робот @BangBankBot!
Используя меня в своем смартфоне ты можешь найти, посмотреть или купить финансовый контракт.
Все сделки регистрируются на технологии блокчейн, новом финансовом интернете, поэтому ты можешь доверять мне.
Для начала выбери направление сделки:
""",
            'DEAL_SELL': 'Продать контракт',
            'DEAL_BUY': 'Найти и купить контракт',
            'DEAL_SELL_INTRO': """
Отлично! Для того чтобы продать контракт необходимо заполнить базовые данные о нем.
Выберите тип контракта:
            """,
            'SELL_CREDIT': 'Продать кредит',
            'SELL_FUTURES': 'Продать фьючерс',
            'SELL_FACTORING': 'Продать требования к оплате (факторинг)',

            'DEAL_BUY_INTRO': "Выбери тип финансового контракта",
            'BUY_CREDIT': 'Купить кредит',
            'BUY_FUTURES': 'Купить фьючерс',
            'BUY_FACTORING': 'Купить требования к оплате (факторинг)',
            'DEAL_BUY_CREDIT_PRICE': 'Введи сумму кредита к покупке',
            'DEAL_BUY_FUTURES_PRICE': 'Введи стоимость фьючерса',
            'DEAL_BUY_FACTORING_PRICE': 'Введи сумму требований к оплате',
            'DEAL_BUY_MANUAL': """
Отлично! Теперь @BankExBot будет тебе показывать предложения биржи.
Для просмотра нажимай кнопки вперед-назад, а когда ты найдешь нужный тебе оффер жми - BUY и ты сможешь оформить сделку )
""",

            'DEAL_BUY_UNDERSTAND_START': 'ОК, понял, начинаем поиск',
            'DEAL_BUY_PREV': 'Назад',
            'DEAL_BUY_NEW_SEARCH': 'Новый поиск',
            'DEAL_BUY_NEXT': 'Вперед',

            'CREDIT_ENTER_DESC': 'Введи описание своего кредита - короткий текст длиной не более 150 символов',
            'CREDIT_ENTER_ZIP': 'Введите ZIP код продавца заёма',
            'CREDIT_ENTER_REG_SERVICE': """
Введи место/службу регистрации действующего контракта (например - Landing Club)
""",
            'CREDIT_ENTER_LOAN_ID': 'Введи ID заемщика в службе регистрации (loanId)',
            'CREDIT_ENTER_LOAN_AMOUNT': 'Введи сумму займа по договору (loanAmount)',
            'CREDIT_ENTER_INTEREST_RATE': 'Введи процентную ставку по договору (interestRate)',
            'CREDIT_ENTER_LOAN_LENGTH': 'Введи полный срок займа в месяцах (loanLength)',
            'CREDIT_ENTER_LOAN_STATUS': 'Введи стадию погашения займа (loanStatus)',
            'LOAN_STATUS_EARLY': 'Early (366-1280 days)',
            'LOAN_STATUS_NORMAL': 'Normal (121-365 days)',
            'LOAN_STATUS_LATE': 'Late (31-120 days)',
            'CREDIT_ENTER_SELLERS_WARRANTY': 'Гарантии продавца на возврат в случае дефолта заемщика',
            'WARRANTY_FULL': 'Полная',
            'WARRANTY_PARTLY': 'Частичная',
            'WARRANTY_NONE': 'Нет',
            'CREDIT_ENTER_PRICE': 'Стоимость продажи?',
            'ENTER_NUMBER': 'Введите число',

            'FUTURES_ENTER_DESC': """
Введи наименование своего фьючерсного контракта - короткий текст длиной не более 150 символов
""",
            'FUTURES_ENTER_ZIP': 'Введите ZIP код продавца контракта',
            'FUTURES_ENTER_REG_SERVICE': """
Введи место/службу регистрации действующего контракта (например - NYMEX)
""",
            'FUTURES_ENTER_LOAN_ID': 'Введи ID действующего контракта в службе регистрации',
            'FUTURES_CHOOSE_CONTRACT_TYPE': 'Выбери тип контракта',
            'FUTURES_TYPE_SETTLEMENT': 'Расчетный',
            'FUTURES_TYPE_DELIVERABLE': 'Поставочный',
            'FUTURES_ENTER_CONTRACT_SIZE': 'Введи размер контракта - количество базового актива',
            'FUTURES_CONTRACT_MATURITY': 'Введи сроки обращения контракта',
            'FUTURES_ENTER_DELIVERY_DATE': 'Введи дату поставки',
            'FUTURES_ENTER_MIN_PRICE_DEVIATION': 'Введи минимальное изменение цены',
            'FUTURES_PRICE': 'Цена фьючерса?',

            'FACTORING_ENTER_DESC': """
Введи описание своих требований к олпате - короткий текст длиной не более 150 символов
""",
            'FACTORING_ENTER_ZIP': "Введите ZIP код поставщика",
            'FACTORING_ENTER_REG_SERVICE': """
Введи место/службу регистрации действующего контракта (например - Landing Club)
""",
            'FACTORING_ENTER_LOAN_ID': 'Введи ID действующего контракта в службе регистрации',
            'FACTORING_PAY_REQS': 'Выбери тип требований к оплате:',
            'FACTORING_REGRESS': 'Факторинг с регрессом',
            'FACTORING_NO_REGRESS': 'Факторинг без регресса',
            'FACTORING_TITLE_SUPPLIER': 'Введи название поставщика',
            'FACTORING_SUM_REQS': 'Сумма требований по счету',
            'FACTORING_DATE_REQS_PAY': 'Дата оплаты по требованию',
            'FACTORING_PRICE': 'Стоимость требования к оплате?',

            'SAIL_YOU_CREATE_CONTRACT': """
Отлично! Ты создал контракт.
Запись о твоем контракте будет записана в распределенный реестр блокчейн.
В блокчейн пишется не только история продавца, но и твоя, как покупателя.
Регистрируем тебя в блокчейн?"
""",
            'BUY_CONTRACT': 'Купить',
            'YES_APPROVE': u"Да, подтверждаю",
            'NO_FEAR': u"Нет, боюсь",
            'WHAT_IS_BLOCKCHAIN': u"Что такое блокчейн?",
            'FEAR_BLOCKCHAIN_WIKI': u"""
Ну что же, в первый раз всем страшно.
Почитай про блокчейн тут: https://ru.wikipedia.org/wiki/Цепочка_блоков_транзакций
""",
            'WHAT_IS_BLOCKCHAIN_WIKI': """
Ок, блокчейн - это цепочка блоков транзакций.
Все равно ничего не понял? Тогда читай тут: https://ru.wikipedia.org/wiki/Цепочка_блоков_транзакций
""",

            'GENERATE_PREVIEW_START': 'Генерирую пример карточки, которая будет показываться покупателям',
            'GENERATE_PREVIEW_END': 'Вот так покупатели увидят твое предложение',
            'GENERATE_PREVIEW_FAIL': 'Не удалось сгенерировать пример карточки, мы создадим её позднее',
            'REGISTER_BC_BEGIN': 'Регистрирую в реестре',
            'REGISTER_BC_END': """
Окей! Ты опубликовал свое предложение!
Когда покупатель заинтересуется твоим контрактом - к тебе прийдет уведомление в смартфон!
""",
            'THNX_UNDERSTAND': 'Спасибо, понял!',
            'CHOOSE_DIRECTION': 'Выберите направление сделки',
            'NO_MORE': 'Пока что нет больше предложений',
            'NO_PREV': 'Нет более ранних публикаций',
            'IMAGE_NOT_FOUND': 'Изображение лота не найдено',
            'ENTER_CORRECT_CONTRACT_TYPE': 'Введите корректный тип контракта',

            'BUY_YOU_CREATE_CONTRACT': """
Отлично! Ты выбрал оффер.
Исполнение твоей сделки гарантирует только история продавца, которая записана в распределенном реестре блокчейн.
В блокчейн пишется не только история продавца, но и твоя, как покупателя.
Регистрируем тебя в блокчейн?
""",
            'BEGIN_DEAL': """
Отлично! Теперь можно начинать сделку!
На смартфон продавца отправлено уведомление. Подожди подтверждения.
""",
            'TMPL_CREDIT_TITLE': 'Переуступка прав требований',
            'TMPL_ZIP': 'ZIP',
            'TMPL_SERVICE': 'Service',
            'TMPL_LOAN_ID': 'Loan ID',
            'TMPL_LOAN_AMOUNT': 'Loan Amount',
            'TMPL_INTEREST_RATE': 'Interest Rate',
            'TMPL_LOAN_LENGTH': 'Loan Length',
            'TMPL_LOAN_STATUS': 'Loan Status',
            'TMPL_SELLERS_GARANTY': 'Sellers Garanty',
            'TMPL_CREDIT_PRICE': 'PRICE',

            'TMPL_FUTURES_TITLE': 'Фьючерскный контракт',
            'TMPL_FUTURES_TYPE': 'Type',
            'TMPL_FUTURES_ASSET': 'Asset',
            'TMPL_FUTURES_TIMING': 'Timing',
            'TMPL_FUTURES_DELIVERY_DATE': 'Delivery date',
            'TMPL_FUTURES_MIN_PRICE_CHANGE': 'Min price change',
            'TMPL_FUTURES_FUTURES_ID': 'Futures ID',
            'TMPL_FUTURES_PRICE': 'Futures price',

            'TMPL_FACTORING_TITLE': 'Payable (factoring)',
            'TMPL_FACTORING_ZIP': 'ZIP',
            'TMPL_FACTORING_SERVICE': 'Service',
            'TMPL_FACTORING_FACTORING_ID': 'Factoring ID',
            'TMPL_FACTORING_FACTORING_TYPE': 'Factoring type',
            'TMPL_FACTORING_PROVIDER': 'Provider',
            'TMPL_FACTORING_AMOUNT': 'Amount',
            'TMPL_FACTORING_DATE_OF_PAYMENT': 'Date of payment',
            'TMPL_FACTORING_PRICE': 'Price',
        }
