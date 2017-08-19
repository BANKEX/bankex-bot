# coding=utf-8
from tornado.options import define, options
import os

from roboman.bot import BaseBot

__author__ = 'grigory51'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_config(path):
    try:
        options.parse_config_file(path=path, final=False)
    except IOError:
        print('[WARNING] File no readable, run with default settings')


define('debug', type=bool, group='common', default=False, help='Tornado debug mode')
define('runtime', type=str, group='common', help='Data dir', default=CURRENT_DIR + '/runtime/')
define('static_root', type=str, group='common', help='Data dir', default=CURRENT_DIR + '/admin/')
define('session_path', type=str, group='common', default=CURRENT_DIR + '/runtime/sessions/')
define('upload_path', type=str, group='common', default=CURRENT_DIR + '/uploads/')
define('phantom_path', type=str, group='common', default='/usr/local/bin/phantomjs')

define('renderer_img', type=list, group='phantom', help='render_urls', default=[
    'http://127.0.0.1:8010'
])
define('renderer_html', type=list, group='phantom', help='render_urls', default=[
    'http://127.0.0.1:8009',
    'http://127.0.0.1:8009',
    'http://127.0.0.1:8009',
    'http://127.0.0.1:8009',
])
define('disable_render_img', type=bool, default=False)

define('host', type=str, group='server', default='127.0.0.1', help='Listen host')
define('port', type=int, group='server', default=8080, help='Listen port')
define('server_name', type=str, group='server', default='<SERVER_NAME>')
define('server_schema', type=str, group='server', default='http')
define('blockchain_server', type=str, group='server', default='http://<BLOCKCHAIN_SERVER_IP>:<BLOCKCHAIN_SERVER_PORT>')

define('mongo_uri', type=str, group='DB',
       default='mongodb://127.0.0.1:27017/<MONGO_DB_NAME>?connectTimeoutMS=1000&socketTimeoutMS=1000', help='Connection URI')

define('mode', type=str, group='Bots', default=BaseBot.MODE_GET_UPDATES)
define('update_interval', type=int, group='Bots', default=1000)
define('key_bank_ex_customer', type=str, group='Bots', default='<API_KEY>')

define('config', type=str, help='Path to config file', callback=parse_config)
if os.getenv('CONF'):
    parse_config(os.getenv('CONF'))

options.parse_command_line(final=True)
