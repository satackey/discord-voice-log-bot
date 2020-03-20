# Discord voice log bot
## Original author: Beskhue
## Forked by: briansukhnandan
## Requirements
This bot requires Python 3.6.

To install requirements:

```pip install -r requirements.txt```

## Configuration
You might want to create a new bot on Discord (i.e., create an application at https://discordapp.com/developers/applications/me/ and turn it into a bot).


Configure the bot by creating the file `src/config.ini` and adding:
```
[Attributes]
CHANNEL_NAME=voice-log
BOT_TOKEN=####################
```
where '#################' is your Bot's token obtained from 'https://discordapp.com/developers/applications'

## Running
Run the bot by executing:

```python3.6 src/main.py```
after installing requirements.
