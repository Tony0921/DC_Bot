<!-- # DC_Bot -->
# DC_Bot
DC_Bot is a Discord bot created to enhance the user experience in Discord servers. The bot is written in Python and utilizes the Discord.py library.

## Features
* Add and remove emoji reactions to messages that correspond to certain roles.
* Store and display images in a pic library.
* Allow the bot to say any message on behalf of the user.
* Clear a specified number of messages from a channel.
* Display live streaming status of specified Twitch streamers.
* And more!

## Getting Started
To use DC_Bot in your Discord server, you will need to create a new bot application in the Discord Developer Portal and generate a bot token. Then, clone this repository and create a `config.json` file with your bot token and server settings.


```
{
    "token": "your_bot_token_here",
    "server_settings": {
        "Main_channel": "your_main_channel_id_here",
        "test_channel": "your_test_channel_id_here",
        "pic_lib": "pic_lib.json",
        "cmd_list": "cmd_list.json",
        "admin_cmd_list": "admin_cmd_list.json",
        "roles": "roles.json",
        "lang_live_status": "lang_live_status.json",
        "getLiveTime": "getLiveTime.json"
    }
}
```

Then, run the bot by running the `bot.py` file.
```
python bot.py
```

## Usage
The bot's commands can be accessed by typing `!help` in any text channel the bot has access to. This will display a list of available commands and their descriptions.

## License
DC_Bot is released under the MIT License. See LICENSE for more information.