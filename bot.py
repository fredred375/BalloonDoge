# bot.py
import os
import discord
import requests
import json
import asyncio
import pandas as pd
from config import *

# dev mode gets data from local file
dev = True

df = pd.read_excel("teamInfo.xlsx")
classroom = df['classroom']
mention = classroom.replace(
    ['管一B101', '管一203', '管一204', '管一103'],
    DISCORD_USERS
)
    

# blocking function to retrieve and parse data, dict[username] = AC_list[]
def getScores():
    if dev:
        with open(DEV_URL, encoding="utf-8") as f:
            data = json.load(f)
    else:
        response = requests.get(URL)
        data = response.json()
    users_AC_list = {}
    for username in data:
        AC_list = []
        for problem in data[username]['problems']:
            if data[username]['problems'][problem]['status'] == 'AC':
                AC_list.append(problem)
        users_AC_list[username] = AC_list
    # print(users_AC_list)
    return users_AC_list

# custom bot class inherited from discord.Client, check https://discord.com/developers/docs/ for class details
class BalloonDoge(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.channel = self.get_channel(DISCORD_CHANNEL_ID)
        self.loop.create_task(self.main())

    # modfies messages on user reactions
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        if user == self.user: return
        if emoji == DONE_EMOJI:
            message = reaction.message
            await message.clear_reaction(DONE_EMOJI)
            content = message.content
            paran = content.find('(')
            if paran > 0:
                content = content[:paran]
            await message.edit(content=content + " (Delivered by {})".format(user.mention))
            # await reaction.message.delete()
        elif emoji == CLAIM_EMOJI:
            message = reaction.message
            await message.clear_reaction(CLAIM_EMOJI)
            await message.add_reaction(DONE_EMOJI)
            content = message.content
            paran = content.find('(')
            if paran > 0:
                content = content[:paran]
            await message.edit(content=content + " (Claimed by {})".format(user.mention))

    async def sendBalloonMessage(self, content):
        message = await self.channel.send(content)
        await message.add_reaction(CLAIM_EMOJI)

    async def newAC(self, username, len_AC_list, problem):
        print(f"New AC: {username} - {problem}")
        print(f"{username} now has a total of {len_AC_list} AC")
        if len_AC_list in BALLOON_LIST:
            await self.sendBalloonMessage(f"`[{self.usernameToIndex[username]}] {username}` at {classroom[self.usernameToIndex[username]]} has reached {len_AC_list} AC by solving {problem}! - **Please send them a balloon!** (Assigned to <@{mention[self.usernameToIndex[username]]}>)")

    async def main(self):
        saved_users_AC_list = {}
        initial_list = getScores()
        self.usernameToIndex = dict((username, i) for (i, username) in enumerate(initial_list))
        if not all(len(initial_list[i]) == 0 for i in initial_list):
            res = input("The scoreboard seems not empty. Resend all balloons? (y/Y/n/N): ").strip()
            if res == 'n' or res == 'N':
                saved_users_AC_list = {}
            else:
                saved_users_AC_list = dict((i, []) for i in initial_list)
                assert res == 'y' or res == 'Y'

        while True:
            try:
                users_AC_list = getScores()
                for username in users_AC_list:
                    for problem in users_AC_list[username]:
                        if username in saved_users_AC_list and problem not in saved_users_AC_list[username]:
                            # new AC
                            saved_users_AC_list[username].append(problem)
                            await self.newAC(username, len(saved_users_AC_list[username]), problem)
                saved_users_AC_list = users_AC_list
                # using non-blocking instead of time.sleep() to keyboard interrupt immediately
                await asyncio.sleep(int(SECONDS_BETWEEN_FETCH))
            except KeyboardInterrupt:
                await self.close()
                exit(0)
            except Exception as e:
                print('{}: {}'.format(type(e).__name__, e))
                await self.close()
                exit(1)

doge = BalloonDoge()
doge.run(DISCORD_TOKEN)