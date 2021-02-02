import discord
from discord.ext import commands
import json
import requests
from pymongo import MongoClient


uri = "mongodb+srv://riju:1234@cluster0.vvjym.mongodb.net/osu?retryWrites=true&w=majority"


cluster = MongoClient(uri)
db = cluster["osu"]
col = db["osu"]


class Osu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group()
    async def osu(self, ctx):

        if ctx.invoked_subcommand is None:
            await ctx.send("OSU! Commands Usage:\n`<osu profile [username]`\n`<osu best [username]`\n`<osu setme [username]`")


    @osu.command()
    async def profile(self, ctx, user=None):
        if ctx.invoked_subcommand is None:
            if not user:
                if col.count({'id' : str(ctx.author.id)}) == 0:
                    await ctx.send(f"You haven't linked any OSU! profiles to your account. You can do this by typing `+osu setme [username]`\nTo search for another player's profile, try `+osu profile [username]`")
                    return

                else:
                    results = col.find({"id" : str(ctx.author.id)})

                    for result in results:
                        user = result['userid']
                        
            osu_id = user

            url = 'https://osu.ppy.sh/api/get_user'

            paras = {
                'k': '6a85011c43953ba2ee63ba939f40988dd399d90f',
                'u': osu_id,
            }

            r = requests.request('GET', url, params=paras).json()

            if len(r) == 0:
                await ctx.send(f"I couldn't find a user by the name **{user}**")
                return

            data = r[0]

            em = discord.Embed(
                color=0xfbc7ff
            )

            em.set_author(name=f"OSU! Stats — {data['username']}", icon_url=f"http://s.ppy.sh/a/{data['user_id']}")

            em.add_field(name="User ID", value=f"{data['user_id']}")
            em.add_field(name="Username", value=f"{data['username']}")
            em.add_field(name="Joined", value=f"{data['join_date']}")
            em.add_field(name="Level", value=f"{round(float(data['level']), 1)}")
            em.add_field(name="Country", value=f"{data['country']}")
            
            seconds = int(data['total_seconds_played'])

            hours = round(seconds/3600)

            em.add_field(name="Hours Played", value=f"{hours}")

            await ctx.send(embed=em)

    
    @osu.command()
    async def best(self, ctx, user=None):
        if ctx.invoked_subcommand is None:
            if not user:
                if col.count({'id' : str(ctx.author.id)}) == 0:
                    await ctx.send(f"You haven't linked any OSU! profiles to your account. You can do this by typing `+osu setme [username]`\nTo search for another player's best plays, try `+osu best [username]`")
                    return

                else:
                    results = col.find({"id" : str(ctx.author.id)})

                    for result in results:
                        user = result['userid']
                        
            osu_id = user

            url = 'https://osu.ppy.sh/api/get_user_best'

            paras = {
                'k': '6a85011c43953ba2ee63ba939f40988dd399d90f',
                'u': osu_id,
            }

            r = requests.request('GET', url, params=paras).json()

            if len(r) == 0:
                await ctx.send("I couldn't find a user by the name **{user}**")
                return

            data = r[0]
            

            em = discord.Embed(
                color=0xfbc7ff
            )

            em.set_author(name=f"OSU! Best Plays — {user}", icon_url=f"http://s.ppy.sh/a/{data['user_id']}")

            em.add_field(name="Beatmap ID", value=f"{data['beatmap_id']}")
            em.add_field(name="Score", value=f"{data['score']}")
            em.add_field(name="Played On", value=f"{data['date']}")
            em.add_field(name="Max Combo", value=f"{data['maxcombo']}")
            em.add_field(name="Ranking", value=f"{data['rank']}")
            em.add_field(name="PP", value=f"{data['pp']}")

            await ctx.send(embed=em)


    @osu.command()
    async def setme(self, ctx, user=None):
        if ctx.invoked_subcommand is None:
            if not user:
                await ctx.send(f"You didn't tell me what your OSU! username is")
                return

            url = 'https://osu.ppy.sh/api/get_user'

            paras = {
                'k': '6a85011c43953ba2ee63ba939f40988dd399d90f',
                'u': user,
            }

            r = requests.request('GET', url, params=paras).json()
            
            if len(r) == 0:
                await ctx.send(f"I couldn't find a profile with that username")
                return

            data = r[0]

            osu_id = data['username']

            if col.count({"userid" : str(ctx.author.id)}) !=0: 
                myquery = {"id" : str(ctx.author.id)}
                newvalue = {"$set" : {"userid" : osu_id}}

                col.update_one(myquery, newvalue)
            else:
                col.insert_one({"userid" : user, "id" : str(ctx.author.id)})

            
            await ctx.send("Added your profile!")


def setup(client):
    client.add_cog(Osu(client))
