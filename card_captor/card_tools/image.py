try:
    from PIL import Image
except ImportError:
    import Image
from io import BytesIO
from mtgsdk import Card
import numpy
import requests


def _get_cards_url(name):
    res = Card.where(name=name).all()
    if len(res) > 0:
        return res[0].image_url
    languages = ["Chinese Simplified", "Chinese Traditional", "French", "German", "Italian",
                 "Japanese", "Korean", "Portuguese (Brazil)", "Russian", "Spanish"]
    for lang in languages:
        res = Card.where(language=lang).where(name=name).all()
        if len(res) > 0:
            return res[0].image_url
    return None

def _download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def _pil_to_opencv(img):
    pil_image = img.convert('RGB')
    open_cv_image = numpy.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image

def get_card_image(name):
    url = _get_cards_url(name)
    img = _download_image(url)
    converted = _pil_to_opencv(img)
    return converted
