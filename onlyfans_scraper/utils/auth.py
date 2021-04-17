r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import json
import pathlib

from .prompts import auth_prompt, ask_make_auth_prompt
from ..constants import configPath, authFile


def read_auth():
    p = pathlib.Path.home() / configPath
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            with open(p / authFile, 'r') as f:
                auth = json.load(f)
            break
        except FileNotFoundError:
            print(
                "You don't seem to have an `auth.json` file. Please fill the following out:")
            make_auth(p)
    return auth


def edit_auth():
    p = pathlib.Path.home() / configPath
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)

    try:
        with open(p / authFile, 'r') as f:
            auth = json.load(f)
        make_auth(p, auth)
    except FileNotFoundError:
        if ask_make_auth_prompt():
            make_auth(p)


def make_auth(path, auth=None):
    if not auth:
        auth = {
            'auth': {
                'app-token': '33d57ade8c02dbc5a333db99ff9ae26a',
                'sess': '',
                'auth_id': '',
                'auth_uid_': '',
                'user_agent': ''
            }
        }

    auth['auth'].update(auth_prompt(auth['auth']))

    with open(path / authFile, 'w') as f:
        f.write(json.dumps(auth, indent=4))


def make_headers(auth):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'app-token': auth['auth']['app-token'],
        'cookie': parse_cookies({
            'sess': auth['auth']['sess'],
            'auth_id': auth['auth']['auth_id'],
            'auth_uid_': auth['auth']['auth_uid_']
        }),
        'user-agent': auth['auth']['user_agent']
    }
    return headers


def parse_cookies(cookies: dict) -> str:
    two_fa = 'auth_uid_'
    auth_uid_ = cookies[two_fa]

    del cookies[two_fa]
    if auth_uid_:
        cookies[two_fa + cookies['auth_id']] = auth_uid_

    cookie_strs = ['{}={}'.format(k, v) for k, v in cookies.items()]
    cookie = '; '.join(cookie_strs)
    return cookie
