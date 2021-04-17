r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

import argparse
import asyncio

from .api import highlights, me, messages, posts, profile, subscriptions
from .db import operations
from .interaction import like
from .utils import auth, download, prompts

from revolution import Revolution


@Revolution(desc='Getting messages...')
def process_messages(headers, model_id):
    messages_ = messages.scrape_messages(headers, model_id)

    if messages_:
        messages_urls = messages.parse_messages(messages_, model_id)
        return messages_urls
    return []


@Revolution(desc='Getting highlights...')
def process_highlights(headers, model_id):
    highlights_, stories = highlights.scrape_highlights(headers, model_id)

    if highlights_ or stories:
        highlights_ids = highlights.parse_highlights(highlights_)
        stories += asyncio.run(
            highlights.process_highlights_ids(headers, highlights_ids))
        stories_urls = highlights.parse_stories(stories)
        return stories_urls
    return []


@Revolution(desc='Getting archived media...')
def process_archived_posts(headers, model_id):
    archived_posts = posts.scrape_archived_posts(headers, model_id)

    if archived_posts:
        archived_posts_urls = posts.parse_posts(archived_posts)
        return archived_posts_urls
    return []


@Revolution(desc='Getting timeline media...')
def process_timeline_posts(headers, model_id):
    timeline_posts = posts.scrape_timeline_posts(headers, model_id)

    if timeline_posts:
        timeline_posts_urls = posts.parse_posts(timeline_posts)
        return timeline_posts_urls
    return []


@Revolution(desc='Getting pinned media...')
def process_pinned_posts(headers, model_id):
    pinned_posts = posts.scrape_pinned_posts(headers, model_id)

    if pinned_posts:
        pinned_posts_urls = posts.parse_posts(pinned_posts)
        return pinned_posts_urls
    return []


def process_profile(headers, username) -> list:
    user_profile = profile.scrape_profile(headers, username)
    urls, info = profile.parse_profile(user_profile)
    profile.print_profile_info(info)
    return urls


def do_download_content(headers, username, model_id):
    profile_urls = process_profile(headers, username)
    pinned_posts_urls = process_pinned_posts(headers, model_id)
    timeline_posts_urls = process_timeline_posts(headers, model_id)
    archived_posts_urls = process_archived_posts(headers, model_id)
    highlights_urls = process_highlights(headers, model_id)
    messages_urls = process_messages(headers, model_id)

    asyncio.run(download.process_urls(
        headers,
        username,
        model_id,
        profile_urls + pinned_posts_urls + timeline_posts_urls
        + archived_posts_urls + highlights_urls + messages_urls))


def do_database_migration(path, model_id):
    results = operations.read_foreign_database(path)
    operations.write_from_foreign_database(results, model_id)


def get_model(headers, subscribe_count) -> tuple:
    """
    Gets user's subscriptions and then prints them to the console. Accepts input
    from user corresponding to the model whose content they would like to scrape.
    """

    with Revolution(desc='Getting your subscriptions (this may take awhile)...') as _:
        list_subscriptions = asyncio.run(
            subscriptions.get_subscriptions(headers, subscribe_count))
        parsed_subscriptions = subscriptions.parse_subscriptions(
            list_subscriptions)
    subscriptions.print_subscriptions(parsed_subscriptions)

    print('\nEnter the number next to the user whose content you would like to download:')
    while True:
        try:
            num = int(input('> '))
            return parsed_subscriptions[num - 1]
        except ValueError:
            print("Incorrect value. Please enter an actual number.")
        except IndexError:
            print("Value out of range. Please pick a number that's in range")


def process_me(headers):
    my_profile = me.scrape_user(headers)
    name, username, subscribe_count = me.parse_user(my_profile)
    me.print_user(name, username)
    return subscribe_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--edit', help='view or edit your current auth', action='store_true')
    parser.add_argument(
        '-u', '--username', help='scrape the content of a user', action='store_true')
    args = parser.parse_args()
    if args.edit:
        pass
    if args.username:
        pass

    headers = auth.make_headers(auth.read_auth())

    main_prompt_result = prompts.main_prompt()

    if not main_prompt_result:
        # Download content from user
        username_or_list_prompt_result = prompts.username_or_list_prompt()

        if username_or_list_prompt_result:
            subscribe_count = process_me(headers)
            username, model_id, *_ = get_model(headers, subscribe_count)

        else:
            username = prompts.username_prompt()
            model_id = profile.get_id(headers, username)

        do_download_content(headers, username, model_id)

    elif main_prompt_result == 1:
        # Like a user's posts
        username = prompts.username_prompt()
        model_id = profile.get_id(headers, username)

        posts = like.get_posts(headers, model_id)
        unfavorited_posts = like.filter_for_unfavorited(posts)
        post_ids = like.get_post_ids(unfavorited_posts)
        like.like(headers, model_id, username, post_ids)

    elif main_prompt_result == 2:
        # Unlike a user's posts
        username = prompts.username_prompt()
        model_id = profile.get_id(headers, username)

        posts = like.get_posts(headers, model_id)
        favorited_posts = like.filter_for_favorited(posts)
        post_ids = like.get_post_ids(favorited_posts)
        like.unlike(headers, model_id, username, post_ids)

    elif main_prompt_result == 3:
        # Migrate from old database
        path, username = prompts.database_prompt()
        model_id = profile.get_id(headers, username)
        do_database_migration(path, model_id)


if __name__ == '__main__':
    main()
