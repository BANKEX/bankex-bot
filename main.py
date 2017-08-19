from raven.contrib.tornado import AsyncSentryClient
from handlers.admin_handler import AdminHandler
from handlers.deals_handler import DealsHandler
from handlers.offers_handler import OffersHandler
from handlers.texts_handler import TextsHandler
from os import path
from handlers.index_handler import IndexHandler
from mongoengine import connection as mongo_connection

from handlers.users_handler import UsersHandler
from roboman.server import RobomanServer
from settings import options
from bots.bankex import BankExBot
from tornado.web import StaticFileHandler

if __name__ == "__main__":
    bots = [
        BankExBot,
    ]

    handlers = [
        (r'/api/(logout)', AdminHandler),
        (r'/api/admin.(.*)', AdminHandler),
        (r'/api/texts.(.*)', TextsHandler),
        (r'/api/users.(.*)', UsersHandler),
        (r'/api/offers.(.*)', OffersHandler),
        (r'/api/deals.(.*)', DealsHandler),

        (r'/static/(.*)', StaticFileHandler, dict(path=path.join(options.static_root, 'static'))),
        (r'/(.*)', IndexHandler),
    ]

    settings = {
        'host': options.host,
        'port': options.port,
        'debug': options.debug,
        'session': {
            'driver': 'file',
            'driver_settings': {
                'host': options.session_path
            },
            'cookie_config': {
                'expires_days': 365
            },
            'force_persistence': True,
            'cache_driver': True
        }
    }

    mongo_connection.connect(host=options.mongo_uri)
    server = RobomanServer(bots=bots, mode=options.mode, handlers=handlers, settings=settings)
    server.sentry_client = AsyncSentryClient(
        'https://f1dc8b4909ce4d41b1bb2da4d92cb4dc:1ceefc0a0a91419da95f2abbf99f7f51@sentry.team.ktsstudio.ru/6'
    )
    server.start()
