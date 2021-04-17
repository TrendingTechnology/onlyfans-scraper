<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/icon.png" width="100" align="right">

# onlyfans-scraper

A command-line program to download media, like posts, and more from creators on OnlyFans.

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/example.png" width="550">

## Installation

You can install this program by entering the following in your console:

```
pip install onlyfans-scraper
```

## Setup

Before you can fully use it, you need to fill out some fields in a `auth.json` file. This file will be created for you when you run the program for the first time.

These are the fields:

```json
{
    "auth": {
        "app-token": "33d57ade8c02dbc5a333db99ff9ae26a",
        "sess": "",
        "auth_id": "",
        "auth_uniq_": "",
        "user_agent": ""
    }
}
```

It's really not that bad. I'll show you in the next sections how to get these bits of info.


### Step One: Creating the 'auth.json' File

You first need to run the program in order for the `auth.json` file to be created. To run it, simply type `onlyfans-dl` in your terminal and hit enter. Because you don't have an `auth.json` file, the program will create one for you and then ask you to enter some information. Now we need to get that information.


### Step Two: Getting Your Auth Info

***If you've already used DIGITALCRIMINAL's OnlyFans script, you can simply copy and paste the auth information from there to here.***

Go to your [notification area](https://onlyfans.com/my/notifications) on OnlyFans. Once you're there, open your browser's developer tools. If you don't know how to do that, consult the following chart:

| Operating System | Keys |
| :----------------: | :----: |
| macOS | <kbd>alt</kbd><kbd>cmd</kbd><kbd>i</kbd> |
| Windows | <kbd>ctrl</kbd><kbd>shift</kbd><kbd>i</kbd> |
| Linux | <kbd>ctrl</kbd><kbd>shift</kbd><kbd>i</kbd> |

Once you have your browser's developer tools open, your screen should look like the following:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/browser_tools_open.png">

Click on the `Network` tab at the top of the browser tools:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/network_tab.png">

Then click on `XHR` sub-tab inside of the `Network` tab:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/xhr_tab.png">

Once you're inside of the `XHR` sub-tab, refresh the page while you have your browser's developer tools open. After the page reloads, you should see a section titled `init` appear:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/init.png">

When you click on `init`, you should see a large sidebar appear. Make sure you're in the `Headers` section:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/headers.png">

After that, scroll down until you see a subsection called `Request Headers`. You should then see two important fields inside of the `Request Headers` subsection: `Cookie` and `User-Agent`.

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/request_headers.png">

Inside of the `Cookie` field, you will see a couple of important bits:

* `sess=`
* `auth_id=`
* `auth_uid_=`

You need everything ***after*** the equal sign and everything ***before*** the semi-colon for all of those bits. 

On a side note, your `auth_uid_` will *only* appear **if you have 2FA (two-factor authentication) enabled**. Also, keep in mind that your `auth_uid_` have numbers after the final underscore and before the equal sign (that's your auth_id). 

Once you've copied the value for your `sess` cookie, go back to the program, paste it in, and hit enter. Now go back to your browser, copy the `auth_id` value, and paste it into the program and hit enter. Then go back to your browser, copy the `auth_uid_` value, and paste it into the program and hit enter (**leave this blank if you don't use 2FA!!!**).

Once you do that, the program will ask for your user agent. You should be able to find your user agent ina field called `User-Agent` below the `Cookie` field. Copy it and paste it into the program and hit enter.

You're all set and you can now use it!


## Usage

Whenever you want to run the program, all you need to do is type `onlyfans-scraper` in your terminal. Once the program launches, all you need to do is follow the on-screen directions.

You will need to use your arrow keys to select an option:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/main_menu.png" width="450">

If you choose to download content, you will have the option of either having a list of your current subscriptions printed or manually entering a username:

<img src="https://raw.githubusercontent.com/Amenly/onlyfans-scraper/main/media/list_or_username.png">

### Liking/Unliking Posts

You can also use this program to like all of a user's posts or remove your likes from their posts. Just select either option during the main menu screen and enter their username.

This program will like posts at a rate of around one post per second. This may be reduced in the future but OnlyFans is strict about how quickly you can like posts.

### Migrating Databases

If you've used DIGITALCRIMINAL's script, you might've liked how his script prevented duplicates from being downloaded each time you ran it on a user. This is done through database files.

This program also uses a database file to prevent duplicates. In order to make it easier for user's to transition from his program to this one, this program will migrate the data from those databases for you (***only IDs and filenames***). 

In order to use it select the last option (Migrate an old database) and enter the *path* to the directory that contains the database files (*Posts.db, Archived.db, etc.*). 

For example, if you have a directory that looks like the following:

```
Users
|__ home
    |__ .sites
        |__ OnlyFans
            |__ melodyjai
                |__ Metadata
                    |__ Archived.db
                    |__ Messages.db
                    |__ Posts.db
```

Then the path you enter should be `/Users/home/.sites/OnlyFans/melodyjai/Metadata`. The program will detect the .db files in the directory and then ask you for the username to whom those .db files belong. The program will then move the relevant data over.
