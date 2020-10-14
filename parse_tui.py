from parse_utils import *
import os


URL_TUI = 'https://apigate.tui.ru/api/office/list?cityId={}&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
FILENAME_SAVE_TUI = 'tui.json'


if __name__ == '__main__':
    filename_save = FILENAME_SAVE_TUI
    print(f'Script start parse {URL_TUI}')

    if os.path.exists(filename_save):
        os.remove(filename_save)

    records_counter = 0
    error_city_id = []
    for city_id in range(1, 500):
        url = URL_TUI.format(city_id)
        parsed_entities = parse(url, parse_tui)
        if len(parsed_entities) > 0:
            print(f'parse city id = {city_id}, amount of offices = {len(parsed_entities)},'
                  f' address_example: {parsed_entities[0]["address"]}')
            save_to_json(parsed_entities, filename_save, mode='a')
            records_counter += len(parsed_entities)
        else:
            error_city_id.append(city_id)
    print(f'Amount of errors = {len(error_city_id)}. Errors city id = {"".join(map(str,error_city_id))}')
    print(f'Records saved to "{filename_save}". Amount of parsed records = {error_city_id}.')
