import discord
from discord.ext import commands
import os
import random
import time
import asyncio
import json
import requests
from requests import get
from json import loads

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("<", "93 "),
    case_insensitive=True,
    owner_id=353416871350894592,
    intents=intents)

client.remove_command('help')

# class MinHelp(commands.MinimalHelpCommand):
#     async def send_pages(self):
#         destination = self.get_destination()
#         for page in self.paginator.pages:
#             e = discord.Embed(description=page, title="Help Modules")
#             # e.set_footer(icon_url=self.ctx.author.avatar_url, text=f"Requested by {self.ctx.author}")
#             await destination.send(embed=e)

# client.help_command = MinHelp()


async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


# ---- Events ----

client.blacklisted_users = []

@client.event
async def on_ready():
	print('Logged in as {0} ({0.id})'.format(client.user))


async def ch_pr():
	await client.wait_until_ready()
	
	statuses = ['<help', 'with my host', 'in silence']

	while not client.is_closed():

		status = random.choice(statuses)

		await client.change_presence(activity=discord.Game(name=status))

		await asyncio.sleep(10)

client.loop.create_task(ch_pr())


# get token
token = ''
client.run(token)
