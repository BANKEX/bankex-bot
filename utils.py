import os
from contextlib import contextmanager
from datetime import datetime
import mimetypes
import signal
from tornkts import utils
from settings import options
import hashlib
from selenium import webdriver


def mkdir(path):
    utils.mkdir(path)


def gen_path():
    hash = hashlib.md5(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').encode('utf-8')).hexdigest()
    result = {
        'folder': '%s/%s/%s' % (options.upload_path, hash[0:2], hash[2:4]),
        'filename': hash + '.png'
    }
    result.update({
        'fullname': '%s/%s' % (result.get('folder'), result.get('filename')),
        'relname': '%s/%s/%s.png' % (hash[0:2], hash[2:4], hash)
    })
    return result


@contextmanager
def phantom(
        service_log_path=os.path.devnull,
        executable_path=options.phantom_path,
        service_args=("--ssl-protocol=tlsv1", "--ignore-ssl-errors=yes")
):
    driver = webdriver.PhantomJS(
        executable_path=executable_path,
        service_args=list(service_args),
        service_log_path=service_log_path
    )

    yield driver

    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()


rrb_html = 0
rrb_img = 0


def get_screenshot_html_url(id, lang):
    global rrb_html
    rrb_html = (rrb_html + 1) % len(options.renderer_html)
    return '{0}/screenshot.html?id={1}&lang={2}'.format(options.renderer_html[rrb_html], id, lang)


def get_screenshot_img_url(id, lang):
    global rrb_img
    rrb_img = (rrb_img + 1) % len(options.renderer_img)
    return '{0}/screenshot.image?id={1}&lang={2}'.format(options.renderer_img[rrb_img], id, lang)