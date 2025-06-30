import discord
import feedparser
import asyncio
import os

DISCORD_TOKEN = os.getenv("token.env")
DISCORD_CHANNEL_ID = 995182313117172278
YOUTUBE_FEED_URL = os.getenv("https://www.youtube.com/feeds/videos.xml?channel_id=UCM513_k9-dobg3D5tuzM0hw")
CHECK_INTERVAL = 300

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_video_id = None

async def check_youtube():
    global last_video_id
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    while not client.is_closed():
        feed = feedparser.parse(YOUTUBE_FEED_URL)
        if not feed.entries:
            await asyncio.sleep(CHECK_INTERVAL)
            continue

        latest_entry = feed.entries[0]
        video_id = latest_entry.yt_videoid

        if video_id != last_video_id:
            last_video_id = video_id
            title = latest_entry.title
            url = latest_entry.link
            await channel.send(f"📢 **New YouTube Video!**\n**{title}**\n{url}")

        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

client.loop.create_task(check_youtube())
client.run(DISCORD_TOKEN)
