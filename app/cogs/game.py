import discord
from discord.ext import commands
import json
import requests
from pymongo import MongoClient
import random


uri = "mongodb+srv://riju:1234@cluster0.vvjym.mongodb.net/osu?retryWrites=true&w=majority"


cluster = MongoClient(uri)
db = cluster["osu"]
col = db["osu"]


class Game(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group()
    async def minecraft(self, ctx):

        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                color=0xfff9f0, description="Lookup commands for Minecraft\n\n`<minecraft server`\n`<minecraft profile`\n\n**Usage:** `<minecraft server [server address]`\n**Usage:** `<minecraft profile [username]`"
            )

            em.set_author(name="Minecraft Commands", icon_url="https://cdn.freebiesupply.com/logos/large/2x/minecraft-1-logo-png-transparent.png")

            await ctx.send(embed=em)



    @minecraft.command()
    async def server(self, ctx, ip=None):
        if ctx.invoked_subcommand is None:
            if not ip:
                await ctx.send("Usage: `<minecraft server [server address]`")
                return

            try:
                url = "https://api.mcsrvstat.us/2/" + ip

                response = requests.request("GET", url).json()

                em = discord.Embed(color=0xfff9f0)
                em.set_author(name=f"Minecraft Server Status — {ip}", icon_url="https://i.imgur.com/t5Yz6Sm.png")

                if str(response['online']) == "True":
                    status = "Online <:online:782962511384281118>"

                else:
                    status = "Offline <:offline:782962511396864032>"

                em.add_field(name="Status", value=f"{status}")
                em.add_field(name="IP", value=f"{response['ip']}")
                em.add_field(name="Version", value=f"{response['version']}")
                em.add_field(name="Port", value=f"{response['port']}")
                em.add_field(name="Online", value=f"{response['players']['online']}")
                em.add_field(name="Max", value=f"{response['players']['max']}")

                await ctx.send(embed=em)
            except:
                await ctx.send(f"I couldn't find a server with that IP")
                

    
    @minecraft.command()
    async def profile(self, ctx, name=None):
        if ctx.invoked_subcommand is None:
            if not name:
                await ctx.send(f"Usage: `<minecraft profile [username]`")
                return

            try:
                url = "https://some-random-api.ml/mc"

                para = {'username': name}

                response = requests.request("GET", url, params=para).json()

                uuid = response['uuid']

            except:
                await ctx.send(f"I couldn't find a player with the name '{name}'")
                return

            body_url = "https://crafatar.com/renders/body/" + uuid + ".png"

            face_url = "https://crafatar.com/avatars/" + uuid + ".png"

            hypixel_stats_url = "https://api.hypixel.net/player?key=7357c1b5-d1cd-48a3-955c-f567a1a2a63e&uuid=" + uuid

            response = requests.request("GET", hypixel_stats_url).json()

            player = response['player']

            try:
                try:
                    aliases = player['knownAliases']

                    names = ", ".join(aliases)
                    name = player['displayname']
                except:
                    names = player['displayname']
                    name = name

            except:
                names = f"{name}"
                name = name

            em = discord.Embed(color=0xfff9f0,
                description=f"[Download Skin](https://crafatar.com/skins/{uuid}.png) | [Download Cape](https://crafatar.com/capes/{uuid}.png)"
            )

            em.set_author(name=f"Minecraft Info — {name}", icon_url=face_url)

            em.set_thumbnail(url=body_url)

            em.add_field(name="UUID", value=uuid)
            em.add_field(name="Username History", value=names)

            await ctx.send(embed=em)


    @commands.command(aliases=['ow'])
    async def overwatch(self, ctx, category: str = None, platform: str= None, tag: str= None):
        if not category and not platform and not tag:
            em = discord.Embed(color=0xfff9f0, description="""
Lookup commands for Overwatch

`<overwatch profile` - Basic profile stats for provided user

**Usage:** <overwatch profile [platform] [UserTag]
**Usage Example:** <overwatch profile pc 
""")

            em.set_author(name="Overwatch Commands", icon_url="https://i.imgur.com/kLMpcqV.jpg")

            await ctx.send(embed=em)
            return

        if not category:
            await ctx.send(f"You need to enter a category.\nValid Categories: `profile`")
            return

        if not platform:
            await ctx.send(f"You need to enter a platform.")
            return

        if not tag:
            await ctx.send(f"You need to enter a valid user tag.\nExample: Cat#24713")
            return

        if category.lower() == "profile":

            try:

                platform = platform.lower()

                tag = tag.replace("#", "-")

                url = f"https://ow-api.com/v1/stats/{platform}/eu/{tag}/profile"

                response = requests.request('GET', url).json()

                em = discord.Embed(color=0xfff9f0)

                em.set_author(name=f"{response['name']}", icon_url=f"{response['icon']}")

                em.add_field(name="Level", value=f"{response['level']}")

                em.add_field(name="Basic Quickplay Stats", value=f"**Games Won:** {response['quickPlayStats']['games']['won']}")

                em.add_field(name="Basic Competitive Stats", value=f"**Games Played:** {response['competitiveStats']['games']['played']}\n**Games Won:** {response['competitiveStats']['games']['won']}\n**Games Lost:** {response['competitiveStats']['games']['played'] - response['competitiveStats']['games']['won']}\n**Damage SR:** {response['rating']}")

                em.set_thumbnail(url=f"{response['icon']}")

                await ctx.send(embed=em)

            except:
                await ctx.send(f"I couldn't find a profile for this user")

        else:
            await ctx.send(f"Valid sub-command: `profile`")



    @commands.command()
    async def gif(self, ctx, *, search):
        try:
            url = "http://api.giphy.com/v1/gifs/search"

            para = {'api_key': 'eeQBgh7U7n9WtBbTTuuhoOefLno8b1rK', 'q': search, 'limit': 20}

            response = requests.request("GET", url, params=para).json()

            em = discord.Embed(color=0xfbbdff)

            em.set_image(url=response['data'][random.randrange(0, 18)]['images']['original']['url'])

            await ctx.send(embed=em)

        except:
            await ctx.send(f"I couldn't find any gifs")



    @commands.command()
    async def memegen(self, ctx, temp=None, *, texts: str = None):

        if not temp:
            em = discord.Embed(title="Meme Generator", color=0xfff9f0,
                            description="""
    To create a meme, type the command followed by the ID of the template, and the texts you want to add to the meme.
    Each text should be separate by a `;`
        
    **Usage Example:** `<memegen 3 text1;text2`
        
    **1.** Distracted Boyfriend
    **2.** Drake Hotline Bling
    **3.** Two Buttons
    **4.** Batman Slapping Robin
    **5.** Change My Mind
    **6.** UNO Draw 25 Cards
    **7.** Surprised Pikachu
    **8.** Inhaling Seagull
    **9.** Trump Bill Signing
    **10.** 10 Guy
    **11. ** Custom
        
                            
    """

                            )

            await ctx.send(embed=em)
            return

        elif not texts:
            await ctx.send("You asked me to create a meme, but didn't tell me what texts you want in the meme")
            return

        templates = {
            "1": "112126428",
            "2": "181913649",
            "3": "87743020",
            "4": "438680",
            "5": "129242436",
            "6": "217743513",
            "7": "155067746",
            "8": "114585149",
            "9": "91545132",
            "10": "101440",
            "11": " ",

        }

        if temp not in templates:
            await ctx.send(f":warning: Invalid template ID")
            return

        if temp == "11":
            await ctx.send(":warning: Under Maintenance")
            return

        text_list = texts.split(";")

        url = 'https://api.imgflip.com/caption_image'

        params = {
            'username': "rijulol",
            'password': "riju1234",
            'template_id': templates[temp],
            'text0': text_list[0],
            'text1': text_list[1],
            'font': "impact",
        }
        response = requests.request('POST', url, params=params).json()

        if response['success']:
            em = discord.Embed(description=f"{ctx.author.mention}", color=0xfff9f0)

            em.set_image(url=response['data']['url'])

            await ctx.send(embed=em)

        else:
            await ctx.send("Services down, try again later")



    @commands.command()
    async def game(self, ctx, *, search=None):

        if not search:
            await ctx.send("You asked me to do a Game search, but didn't tell me the game's name.\n**Usage:** `<game [game name]`")

        search = search.strip(" ")

        search = search.replace(" ", "-")

        url = f"https://api.rawg.io/api/games/{search}?key=3984a58125dc4ddd890f5397fd9ccb09"

        response = requests.request("GET", url).json()

        try:
            name = response['name']
            released = response['released']
            image = response['background_image']
            website = response['website']
            rating = response['rating']
            description = str(response['description_raw']).replace("###", "#")
            if len(description) > 2000:
                description = description[:2000] + "..."

            platforms_raw = response['parent_platforms']

            platforms = []

            for i in platforms_raw:
                platforms.append(i['platform']['name'])

            em = discord.Embed(title=f"{name}", url=f"{website}", description=f"{description}", color=0xfff9f0)

            em.set_thumbnail(url=f"{image}")

            em.add_field(name="Released", value=f"{released}", inline=False)
            em.add_field(name="Rating", value=f"{rating}", inline=False)
            em.add_field(name="Website", value=f"{website}", inline=False)
            em.add_field(name="Platforms", value=", ".join(platforms), inline=False)

            await ctx.send(embed=em)

        except:
            await ctx.send(f"No results found. Be more specific with the name")


def setup(client):
    client.add_cog(Game(client))
