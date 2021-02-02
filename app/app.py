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
    owner_id=353416871350894592, intents=intents)

client.remove_command('help')

# ---- Cogs ----


@client.command()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")

client.blacklisted_users = []

# ---- Events ----


@client.event
async def on_ready():
	data = read_json("blacklisted")
	client.blacklisted_users = data["blacklistedUsers"]
	print('Logged in as {0} ({0.id})'.format(client.user))


async def ch_pr():
	await client.wait_until_ready()
	
	statuses = ['<help', 'with my host', 'in silence']

	while not client.is_closed():

		status = random.choice(statuses)

		await client.change_presence(activity=discord.Game(name=status))

		await asyncio.sleep(10)

client.loop.create_task(ch_pr())


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(":warning: Missing parameters")
		return

	if isinstance(error, commands.MissingPermissions):
		missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
		if len(missing) > 2:
			fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
		else:
			fmt = ' and '.join(missing)
		_message = ':no_entry: You need the **{}** permission(s) to use this command.'.format(fmt)
		await ctx.send(_message)
		return

	if isinstance(error, commands.CommandOnCooldown):
		coold = str(time.strftime('%H:%M:%S', time.gmtime(error.retry_after)))
		await ctx.send(f":warning: **{ctx.author}** Cooldown: {coold}")
		return

	if isinstance(error, commands.BotMissingPermissions):
		missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
		if len(missing) > 2:
			fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
		else:
			fmt = ' and '.join(missing)
		_message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
		await ctx.send(_message)
		return


# ---- Blacklisted ----


def read_json(filename):
	with open(f"{filename}.json", "r") as file:
		data = json.load(file)
	return data


def write_json(data, filename):
	with open(f"{filename}.json", "w") as file:
		json.dump(data, file, indent=4)


async def get_afk_data():
	with open("afk.json", "r") as f:
		users = json.load(f)

	return users


@client.event
async def on_message(message):

	users = await get_afk_data()

	userid = str(message.author.id)

	if message.author.id in client.blacklisted_users:
		return

	if message.author.bot:
		return

	if userid in users:
		del users[userid]

		with open("afk.json", "w") as f:
			json.dump(users, f)

		await message.channel.send(
		    f"Welcome back {message.author.display_name}"
		)

	for x in users:
		if x in message.content.lower():
			member = client.get_user(int(x))
			name = member.name
			await message.channel.send(
			    f"{message.author.mention} {name} is AFK — {users[x]['status']}"
			)

	await client.process_commands(message)


# ---- Basic Commands ----


@client.command()
async def motivate(ctx):
    response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    await ctx.send('{quoteText} - {quoteAuthor}'.format(**loads(response.text)))


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=9):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"<:93_coin:803910969834602536> Global Leaderboard", color=0xf7ff8a)
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt} <:93_coin:803910969834602536>", inline=True)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@client.command()
async def hello(ctx):
	responses = ['Hello!', 'Hey!', "I'm here", 'Hello~']
	await ctx.send(f"{random.choice(responses)}")


@client.command()
async def ping(ctx):
  before = time.monotonic()
  message = await ctx.send(":ping_pong: Pong!")
  ping = (time.monotonic() - before) * 1000
  await message.edit(content=f":ping_pong: Pong! {round(int(ping))}ms")


@client.command(aliases=['say'])
@commands.has_permissions(manage_messages=True)
async def repeat(ctx, *args):
	await ctx.send(' '.join(args))


@client.command()
async def invite(ctx):
    em = discord.Embed(
        color=0xfcfcfc,
        description="Powerful utility and moderation bot, created by ive and chunchunmaru. Written in Python using discord.py [Invite](https://discord.com/oauth2/authorize?client_id=718749763859775559&permissions=8&scope=bot)"
    )

    em.set_author(name="Invite ナインスリー to your guild", icon_url=client.user.avatar_url)

    em.set_image(url="https://i.imgur.com/6rXCToA.png")

    await ctx.send(embed=em)


client.run('')
