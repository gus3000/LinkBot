import discord
import os
import re

from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

social_equivalents = {
    "instagram": "vxinstagram",
    "facebook": "facebed",
    "twitter": "fivvx",
    "tiktok": "tnktok",
}

re_social_domains = "|".join(social_equivalents)
re_pattern = r"https?://(www\.)?(" + re_social_domains + r")\.com/[^ ,]+"


def contains_social_url(content: str) -> str:
    match = re.search(re_pattern, content)
    if not match:
        return None
    return match.group(0)


def get_equivalent_url(url: str) -> str:
    for old, new in social_equivalents.items():
        url = url.replace(old, new)
    return url


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    url = contains_social_url(message.content)
    if url is not None:
        replacement = get_equivalent_url(url)
        await message.channel.send(replacement)


# for url in ['toto', 'https://www.instagram.com/p/DX6LBcziCDl/']:
#    if contains_social_url(url):
#        print(url, get_equivalent_url(url))

client.run(os.getenv("DISCORD_BOT_TOKEN"))
