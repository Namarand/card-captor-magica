try:
    from PIL import Image
except ImportError:
    import Image
from mtgsdk import Card
import difflib
import pytesseract

def identify_card(image_path, database):
    ocr_result = _detect_characters(image_path)
    closest = database.find_closest(ocr_result)
    return closest

def _detect_characters(image_path):
    return pytesseract.image_to_string(Image.open(image_path), lang='fra')

def _fetch_extension(extensions_id):
    return Card.where(set=extensions_id).all()

def _create_card_database(extensions_id, languages):
    database = []
    for extension in extensions_id:
        cards = _fetch_extension(extension)
        database += get_cards_name(cards, languages)
    return database

def _get_cards_name(cards, languages):
    results = []
    for card in cards:
        if "English" in languages:
            results += [card.name]
        else:
            for foreign_card in card.foreign_names:
                if foreign_card["language"] in languages:
                    results += [foreign_card["name"]]
    return results
