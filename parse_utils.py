import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    response = requests.get(url=url, headers=HEADERS, params=params)
    return response


def parse_mebelshara(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')
    entities = soup.find_all('div', class_='shop-list-item')
    entities_parsed = []
    for entity in entities:
        entities_parsed.append({
            'address': entity.find_previous('h4', class_='js-city-name').get_text() + ', ' + entity['data-shop-address'],
            'latlon': [entity['data-shop-latitude'], entity['data-shop-longitude']],
            'name': entity['data-shop-name'],
            'phones': [entity['data-shop-phone']],
            'working_hours': [entity['data-shop-mode1'], entity['data-shop-mode2']]
        })
    return entities_parsed


def parse_tui(html_text):
    entity_list = json.loads(html_text)['offices']
    entities_parsed = []
    for entity in entity_list:
        try:
            working_hours = []
            hours_of_operation = entity['hoursOfOperation']
            set_days(hours_of_operation['workdays'], 'пн - пт', working_hours)
            set_days(hours_of_operation["saturday"], 'сб', working_hours)
            set_days(hours_of_operation["sunday"], 'вс', working_hours)
            entities_parsed.append({
                'address': entity['address'],
                'latlon': [entity['latitude'], entity['longitude']],
                'name': entity['name'],
                'phones': [phone.strip() for phone in entity['phone'].split(';')] if 'phone' in entity else [],
                'working_hours': working_hours,
            })
        except KeyError as err:
            print(f'KeyError except: {err} on entity {entity}')
    return entities_parsed


def set_days(days, days_str, working_hours_list):
    if not days['isDayOff']:
        working_hours_list.append(f'{days_str} {days["startStr"]} - {days["endStr"]}')


def parse(url, parse_function):
    response = get_html(url)
    if response.status_code == 200:
        parsed_entities = parse_function(response.text)
        return parsed_entities
    else:
        print(f'Error: response code = {response.status_code}')
        return []


def save_to_json(data, filename='data.json', mode='w'):
    with open(filename, mode, encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
