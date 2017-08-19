#!/usr/bin/env python

import sys
from tornkts.manage import Manage
from mongoengine import connection as mongo_connection
from settings import options

mongo_connection.connect(host=options.mongo_uri)

manage = Manage()
try:
    manage.run(sys.argv[1])
except IndexError:
    manage.help()