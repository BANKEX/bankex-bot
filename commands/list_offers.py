from models.user import User
from models.offer import Offer

for offer in Offer.objects:
    print(offer.get_id(),)