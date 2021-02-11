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


async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")

		
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


def read_json(filename):
	with open(f"{filename}.json", "r") as file:
		data = json.load(file)
	return data


def write_json(data, filename):
	with open(f"{filename}.json", "w") as file:
		json.dump(data, file, indent=4)


@client.event
async def on_message(message):

	if message.author.bot:
		return

	await client.process_commands(message)


client.run('')
