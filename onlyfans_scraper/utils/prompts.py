r"""
               _          __                                                                      
  ___   _ __  | | _   _  / _|  __ _  _ __   ___         ___   ___  _ __   __ _  _ __    ___  _ __ 
 / _ \ | '_ \ | || | | || |_  / _` || '_ \ / __| _____ / __| / __|| '__| / _` || '_ \  / _ \| '__|
| (_) || | | || || |_| ||  _|| (_| || | | |\__ \|_____|\__ \| (__ | |   | (_| || |_) ||  __/| |   
 \___/ |_| |_||_| \__, ||_|   \__,_||_| |_||___/       |___/ \___||_|    \__,_|| .__/  \___||_|   
                  |___/                                                        |_|                
"""

from PyInquirer import prompt, Separator

from ..constants import mainPromptChoices, usernameOrListChoices


def main_prompt() -> int:
    main_prompt_choices = [*mainPromptChoices]
    main_prompt_choices.insert(3, Separator())

    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What would you like to do?',
            'choices': [*main_prompt_choices]
        }
    ]

    answer = prompt(questions)
    return mainPromptChoices[answer['action']]


def username_or_list_prompt() -> bool:
    questions = [
        {
            'type': 'list',
            'name': 'username_or_list',
            'message': 'Would you like a list of your subscriptions printed or would you like to enter a username?',
            'choices': [*usernameOrListChoices]
        }
    ]

    answer = prompt(questions)
    return usernameOrListChoices[answer['username_or_list']]


def username_prompt() -> str:
    questions = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter a model\'s username:'
        }
    ]

    answer = prompt(questions)
    return answer['username']


def database_prompt() -> tuple:
    questions = [
        {
            'type': 'input',
            'name': 'path',
            'message': 'Enter the path to the directory that contains your database files:'
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter that model\'s username:'
        }
    ]

    answers = prompt(questions)
    return (answers['path'], answers['username'])


def auth_prompt(auth) -> dict:
    questions = [
        {
            'type': 'input',
            'name': 'app-token',
            'message': 'Enter your `app-token` value:',
            'default': auth['app-token']
        },
        {
            'type': 'input',
            'name': 'sess',
            'message': 'Enter your `sess` cookie:',
            'default': auth['sess']
        },
        {
            'type': 'input',
            'name': 'auth_id',
            'message': 'Enter your `auth_id` cookie:',
            'default': auth['auth_id']
        },
        {
            'type': 'input',
            'name': 'auth_uid_',
            'message': 'Enter your `auth_uid_` cookie (leave blank if you don\'t use 2FA):',
            'default': auth['auth_uid_']
        },
        {
            'type': 'input',
            'name': 'user_agent',
            'message': 'Enter your `user agent`:',
            'default': auth['user_agent']
        }
    ]

    answers = prompt(questions)
    return answers


def ask_make_auth_prompt() -> bool:
    questions = [
        {
            'type': 'confirm',
            'name': 'make_auth',
            'message': "It doesn't seem you have an `auth.json` file. Would you like to make one?",
        }
    ]

    answer = prompt(questions)
    return answer['make_auth']
