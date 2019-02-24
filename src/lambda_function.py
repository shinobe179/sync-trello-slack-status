import json
import os

import requests

trello_username = os.environ['TRELLO_USERNAME']
trello_key = os.environ['TRELLO_KEY']
trello_token = os.environ['TRELLO_TOKEN']
ignore_list_name = os.environ['IGNORE_LIST_NAME']
slack_token = os.environ['SLACK_TOKEN']


def lambda_handler(*args):
    trello_task_count = get_trello_task_count(trello_username, trello_key, trello_token, ignore_list_name)
    change_slack_status(trello_task_count, slack_token)

def get_trello_task_count(username, key, token, ignore_list_name=None):
    api_header = 'https://trello.com/1/'
    task_number = 0
    
    # ボードID一覧の取得
    r = requests.get(api_header + 'members/' + username + '/boards?key=' + key + '&token=' + token + '&fields=id')
    board_id_list = [i['id'] for i in r.json()]
    
    # リストID、カードID一覧の取得
    for bid in board_id_list:
        lr = requests.get(api_header + 'boards/' + bid + '/lists?key=' + key + '&token=' + token + '&fields=id,name')
        list_list = lr.json()
        ignore_list_id = ''
        for i in list_list:
            if 'Done' in i['name']:
                ignore_list_id =  i['id']
                break
        cr = requests.get(api_header + 'boards/' + bid + '/cards?key=' + key + '&token=' + token + '&fields=idList')
        card_list = cr.json()
        task_number += (len(cr.json()) - len([i for i in card_list if i['idList'] == ignore_list_id]))
    return task_number

def change_slack_status(task_count, token, status_expiration=0):
    status_text = 'tasks:' + str(task_count)

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

    headers_dict = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                   }
    data_dict = {'profile': 
                    {'status_text': status_text,
                     'status_emoji': status_emoji,
                     'status_expiration': status_expiration
                    }
                }
    r = requests.post('https://slack.com/api/users.profile.set', headers=headers_dict, data=json.dumps(data_dict))
    return r.json()
