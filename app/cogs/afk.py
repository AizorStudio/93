import discord
from discord.ext import commands
import json


# Small bot, so using JSON for now


async def get_afk_data():
    with open("afk.json", "r") as f:
        users = json.load(f)

    return users


class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def afk(self, ctx, *, status="Not specified"):

        if len(status) > 100:
            await ctx.send(f"Status cannot have more than 100 characters")

        elif "<@" in status:
            await ctx.send(f"Status cannot contain mentions")

        elif "@everyone" in status or "@here" in status:
            await ctx.send(f"Status cannot contain mentions")

        else:
            users = await get_afk_data()

            if not ctx.author.id in users:
                users[str(ctx.author.id)] = {}
                users[str(ctx.author.id)]['status'] = status

            else:
                users[str(ctx.author.id)]['status'] = status


            with open("afk.json", "w") as f:
                json.dump(users, f)

            await ctx.send(f"AFK status set.")

    
    @commands.command(aliases=['imback'])
    async def removeafk(self, ctx):
        try:
            users = await get_afk_data()

            userid = str(ctx.author.id)
                
            del users[userid]

            with open("afk.json", "w") as f:
                json.dump(users, f)


            await ctx.send(f"Welcome back {ctx.author.display_name}, I removed your AFK status")

        except:
            await ctx.send(f"You have not set an AFK status. Try <afk (status)")

        
def setup(client):
    client.add_cog(Afk(client))
