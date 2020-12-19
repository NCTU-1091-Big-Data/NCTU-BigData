# -*- coding: utf-8 -*-
import json
import requests
import telegram
from sseclient import SSEClient as EventSource
from edit_stream_config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN

bot = telegram.Bot(TELEGRAM_TOKEN)

STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
API = 'https://zh.wikipedia.org/w/api.php'

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
        res = requests.post(API, data=payload).json()
        revisions = list(res['query']['pages'].values())[0]['revisions']

        print(revisions[0]['revid'], revisions[0]['*'][:100].replace('\n', ' '))
        if change['type'] == 'edit':
            print(revisions[1]['revid'], revisions[1]['*'][:100].replace('\n', ' '))

        message = ''
        if change['type'] == 'edit':
            message = '修訂 <a href="https://zh.wikipedia.org/wiki/{0}">{0}</a> <a href="https://zh.wikipedia.org/wiki/Special:diff/{1}">{1}</a>'.format(change['title'], change['revision']['new'])
        elif change['type'] == 'new':
            message = '新頁面 <a href="https://zh.wikipedia.org/wiki/{0}">{0}</a>'.format(change['title'])
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
