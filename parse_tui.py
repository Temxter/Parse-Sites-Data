from parse_utils import *
import os

URL_TUI_PATTERN_CITY_ID = 'https://apigate.tui.ru/api/office/list?cityId={}&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
FILENAME_SAVE_TUI = 'tui.json'

CORRECT_CITY_IDS = [1, 2, 16, 17, 18, 19, 20, 25, 32, 33, 41, 42, 46, 48, 50, 88, 107, 111, 113, 114, 119, 123, 127,
                    129, 133, 135, 139, 140, 143, 147, 151, 158, 164, 169, 172, 174, 183, 186, 187, 191, 192, 198, 201,
                    211, 229, 235, 236, 289, 310, 327, 328, 332, 334, 347, 351, 354, 356, 362, 363, 364, 367, 368, 370,
                    378, 381, 382, 383, 385, 388, 389, 391, 393, 394, 398, 399, 400, 401, 404, 405, 406, 408, 413, 414,
                    415, 419, 422, 424, 425, 431, 433, 437, 438, 442, 453, 455]
# CORRECT_CITY_IDS = define_right_city_ids(URL_TUI_PATTERN_CITY_ID, from_id=1, to_id=1000, sleep=0)

if __name__ == '__main__':
    filename_save = FILENAME_SAVE_TUI
    print(f'Script start parse {URL_TUI_PATTERN_CITY_ID}')

    error_city_id = []
    parsed_entities = []

    for city_id in CORRECT_CITY_IDS:
        url = URL_TUI_PATTERN_CITY_ID.format(city_id)
        parsed_entities.extend(parse(url, parse_tui))
        if len(parsed_entities) > 0:
            print(f'parse city id = {city_id}, total amount of offices = {len(parsed_entities)},'
                  f' address_example: {parsed_entities[0]["address"]}')
            save_to_json(parsed_entities, filename_save)
        else:
            error_city_id.append(city_id)

    if error_city_id:
        print(f'Amount of errors = {len(error_city_id)}. Errors city id = {", ".join(map(str, error_city_id))}')
    print(f'Records saved to "{filename_save}". Amount of parsed records = {len(parsed_entities)}.')
