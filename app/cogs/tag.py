import discord
from discord.ext import commands
from pymongo import MongoClient


uri = "mongodb+srv://riju:1234@cluster0.owqch.mongodb.net/93?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["93"]
col = db["tags"]


class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tagcreate', 'ctag', 'tagc'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def createtag(self, ctx, tagname, *, tagcontent=" "):
        if len(tagcontent) > 500:
            await ctx.send(f"Tag content cannot have more than 150 characters")
        elif "@everyone" in tagcontent or "@here" in tagcontent:
            await ctx.send(f"Tags content cannot have everyone of here tags") 
        elif "@everyone" in tagname or "@here" in tagname:
            await ctx.send(f"Tags names cannot have everyone of here tags")
        else:
            try:
                img = ctx.message.attachments[0].url
                tagcontent = tagcontent + " " + img
            except:
                pass
            userid = str(ctx.author.id)
            if col.count({'userid': userid}) != 0:
                checks = col.find({'userid': userid})
                items = []
                for check in checks:
                    for key in check:
                        items.append(key)
                if tagname in items:
                    await ctx.send("Tag already exists")
                else:
                    try:
                        myquery = {"userid": userid}
                        newvalues = {"$set": {tagname: tagcontent}}

                        col.update_one(myquery, newvalues)
                        await ctx.send("Added the tag")
                    except:
                        print("An error occurred")
            else:
                try:
                    post = {"userid": userid, tagname: tagcontent}
                    col.insert_one(post)
                    await ctx.send("Created your account and added the tag")
                except:
                    await ctx.send(f"An error occured")



    @commands.command(aliases=['findtag', 'tagfind'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tag(self, ctx, *, tagname):
        userid = str(ctx.author.id)
        results = col.find({"userid": userid})

        checks = col.find({'userid': userid})
        items = []
        for check in checks:
            for key in check:
                items.append(key)
        if tagname in items:
            for result in results:
                await ctx.send(result[tagname])
        else:
            await ctx.send(f"Tag not found, try creating one. Note: tag names are case-sensitive")


    @commands.command(aliases=['tagupdate', 'tupdate', 'updatet'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def updatetag(self, ctx, argA, *, argB):
        if len(argB) > 150:
            await ctx.send(f"Tag content cannot have more than 150 characters")
        elif "@everyone" in argB or "@here" in argB:
            await ctx.send(f"Tags content cannot have everyone of here tags") 
        else:
            existingTagName = argA
            updatedTagValue = argB 
            checks = col.find({'userid' : str(ctx.author.id)})
            items = []
            for check in checks:
                for key in check:
                    items.append(key)
            if existingTagName in items:
                col.update_one({"userid" : str(ctx.author.id)}, {"$set" : {existingTagName : updatedTagValue}})
                await ctx.send("Tag updated")
            else:
                await ctx.send("That tag doesn't exist")


    @commands.command(aliases=['tdelete', 'deletet', 'tdel', 'delt'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def deletetag(self, ctx, *, arg):
        tagName = arg 
        checks = col.find({'userid' : str(ctx.author.id)})
        items = []
        for check in checks:
            for key in check:
                items.append(key)
        if tagName in items:
            col.update({'userid' : str(ctx.author.id)}, {"$unset" : {tagName : 1}}, False, True)
            await ctx.send("Tag deleted")
        else:
            await ctx.send("Tag doesn't exist")


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def alltags(self, ctx):
        async with ctx.channel.typing():

            results = col.find({"userid" : str(ctx.author.id)})

            result_ = []

            for result in results:
                for name in result:
                    result_.append(name)

            length = int(len(result_))
            description_variable = "\n".join(result_[2 : length])
            
            
            
            if len(description_variable) == 0:
                description_value = f"**{ctx.author.display_name}**, you dont have any tags. Try creating one with `<createtag`"
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
                embed.set_footer(text="To access a tag, use <tag (name). To create a new tag, use <createtag")
                try:
                    await ctx.author.send(embed = embed)
                    await ctx.send("I've sent you a list of your tags")
                except:
                    await ctx.send(f"{ctx.author.mention} I couldn't send you your tags, you likely are not accepting DMs from bots")



def setup(client):
    client.add_cog(Tags(client))
