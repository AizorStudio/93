import discord
from discord.ext import commands
import asyncio
import requests
import random
import re
import io
from io import StringIO
import PIL
from PIL import Image

def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


def get_archive(in_list):
    file = io.open("archive.txt", "w", encoding="utf-8")
    file.writelines(in_list)


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)


class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['exp', 'e'])
    async def expand(self, ctx, emoji: discord.PartialEmoji):
        try:
            await ctx.send(emoji.url)
        except:
            await ctx.send("Not a custom emote")


    @commands.command(aliases=['avy', 'av'])
    async def avatar(self, ctx, member: discord.Member = None):

        if not member:
            member = ctx.author
            
        embed = discord.Embed(title=f"{member}", color=0xb5b5b5)

        embed.set_image(url=member.avatar_url)

        await ctx.send(embed=embed)


    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            color=0xb5b5b5, title=f"Server Info — {ctx.guild.name}"
        )
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="Created At", value=f"{str(ctx.guild.created_at)[:-7]}", inline=False)
        embed.add_field(name="Channels",
                        value=f"Voice: {len(ctx.guild.voice_channels)}  Text: {len(ctx.guild.text_channels)}  Category: {len(ctx.guild.categories)}",
                        inline=False)
        embed.add_field(name="Ownership", value=f"{ctx.guild.owner}")
        embed.add_field(name="Tier—Boosts—Boosters",
                        value=f"{ctx.guild.premium_tier}—{ctx.guild.premium_subscription_count}—{len(ctx.guild.premium_subscribers)}",
                        inline=False)
        region = str(ctx.guild.region)
        embed.add_field(name="Server Region", value=f"{region.capitalize()}")
        embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Role Count", value=f"{len(ctx.guild.roles)}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        try:
            embed.set_image(url=f"{ctx.guild.banner_url}")

        except:
            pass

        await ctx.send(embed=embed)


    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        embed = discord.Embed(color=0xb5b5b5, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info — {member}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="Member ID", value=member.id)
        embed.add_field(name="Display ID", value=member.display_name)

        created = str(member.created_at)
        joined = str(member.joined_at)

        embed.add_field(name="Created At", value=created[:-7])
        embed.add_field(name="Joined At", value=joined[:-7])

        embed.add_field(name="Top role", value=member.top_role.mention)

        embed.add_field(name="Bot", value=member.bot)

        roles = [role for role in member.roles if role != ctx.guild.default_role]

        if len(roles) == 0:
            embed.add_field(name=f"Roles ({len(roles)})", value="No Roles")
        else:
            embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def archive(self, ctx, limit=50):
        if limit > 2500:
            await ctx.send(f"Too many messages (>2500)")
            return

        counter = 0
        msgs = []
        async for message in ctx.channel.history(limit=limit):
            try:
                msgs.append(f"[{str(message.created_at)[:-7]}] - {message.author} -> {message.content}\n")
            except:
                pass
            counter += 1

        get_archive(msgs)

        if len(msgs) == 0:
            await ctx.send(f":warning: No messages found")
        else:
            file = discord.File("archive.txt", filename="archive.txt")
            await ctx.send(f"{ctx.author.mention} Ok, I archived {len(msgs)} messages that I could access", file=file)


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def cleanme(self, ctx, limit=50):
        if limit > 2500:
            await ctx.send(f"Too many messages (>2500)")
            return

        counter = 0
        msgs = []
        async for message in ctx.channel.history(limit=limit):
            if message.author == ctx.author:
                try:
                    msgs.append(f"[{str(message.created_at)[:-7]}] - {message.author} -> {message.content}\n")
                    await message.delete()
                except:
                    pass
            else:
                pass

            counter += 1

        get_archive(msgs)

        if len(msgs) == 0:
            await ctx.send(f":warning: I could not find any messages sent by you in the last {limit} searched messages")
        else:
            file = discord.File("archive.txt", filename="archive.txt")
            await ctx.send(f"Ok, {ctx.author.mention} I have deleted your messages and sent you the archived file on DM")
            await ctx.author.send(f"{ctx.author.mention} Ok, I archived {len(msgs)} messages that I could access", file=file)


    @commands.command()
    async def roleinfo(self, ctx, roles: discord.Role):

        em = discord.Embed(
            color=0xb5b5b5
        )
        em.add_field(name="Role ID", value=f"{roles.id}")
        em.add_field(name="Members with", value=f"{len(roles.members)}")
        em.add_field(name="Displayed Sep", value=f"{roles.hoist}")
        em.add_field(name="Created At", value=f"{str(roles.created_at)[:-7]}")
        em.add_field(name="Top Position", value=f"{len(ctx.guild.roles) - roles.position - 1}")
        em.add_field(name="Colour Hex", value=f"{roles.colour}")
        em.set_author(name=f"Role Info — {roles.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)


    @commands.command()
    async def weather(self, ctx, *, query=None):

        if not query:
          await ctx.send(f'You did not tell me what location to search the weather for')
          return

        try:

            querya = query.replace(" ", "+")

            api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=6106f39f370b92d9491bfc26e5df4f3e&q='

            url = api_address + querya

            json_data = requests.get(url).json()

            weather_t = json_data['weather'][0]['main']

            temp = json_data['main']['temp']

            temp_c = (int(temp) - 273.15)

            temp_f = (temp_c * 9 / 5) + 32

            windspeed = json_data['wind']['speed']

            feels_like = json_data['main']['feels_like']

            feels_like = round(int(feels_like) - 273.15)

            temp_min = json_data['main']['temp_min']
            temp_min_c = (int(temp_min) - 273.15)

            temp_max = json_data['main']['temp_max']
            temp_max_c = (int(temp_max) - 273.15)

            pressure = json_data['main']['pressure']

            humidity = json_data['main']['humidity']

            loc_c = json_data['sys']['country']

            loc_p = json_data['name']

            visibility = json_data['visibility']

            lat = json_data['coord']['lat']

            lon = json_data['coord']['lon']

            embed = discord.Embed(
                color=0xb3bbff

            )

            embed.set_author(name=f"Weather — {loc_p}, {loc_c}", icon_url='https://i.imgur.com/CpbNTYM.gif')


            embed.add_field(name=':cloud: Weather', value=f"{weather_t}",
                            inline=True)
            embed.add_field(name=':sweat: Humidity',
                            value=f"{humidity}%",
                            inline=True)
            embed.add_field(name=":thermometer: Temperature", value=f"{round(temp_f, 2)}°F/{round(temp_c, 2)}°C",
                            inline=True)
            embed.add_field(name=":white_sun_small_cloud: Feels Like", value=f"{feels_like}°C",
                            inline=True)
            embed.add_field(name=':dash: Wind Speed',
                            value=f"{windspeed}mph",
                            inline=True)
            embed.add_field(name=":eyes: Visibility",
                            value=f"{visibility}m",
                            inline=True)
            embed.add_field(name=":straight_ruler: Lat/Long",
                            value=f"{lat}/{lon}",
                            inline=True)
            embed.add_field(name=":high_brightness: Min/Max",
                            value=f"{round(temp_min_c, 1)}°C/{round(temp_max_c, 1)}°C",
                            inline=True)
            embed.add_field(name=":anger: Pressure",
                            value=f"{pressure}hPa",
                            inline=True)

            await ctx.send(embed=embed)

        except:
            em = discord.Embed(
                description="Location not found", color=0xff0000
            )

            await ctx.send(embed=em)

        
    @commands.command(aliases=['time', 'clock'])
    async def timer(self, ctx, arg):
        await ctx.send(f"Ok, I have set the timer")

        amount = convert(arg)

        await asyncio.sleep(amount)

        em = discord.Embed(description=f"Time up! {amount}", color=0xe2b8ff)
        em.set_author(name="Timer", icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=em)


    @commands.command()
    async def choose(self, ctx, *choices):
        string = " ".join(choices)

        string = string.split(';')

        await ctx.send(f"{ctx.author.mention} I would choose: {random.choice(string)}")


    @commands.command()
    async def remind(self, ctx, arga, *, args):
        arg = convert(arga)
        await ctx.message.delete()
        await ctx.send(f"Ok, I will remind you")
        await asyncio.sleep(arg)
        em = discord.Embed(description=f"{args}", color=0x85a9ff)
        em.set_author(name="Event Reminder", icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=em)


    @commands.command()
    async def flip(self, ctx, coins=None):
    
        choice = ['h', 't']
    
        if not coins:
            ch = random.choice(choice)
            if ch == "t":
                text = "Heads!"
            else:
                text = "Tails!"
    
            await ctx.send(text)
            return
    
        try:
            coins = int(coins)
    
            if coins >= 1000:
                await ctx.send("Too many coins >1000")
    
            elif coins < 2:
                await ctx.send("Choose more than 2 coins")
    
            else:
                flips = []
    
                for i in range(coins):
                    ch = random.choice(choice)
                    flips.append(ch)
    
                count_h = flips.count('h')
                count_t = flips.count('t')
    
                await ctx.send(f"Heads: {count_h}\nTails: {count_t}")
    
        except:
            await ctx.send("Invalid format. Usage: `<flip [number of coins]`")


    @commands.command(aliases=['ht'])
    async def historytoday(self, ctx, choice=None):
        URL = 'http://history.muffinlabs.com/date'

        response = requests.request('GET', URL).json()

        # Events

        events = response['data']['Events']

        rand_event = events[random.randrange(0, len(events))]

        # Births

        births = response['data']['Births']

        rand_birth = births[random.randrange(0, len(births))]

        # Deaths

        deaths = response['data']['Deaths']

        rand_deaths = deaths[random.randrange(0, len(deaths))]

        em = discord.Embed(color=0x8fff93)

        em.add_field(name=f"•  Events: {rand_event['year']} — {rand_event['text']}",
                    value=f"{rand_event['links'][0]['link']}", inline=False)
        em.add_field(name=f"•  Births: {rand_birth['year']} — {rand_birth['text']}",
                    value=f"{rand_birth['links'][0]['link']}", inline=False)
        em.add_field(name=f"•  Deaths: {rand_deaths['year']} — {rand_deaths['text']}",
                    value=f"{rand_deaths['links'][0]['link']}", inline=False)

        await ctx.send(embed=em)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def poll(self, ctx, *, message):
        em = discord.Embed(description=f"Enter type of poll: [1] Yes/No [2] Multiple Choice", color=0x85a9ff)
        em.set_author(name="Poll type", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)
        ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
        content = ida.content
        content = str(content)
        
        if content == "1":
            em = discord.Embed(title="📢 Poll", description=f"{message}")
            msg = await ctx.send(embed=em)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        elif content == "2":
            reacts = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            emx = discord.Embed(description=f"Enter options, each separated by a `;` (maximum choices: 9)", color=0x85a9ff)
            emx.set_author(name="Enter options", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emx)
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=60)
            content = ida.content
            content = str(content)
            options = content.split(";")
            if len(options) > 9:
                await ctx.send(f"Max options supported: 9")
            else:
                em = discord.Embed(title="📢 Poll", description=f"{message}")
                for i in range(len(options)):
                    em.add_field(name=f"{reacts[i]}", value=f"{options[i]}", inline=False)
                msg = await ctx.send(embed=em)
                for j in range(len(options)):
                    await msg.add_reaction(f"{reacts[j]}")
        else:
            await ctx.send(f"Choice incorrectly entered")

    @commands.command(aliases=['lyric', 'ly'])
    async def lyrics(self, ctx, *, title: str = None):
        if not title:
            await ctx.send("You didn't tell me what song to fetch the lyrics for\nUsage: `<lyrics [song name]` (Specify author name for more precise results)")
            return

        title.replace(" ", "+")

        url = "https://some-random-api.ml/lyrics?title=" + title

        r = requests.request('GET', url).json()

        try:
            if r['error']:
                await ctx.send("I couldn't find lyrics for that song")
                return
            else:
                pass

        except:
            pass

        description = r['lyrics']

        if len(description) > 2000:
            description = description[:2000] + "..."

        em = discord.Embed(
            color=0xb5b5b5,
            title=f"{r['title']} - {r['author']}", url=f"{r['links']['genius']}",
            description=description

        )

        em.set_thumbnail(url=f"{r['thumbnail']['genius']}")

        em.set_footer(text="Didn't get what you're looking for? Try adding the author's name to the search")

        await ctx.send(embed=em)
        
    @commands.command()
    async def color(self, ctx, hex: str = None):
        if not hex:
            await ctx.send("No hex provided")

        hex = hex.replace('#', '')

        url = "https://some-random-api.ml/canvas/colorviewer?hex=" + hex

        r = requests.request('GET', url)

        with open('color.png', 'wb') as f:
            for chunk in r:
                f.write(chunk)

        im = Image.open('color.png')

        new_image = im.resize((64,64))

        new_image.save('color.png')


        file = discord.File("color.png", filename="color.png")
        await ctx.send(file=file)


    @commands.command()
    async def cowsay(self, ctx, *, say):
        if len(say) > 150:
            await ctx.send(f"Too many characters (>150)")
            return

        await ctx.send(f"""```fix
    ---------------------------------------
    [  {say}  ]
    ---------------------------------------
            \   ^__^ 
            \   (oo)\_______
                (__)\       )\/
                    ||----w |
                    ||     ||```
    """)


    @commands.command(aliases=['poke', 'pokedex'])
    async def pokemon(self, ctx, *, poke: str = None):

        if not poke:
            await ctx.send("You didn't tell me what Pokémon to search for\nUsage: `<pokemon [name]`")
            return

        poke = poke.replace(" ", "+")

        url = "https://some-random-api.ml/pokedex?pokemon=" + poke

        r = requests.request('GET', url).json()

        try:
            if r['error']:
                await ctx.send(f"I couldn't find a Pokémon by that name")
                return
            else:
                pass

        except:
            pass

        em = discord.Embed(
            color=0xfffafa
        )

        em.set_thumbnail(url=f"{r['sprites']['animated']}")

        em.set_author(name=f"Pokémon — {str(r['name']).capitalize()}", icon_url="https://i.gifer.com/origin/28/2860d2d8c3a1e402e0fc8913cd92cd7a_w200.gif")

        em.add_field(name="Type", value=", ".join(r['type']))
        em.add_field(name="Species", value=", ".join(r['species']))
        em.add_field(name="Abilities", value=", ".join(r['abilities']))
        em.add_field(name="Height", value=f"{r['height']}")
        em.add_field(name="Weight", value=f"{r['weight']}")
        em.add_field(name="HP", value=f"{r['stats']['hp']}")
        em.add_field(name="Attack", value=f"{r['stats']['attack']}")
        em.add_field(name="Defense", value=f"{r['stats']['defense']}")
        em.add_field(name="Speed", value=f"{r['stats']['speed']}")

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Utils(client))
