# -*- coding: utf-8 -*-
import json
import time
import re
import requests
import telegram
from sseclient import SSEClient as EventSource
from edit_stream_config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from dump_feature import get_all_feature
from xgb_inf import inference

bot = telegram.Bot(TELEGRAM_TOKEN)

STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
API = 'https://zh.wikipedia.org/w/api.php'

while True:
    try:
        for event in EventSource(STREAM_URL):
            if event.event == 'message':
                if len(event.data) == 0:
                    continue

                try:
                    change = json.loads(event.data)
                except json.decoder.JSONDecodeError:
                    print('JSONDecodeError:', event.data)
                    continue

                if not change['wiki'] == 'zhwiki':
                    continue
                if change['type'] not in ['edit', 'new']:
                    continue
                if not change['namespace'] == 0:
                    continue
                if change['bot']:
                    continue

                print(change['user'], change['title'], change['revision'])

                if change['type'] == 'new':
                    oldid = change['revision']['new']
                else:
                    oldid = change['revision']['old']

                payload = {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'revisions',
                    'titles': change['title'],
                    'utf8': 1,
                    'rvprop': 'content|ids',
                    'rvstartid': change['revision']['new'],
                    'rvendid': oldid
                }
                while True:
                    try:
                        res = requests.post(API, data=payload).json()
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(500)

                revisions = list(res['query']['pages'].values())[0]['revisions']

                if re.search(r'#(REDIRECT|重定向)', revisions[0]['*'], flags=re.I):
                    continue

                new_features = get_all_feature(revisions[0]['*'])
                new_level = inference(new_features)[0]

                print(revisions[0]['revid'], revisions[0]['*'][:100].replace('\n', ' '))
                if change['type'] == 'edit':
                    print(revisions[1]['revid'], revisions[1]['*'][:100].replace('\n', ' '))
                    old_features = get_all_feature(revisions[1]['*'])
                    old_level = inference(old_features)[0]

                message = ''
                if change['type'] == 'edit':
                    message = '修訂 <a href="https://zh.wikipedia.org/wiki/{0}">{0}</a> <a href="https://zh.wikipedia.org/wiki/Special:diff/{1}">{1}</a> 預測等級：{2}→{3}'.format(
                        change['title'], change['revision']['new'], old_level, new_level)
                elif change['type'] == 'new':
                    message = '新頁面 <a href="https://zh.wikipedia.org/wiki/{0}">{0}</a> 預測等級：{1}'.format(change['title'], new_level)
                print(message)

                # print(change)

                if message:
                    bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=message,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                print()

    except Exception as e:
        print(e)
        time.sleep(5000)
