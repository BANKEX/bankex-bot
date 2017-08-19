from raven.contrib.tornado import AsyncSentryClient

from handlers.screenshot_handler import ScreenshotHandler
from tornado.ioloop import IOLoop
from settings import options
from tornado.web import Application
from tornkts.handlers import DefaultHandler
from mongoengine import connection as mongo_connection


class Server(Application):
    def __init__(self):
        handlers = [
            (r"/screenshot.(.*)", ScreenshotHandler),
        ]
        settings = {
            'compress_response': False,
            'default_handler_class': DefaultHandler,
            'debug': options.debug
        }
        super(Server, self).__init__(handlers, **settings)


def run_server():
    mongo_connection.connect(host=options.mongo_uri)

    server = Server()
    server.listen(options.port, options.host)
    server.sentry_client = AsyncSentryClient(
        'https://f1dc8b4909ce4d41b1bb2da4d92cb4dc:1ceefc0a0a91419da95f2abbf99f7f51@sentry.team.ktsstudio.ru/6'
    )
    IOLoop.instance().start()


if __name__ == "__main__":
    run_server()
