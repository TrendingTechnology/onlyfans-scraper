r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import asyncio
import pathlib
import platform

import httpx
from tqdm.asyncio import tqdm
try:
    from win32_setctime import setctime  # pylint: disable=import-error
except ModuleNotFoundError:
    pass

from .auth import read_auth
from .dates import convert_date_to_timestamp
from .separate import separate_by_id
from ..db import operations


async def process_urls(headers, username, model_id, urls):
    if urls:
        operations.create_database(model_id)
        media_ids = operations.get_media_ids(model_id)
        separated_urls = separate_by_id(urls, media_ids)

        path = pathlib.Path.cwd() / username
        path.mkdir(exist_ok=True)

        # Added pool limit:
        limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
        async with httpx.AsyncClient(headers=headers, limits=limits) as c:
            aws = [asyncio.create_task(
                download(c, path, model_id, *url)) for url in separated_urls]

            with tqdm(desc='Files downloaded', total=len(aws), colour='cyan', leave=True) as bar:
                for coro in asyncio.as_completed(aws):
                    await coro
                    bar.update()


async def download(client, path, model_id, url, date=None, id_=None):
    filename = url.split('?', 1)[0].rsplit('/', 1)[-1]
    path_to_file = path / filename

    async with client.stream('GET', url) as r:
        if not r.is_error:
            total = int(r.headers['Content-Length'])
            with tqdm(desc=filename, total=total, unit_scale=True, unit_divisor=1024, unit='B', leave=False) as bar:
                num_bytes_downloaded = r.num_bytes_downloaded
                with open(path_to_file, 'wb') as f:
                    async for chunk in r.aiter_bytes(chunk_size=1024):
                        f.write(chunk)
                        bar.update(
                            r.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = r.num_bytes_downloaded

        else:
            r.raise_for_status()

    if path_to_file.is_file():
        if date:
            set_time(path_to_file, convert_date_to_timestamp(date))

        if id_:
            data = (id_, filename)
            operations.write_from_data(data, model_id)


def set_time(path, timestamp):
    if platform.system() == 'Windows':
        setctime(path, timestamp)
    pathlib.os.utime(path, (timestamp, timestamp))
