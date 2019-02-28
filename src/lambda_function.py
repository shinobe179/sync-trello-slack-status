import json
import os

import requests

trello_username = os.environ['TRELLO_USERNAME']
ignore_list_name = os.environ['IGNORE_LIST_NAME']
slack_token = os.environ['SLACK_TOKEN']


def lambda_handler(*args):
    trello_task_count = get_trello_task_count(trello_username, ignore_list_name)
    change_slack_status(trello_task_count, slack_token)


def get_request_to_trello(path, fields=None):
    api_header = 'https://trello.com/1/'
    key = os.environ['TRELLO_KEY']
    token = os.environ['TRELLO_TOKEN']

    r = requests.get('{}{}?key={}&token={}&fields={}'.format(api_header, path, key, token, fields))
    return r


def get_trello_task_count(username, ignore_list_name=None):
    task_count = 0

    # ボードID一覧の取得
    board_resp = get_request_to_trello('members/username/boards', fields='id')
    board_ids = [i['id'] for i in board_resp.json()]

    # リストID、カードID一覧の取得
    for bid in board_ids:
        list_resp = get_request_to_trello('boards/{}/lists'.format(bid), fields='id,name')
        lists = list_resp.json()
        ignore_list_id = ''
        for i in lists:
            if 'Done' in i['name']:
                ignore_list_id = i['id']
                break
        card_resp = get_request_to_trello('boards/{}/cards'.format(bid), fields='idList')
        cards = card_resp.json()
        task_count += (len(cards) - len([i for i in cards if i['idList'] == ignore_list_id]))
    return task_count


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