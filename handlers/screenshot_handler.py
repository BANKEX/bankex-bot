from io import BytesIO
from PIL import Image
from base.base_handler import TemplateMixin, BankExBaseHandler
from base.base_server_error import BankExServerError
from models.content import Text
from models.user import User
from models.offer import Offer
from settings import options
import utils


class ScreenshotHandler(TemplateMixin, BankExBaseHandler):
    @property
    def get_methods(self):
        result = {
            'image': self.image,
            'html': self.html,
        }
        if options.disable_render_img:
            del result['image']
        return result

    def image(self):
        try:
            offer = Offer.objects.get(id=self.get_mongo_id_argument('id'))
        except Offer.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND)

        with utils.phantom() as driver:
            url = utils.get_screenshot_html_url(
                offer.get_id(),
                self.get_str_argument('lang', default=Text.LANG_RU)
            )

            driver.set_window_size(1280, 720)
            driver.get(url)

            elem = driver.find_element_by_id('container')
            location = elem.location
            size = elem.size
            screenshot = driver.get_screenshot_as_png()

        im = Image.open(BytesIO(screenshot))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))

        img_string = BytesIO()
        im.save(img_string, format="png")

        self.set_header("Content-Type", "image/png")
        self.write(img_string.getvalue(), nocontenttype=True)

    def html(self):
        try:
            offer = Offer.objects.get(id=self.get_mongo_id_argument('id'))
        except Offer.DoesNotExist:
            raise BankExServerError(BankExServerError.NOT_FOUND)

        template_name = None

        if offer.type == Offer.TYPE_CREDIT:
            template_name = 'credit.html'
        elif offer.type == Offer.TYPE_FUTURES:
            template_name = 'futures.html'
        elif offer.type == Offer.TYPE_FACTORING:
            template_name = 'factoring.html'

        if template_name is not None:
            self.render(template_name, {
                'offer': offer,
                'Text': Text,
                'lang': self.get_str_argument('lang', default=Text.LANG_RU)
            })
        else:
            raise BankExServerError(BankExServerError.BAD_REQUEST)
