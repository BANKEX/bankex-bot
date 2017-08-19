from tornado.httpclient import HTTPClient

from models.user import User
from models.offer import Offer
import sys

if len(sys.argv) < 3:
    raise Exception('Enter MongoId')

offer = Offer.objects.get(id=sys.argv[2])

offer.generate_img(sync=True)
offer.save(validate=False)