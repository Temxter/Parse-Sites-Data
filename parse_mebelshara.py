from parse_utils import *


URL_MEBELSHARA = 'https://www.mebelshara.ru/contacts'
FILENAME_SAVE_MEBELSHARA = 'mebelshara.json'


if __name__ == '__main__':
    url, filename_save = URL_MEBELSHARA, FILENAME_SAVE_MEBELSHARA
    print(f'Script start parse {url}')
    parsed_entities = parse(url, parse_mebelshara)
    save_to_json(parsed_entities, filename_save)
    print(f'Records saved to "{filename_save}". Amount of parsed records = {len(parsed_entities)}.')
