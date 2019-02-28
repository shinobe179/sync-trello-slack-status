import json
import os

import requests

trello_username = os.environ['TRELLO_USERNAME']
list_name = os.environ['LIST_NAME']
ignore_flag = os.environ['IGNORE_FLAG']
slack_token = os.environ['SLACK_TOKEN']


def lambda_handler(*args):
    trello_task_count = get_trello_task_count(trello_username, list_name, ignore_mode=ignore_flag)
    change_slack_status(trello_task_count, slack_token)


def get_request_to_trello(path, fields=None):
    api_header = 'https://trello.com/1/'
    key = os.environ['TRELLO_KEY']
    token = os.environ['TRELLO_TOKEN']

    r = requests.get('{}{}?key={}&token={}&fields={}'.format(api_header, path, key, token, fields))
    return r


def search_list_id(list_name, trello_lists):
    list_id = ''
    for tl in trello_lists:
        if list_name in tl['name']:
            list_id = tl['id']
            break
    return list_id


def get_trello_task_count(username, list_name, ignore_mode='disable'):
    card_count = 0

    board_resp = get_request_to_trello('members/username/boards', fields='id')
    board_ids = [i['id'] for i in board_resp.json()]

    for bid in board_ids:
        list_resp = get_request_to_trello('boards/{}/lists'.format(bid), fields='id,name')
        trello_lists = list_resp.json()
        list_id = search_list_id(list_name, trello_lists)
        card_resp = get_request_to_trello('boards/{}/cards'.format(bid), fields='idList')
        cards = card_resp.json()
        if ignore_mode == "enable":
            card_count += (len(cards) - len([card for card in cards if card['idList'] == list_id]))
        elif ignore_mode == "disable":
            card_count += (len([card for card in cards if card['idList'] == list_id]))

    return card_count


def return_emoji(task_count):
    if 0 <= task_count < 10:
        status_emoji = ':laughing:'
    elif 10 <= task_count < 20:
        status_emoji = ':smiley:'
    elif 20 <= task_count < 30:
        status_emoji = ':neutral_face:'
    elif 30 <= task_count < 40:
        status_emoji = ':fearful:'
    elif 40 <= task_count:
        status_emoji = ':exploding_head:'
    else:
        status_emoji = ':drooling_face:'
    return status_emoji


def change_slack_status(task_count, token, status_expiration=0):
    status_text = 'tasks:' + str(task_count)
    status_emoji = return_emoji(task_count)

    headers_dict = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    data_dict = {
        'profile': {
            'status_text': status_text,
            'status_emoji': status_emoji,
            'status_expiration': status_expiration
            }
    }
    r = requests.post('https://slack.com/api/users.profile.set', headers=headers_dict, data=json.dumps(data_dict))
    return r.json()

