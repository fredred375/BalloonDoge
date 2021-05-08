# BalloonDoge
Discord bot made for 2021 PDAO staff

This bot automatically mentions staffs when a contestant should be delivered a balloon.

Staffs are mentioned depending on which classroom the balloon should be delivered to.

All other discord users can react to the comment and 'claim' or 'confirm' the delivery of the balloon.

# How to use 
Before using this script, you must make a discord application and add the bot to the target server.

Modify the variables in config.py.

```
DISCORD_TOKEN="YOURBOTTOKEN" 
DISCORD_CHANNEL_ID=8888888888888888888
DISCORD_USERS=['DISCORDUSER1', 'DISCORDUSER2', 'DISCORDUSER3', 'DISCORDUSER4']
URL='YOURAPIPATH'
DEV_URL='yourlocalfile.json'
BALLOON_LIST=[2, 5, 8, 11, 12]
```

Run python bot.py

***Warning***
The bot will stop functioning if internet connection is lost.