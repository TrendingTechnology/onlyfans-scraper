r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import httpx

from ..constants import (
    timelineEP, timelineNextEP,
    timelinePinnedEP,
    archivedEP, archivedNextEP
)


def scrape_pinned_posts(headers, model_id) -> list:
    with httpx.Client(http2=True, headers=headers) as c:
        r = c.get(timelinePinnedEP.format(model_id), timeout=None)
        if not r.is_error:
            return r.json()['list']
        r.raise_for_status()


def scrape_timeline_posts(headers, model_id, timestamp=0) -> list:
    ep = timelineNextEP if timestamp else timelineEP
    with httpx.Client(http2=True, headers=headers) as c:
        r = c.get(ep.format(model_id, timestamp), timeout=None)
        if not r.is_error:
            posts = r.json()['list']
            if not posts:
                return posts
            posts += scrape_timeline_posts(
                headers, model_id, posts[-1]['postedAtPrecise'])
            return posts
        r.raise_for_status()


def scrape_archived_posts(headers, model_id, timestamp=0) -> list:
    ep = archivedNextEP if timestamp else archivedEP
    with httpx.Client(http2=True, headers=headers) as c:
        r = c.get(ep.format(model_id, timestamp), timeout=None)
        if not r.is_error:
            posts = r.json()['list']
            if not posts:
                return posts
            posts += scrape_archived_posts(
                headers, model_id, posts[-1]['postedAtPrecise'])
            return posts
        r.raise_for_status()


def parse_posts(posts: list):
    media = [post['media'] for post in posts if post['media']]
    urls = [
        (i['info']['source']['source'], i['createdAt'], i['id']) for m in media for i in m if i['canView']]
    return urls
