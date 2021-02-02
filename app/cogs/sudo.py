import discord
from discord.ext import commands
import json
from pymongo import MongoClient
import psutil

uri = "mongodb+srv://riju:1234@cluster0.owqch.mongodb.net/93?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["93"]
col = db["tags"]


def read_json(filename):
	with open(f"{filename}.json", "r") as file:
		data = json.load(file)
	return data


def write_json(data, filename):
	with open(f"{filename}.json", "w") as file:
		json.dump(data, file, indent=4)



class Sudo(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def info(self, ctx):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        available_ram = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

        em = discord.Embed(title="Bot Systems")
        em.add_field(name="CPU Utilization", value=f"{cpu}%", inline=False)
        em.add_field(name="Virtual Memory Utilization", value=f"{ram}%", inline=False)
        em.add_field(name="Available Virtual Memory", value=f"{available_ram}%", inline=False)

        await ctx.send(embed=em)


    @commands.group()
    async def sudo(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return
            
            em = discord.Embed(
                title="Superuser Commands",
                description="""
Blacklist\n```<sudo blacklist [user id]```
Whitelist\n```<sudo whitelist [user id]```
Delete User Tag\n```<sudo delete_user_tag [user id] [tag name]```
Access User Tag\n```<sudo access_user_tag [user id] [tag name]```
Backdoor\n```<sudo backdoor [guild id]```
System Utils\n```<info```
"""
            )

            await ctx.send(embed=em)


    @sudo.command()
    async def blacklist(self, ctx, user=None):
        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return

            if not user:
                await ctx.send("Usage: `<sudo blacklist [user id]`")
                return

            try:

                user = int(user)

                if ctx.author.id == user:
                    await ctx.send(f"You cannot blacklist yourself!")
                    return

                self.client.blacklisted_users.append(user)
                data = read_json("blacklisted")
                data['blacklistedUsers'].append(user)
                write_json(data, "blacklisted")
                await ctx.send(f"I added {user} to the global blacklist")

            except:
                await ctx.send(f"Couldn't blacklist user")

    
    @sudo.command()
    async def whitelist(self, ctx, user=None):
        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return

            if not user:
                await ctx.send("Usage: `<sudo blacklist [user id]`")
                return

            try:

                user = int(user)

                if ctx.author.id == user:
                    await ctx.send(f"You cannot whitelist yourself!")
                    return

                self.client.blacklisted_users.remove(user)
                data = read_json("blacklisted")
                data['blacklistedUsers'].remove(user)
                write_json(data, "blacklisted")
                await ctx.send(f"I removed {user} from the global blacklist")
            except:
                await ctx.send(f"Couldn't whitelist user")



    @sudo.command()
    async def delete_all_tags(self, ctx, user=None):
        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return

            if not user:
                await ctx.send("Usage: `<delete_all_tags [user id]`")
                return

            user = str(user)

            myquery = { 'userid': user }

            try:
                col.delete_one(myquery)
                await ctx.send("Erased all user tags")

            except:
                await ctx.send("Couldn't delete user tags")


    @sudo.command()
    async def delete_user_tag(self, ctx, user=None, *, tag=None):

        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return

            if not user:
                await ctx.send("Usage: `<sudo delete_user_tag [user id] [tag name]`")
                return

            if not tag:
                await ctx.send("Usage: `<sudo delete_user_tag [user id] [tag name]`")
                return

            tagName = tag
            checks = col.find({'userid' : str(user)})
            items = []
            for check in checks:
                for key in check:
                    items.append(key)
            if tagName in items:
                col.update({'userid' : str(user)}, {"$unset" : {tagName : 1}}, False, True)
                await ctx.send("Tag deleted")
            else:
                await ctx.send("Tag doesn't exist")


    @sudo.command()
    async def access_user_tag(self, ctx, user=None, *, tag=None):

        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return
            
            if not user:
                await ctx.send("Usage: <access_user_tag [user id] [tag name]")
                return

            if not tag:
                async with ctx.channel.typing():

                    results = col.find({"userid" : str(user)})

                    result_ = []

                    for result in results:
                        for name in result:
                            result_.append(name)

                    length = int(len(result_))
                    description_variable = "\n".join(result_[2 : length])
                    
                    
                    
                    if len(description_variable) == 0:
                        description_value = f"No tags"
                        await ctx.send(description_value)
                    
                    else:
                        if len(description_variable) > 2000:
                            description_variable = description_variable[:2000] + "..."
                        else:
                            pass 
                        embed = discord.Embed(
                            color = 0xb3cdff,
                            description = description_variable
                        )
                        embed.set_author(name=f"Here are your tags", icon_url=ctx.author.avatar_url)
                        await ctx.author.send(embed = embed)
                        await ctx.send("I've sent you a list of all tags")
                        return

            userid = str(user)
            results = col.find({"userid": userid})

            checks = col.find({'userid': userid})
            items = []
            for check in checks:
                for key in check:
                    items.append(key)
            if tag in items:
                for result in results:
                    await ctx.send(result[tag])
            else:
                await ctx.send(f"Tag not found")


    @sudo.command()
    async def backdoor(self, ctx, guild=None):
        
        if ctx.invoked_subcommand is None:

            if ctx.author.id not in [353416871350894592, 729952090490929265, 633141621466333184]:
                await ctx.send(":warning: Command group restricted to bot owners")
                return
            
            if not guild:
                guild = ctx.guild.id

            guild = int(guild)

            to_leave = self.client.get_guild(guild)

            try:
                await to_leave.leave()
                await ctx.send(f"Superuser -> Leaving guild {guild}")
            except:
                await ctx.send(f"Lol no (an error occured)")


def setup(client):
    client.add_cog(Sudo(client))
