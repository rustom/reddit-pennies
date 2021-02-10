import asyncpraw
import asyncio
import discord
import os

channelID = 808500202109009920
# subs = ['pennystocks']
# temp_keywords = ['OCGN', 'DD', 'moon', 'invest', 'tomorrow', 'covid', 'the', ' ', 'trading', 'stock', 'penny']

bar = '~~~~~~~~~~~~~~~~~~~~~~~~~~'

token = os.environ['DISCORDBOT_TOKEN']
username = os.environ['BOTONE_USERNAME']
password = os.environ['BOTONE_PASSWORD']
client_id = os.environ['BOTONE_ID']
client_secret = os.environ['BOTONE_SECRET']
user_agent = os.environ['BOTONE_AGENT']

client = discord.Client()

@client.event
async def on_ready():
    channel = client.get_channel(channelID)
    await channel.send(f'{client.user} has connected to Discord on channel #{channel.name}!')

    await scrape('pennystocks', channel)


async def scrape(sub, channel):
    count = 0
    while True:
        try:
            reddit = asyncpraw.Reddit(client_id=client_id, client_secret=client_secret,
                                      password=password, username=username, user_agent=user_agent)
            subreddit = await reddit.subreddit(sub)

            async for submission in subreddit.stream.submissions():
                print(count, submission.title)
                count += 1
                if submission.link_flair_text == 'DD :DD:':
                    await channel.send(bar + '\n' + '[' + submission.link_flair_text + ']' + submission.title + '\n' + submission.url + '/n/n')
            
        except Exception as e:
            await asyncio.sleep(30)
            print('EXCEPTION')

# Criteria:
# - DD flair
# - 300 upvotes
# - 50 comments
# - Last 5 hours

client.run(token)
client.close()