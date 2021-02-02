import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio



uri = "\"

cluster = MongoClient(uri)
db = cluster["93"]
col = db["tags"]


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group()
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:

            em = discord.Embed(
                color=0xfffafa, description="""
`<profile view [user/none]` - View user's profile
`<profile set` - Setup profile 
`<profile delete` - Reset your profile
`<profile connect [service name] [account name] [link (optional)]` - Add a connection
`<profile xconnect` - Remove a connection
`<profile follow [user]` - Follow a user
`<cookie [user]` - Send cookies
""" 
            )

            em.set_author(name="Profile Commands", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=em)




    @profile.command()
    async def view(self, ctx, member: discord.Member = None):
        if ctx.invoked_subcommand is None:
            if not member:
                member = ctx.author
                userid = str(ctx.author.id)
            else:
                member = member
                userid = str(member.id)

            if col.count({'userid': userid}) == 0:
                await ctx.send(f"{member.display_name} has not set their profile yet.")

            else:
                results = col.find({"userid": userid})

                for result in results:
                    note = result['note']
                    follower_ = result["followers"]
                    rep_ = result['reputation']
                    del result['_id']
                    del result['userid']
                    del result['note']
                    del result['followers']
                    del result['reputation']

                em = discord.Embed(description=f"{note}", color=0xfffafa)
                em.set_author(name=f"Viewing {member.display_name}'s profile", icon_url=member.avatar_url)
                em.set_thumbnail(url=member.avatar_url)

                for i in result:
                    value = result[i]
                    em.add_field(name=f"{i.capitalize()}", value=value)
                try:
                    em.set_footer(text = f"Followers: {follower_[0]} ｜ Cookies: {rep_}")
                except:
                    em.set_footer(text=f"Followers: {follower_} ｜ Cookies: {rep_}")

                await ctx.send(embed=em)


    @profile.command()
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)

            if col.count({'userid': userid}) != 0:
                await ctx.send("You have already set up your profile, try <updateprofile if you want to update something")

            else:
                post = {"userid": userid, "followers" : [0], "reputation": 0}
                col.insert_one(post)

                await ctx.send(f"Ok, let's get your profile set up. I will ask you questions, answer them accordingly. You can abort anytime, just type 'cancel'")

                await asyncio.sleep(2)

                await ctx.send(f"What is your real name/nickname? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    name = id  # first input
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"Nickname": name}}

                    col.update_one(myquery, newvalues)

                await ctx.send(f"What is your age? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    try:
                        age = int(id)  # second input
                        myquery = {"userid": userid}
                        newvalues = {"$set": {"age": age}}

                        col.update_one(myquery, newvalues)

                    except:
                        await ctx.send(f"Age has to be a number")

                await ctx.send(f"Nationality? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    nationality = id
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"nationality": nationality}}

                    col.update_one(myquery, newvalues)

                await ctx.send(f"Birthday? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    bday = id
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"Birthday": bday}}

                    col.update_one(myquery, newvalues)

                await ctx.send(f"Add a description/note to your profile")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                note = id

                if len(note) > 250:
                    await ctx.send(f"Note has to be shorter than 250 characters.")
                    return
                
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return

                myquery = {"userid": userid}
                newvalues = {"$set": {"note": note}}

                col.update_one(myquery, newvalues)

                await ctx.send(f"Profile Basics Complete, to connect/add a social account, use `<profile connect`")


    @profile.command(aliases=['dprofile'])
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:

            userid = str(ctx.author.id)

            await ctx.send(f"Are you sure you want to delete your profile? (This action cannot be reversed)")
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
            id = str(ida.content)

            if id.lower() == "yes":
                myquery = { "userid": userid }

                col.delete_one(myquery)

                await ctx.send(f"You profile was deleted.")
            else:
                await ctx.send(f"Action cancelled")
            

    @profile.command()
    async def connect(self, ctx, service = None, username = None, link = None):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)
            results = col.find({"userid" : userid})
            for result in results:
                del result['_id']
                del result["userid"]
                try:
                    del result["colour"]
                except:
                    pass
                length = len(result)
            if col.count({"userid" : userid}) != 0:
                try:
                    if length < 12:
                        if service != None and username != None:
                            if link == None:
                                myquery = {"userid": userid}
                                newvalues = {"$set": {service: username}}

                                col.update_one(myquery, newvalues)
                            else:
                                myquery = {"userid": userid}
                                newvalues = {"$set": {service: f"[{username}]({link})"}}

                                col.update_one(myquery, newvalues)

                            await ctx.send(f"Added your connection\nYou can add {12 - length} more connections")
                        else:
                            await ctx.send(f"You can add upto {12 - length} more connections")
                            await asyncio.sleep(1)
                            await ctx.send('Write it in as `"<profile connect <service name>" "<username>" <link (optional)>` \nFor example - `Spotify <spotify username> <spotify profile link (optional)>`')
                    else:
                        await ctx.send("You cannot add more connections!")

                except:
                    await ctx.send("HMMM an error occured")

            else:
                await ctx.send("You don't have a profile currently! Try making one by typing `<profile set`")


    @profile.command()
    async def xconnect(self, ctx, *,service = None):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)
            if service != None:
                service = str(service)

                checks = col.find({"userid" : userid})
                items = []
                for check in checks:
                    for key in check:
                        items.append(key)

                if service in items:
                    col.update({'userid': userid}, {"$unset": {f"{service}": 1}}, False, True)
                    await ctx.send("Connection removed")

                else:
                    await ctx.send("I couldn't find that connection, re-check the name")

    @profile.command()
    async def follow(self, ctx, member : discord.Member = None):
        if ctx.invoked_subcommand is None:
            if member != None:
                userid = str(member.id)
                if col.count({"userid" : userid}) != 0:
                    result1 = col.find({"userid" : userid})
                    for checks in result1:
                        userCheck = checks['followers']

                        try:
                            userCheck = userCheck[1:]
                        except:
                            userCheck = []

                    if ctx.author.id in userCheck:
                        await ctx.send(f"You are already following {member.display_name}")
                    else:
                        await ctx.send(f"Do you want to follow {member.display_name}? (y/n)")
                        answer = await self.client.wait_for('message', check = check(ctx.author), timeout= 20)
                        if str(answer.content) == 'y' or str(answer.content) == 'Y':
                            results = col.find({"userid" : userid})
                            for result in results:
                                followers = result["followers"]
                            try:
                                followers += 1
                            except:
                                followers[0] += 1
                                followers = followers[0]
                            followers = [followers, ctx.author.id]

                            myquery = {"userid": userid}
                            newvalues = {"$set": {"followers": followers }}

                            col.update_one(myquery, newvalues)

                            await ctx.send(f"You are now following {member}")
                        else:
                            pass

                else:
                    await ctx.send("The user doesn't have a profile!")

            else:
                await ctx.send("Example usage: `<follow <mention user>`")


    @profile.command()
    async def followers(self, ctx, member : discord.Member = None):
        if ctx.invoked_subcommand is None:
            if member == None:
                member = ctx.author
                userid = str(ctx.author.id)
            else:
                userid = str(member.id)

            checks = col.find({"userid" : userid})

            followerUsers = []

            for check in checks:
                followers_ = check['followers']
                try:
                    users = followers_[1:]
                except:
                    users = None
                try:
                    number = followers_[0]
                except:
                    number = followers_
                followerUsers.append(users)

            em = discord.Embed(description = f"Number of followers - {number}", color=0x9e9e9e)
            em.set_author(name=f"Viewing {member.display_name}'s Followers", icon_url=member.avatar_url)
            try:
                for user in users:
                    em.add_field(name = '\u200b', value = f"<@{user}>")
            except:
                em.add_field(name='\u200b', value= "None")

            await ctx.send(embed = em)


    @commands.command(aliases = ['rep', 'reputation', 'cookies'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, member : discord.Member = None):

        if member == None:
            await ctx.send("You didn't tell me who to give the cookie to")

        else:
            userid = str(member.id)

        if member == ctx.author:
            await ctx.send("Hey, you cannot give yourself cookies")
        else:

            results = col.find({"userid" : userid})

            repList = []

            for result in results:
                try:
                    rep = result["reputation"]
                except:
                    rep = []

                repList.append(rep)
            try:
                reputation = repList[0]

                reputation += 1

                myquery = {"userid": userid}
                newvalues = {"$set": {"reputation": reputation}}

                col.update_one(myquery, newvalues)

                await ctx.send(f"**{ctx.author}** gave a cookie to **{member}**")
            except:
                await ctx.send("The mentioned user doesn't have a profile set")


def setup(client):
    client.add_cog(Profile(client))
