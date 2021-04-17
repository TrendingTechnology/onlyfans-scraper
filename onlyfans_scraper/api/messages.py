r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import httpx

from ..constants import messagesEP, messagesNextEP


def scrape_messages(headers, user_id, message_id=0) -> list:
    ep = messagesNextEP if message_id else messagesEP
    with httpx.Client(http2=True, headers=headers) as c:
        r = c.get(ep.format(user_id, message_id), timeout=None)
        if not r.is_error:
            messages = r.json()['list']
            if not messages:
                return messages
            messages += scrape_messages(headers, user_id, messages[-1]['id'])
            return messages
        r.raise_for_status()


def parse_messages(messages: list, user_id):
    messages_with_media = [(message['media'], message['createdAt'])
                           for message in messages if message['fromUser']['id'] == user_id and message['media']]

    messages_urls = []
    for message in messages_with_media:
        media, date = message
        for m in media:
            if m['canView']:
                messages_urls.append((m['src'], date, m['id']))
    return messages_urls
