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
            
        
def setup(client):
    client.add_cog(Afk(client))
