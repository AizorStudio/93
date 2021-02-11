import discord
from discord.ext import commands
import os


def cog_list():
    coglist = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            name = filename.replace('.py', '')
            coglist.append(name)
    
    return coglist


class Help(commands.Cog):
    """Help Commands"""

    def __init__(self, client):
        self.client = client


    @commands.command(
        usage="<modules",
        brief="Returns all available bot modules",
    )
    async def modules(self, ctx):

        cogs = cog_list()

        cog_cap = []

        for i in cogs:
            cog_cap.append(i.capitalize())

        des = "• " + "\n• ".join(cog_cap)

        e = discord.Embed(title="ナインスリー Folders", description=des)
        e.set_footer(text="<help [module] for sub-commands & <cmd [command] for usage")

        await ctx.send(embed=e)
    

    @commands.command(
        aliases=['command', 'commands'],
        usage="<cmd [command]",
        brief="Returns information for a command",
    )
    async def cmd(self, ctx, command=None):
        if not command:
            return await ctx.send(embed=discord.Embed(description="That is not a valid command name. Try using `<modules`"))


    @commands.command(
        usage="<help [module]",
        brief="Returns a help page",
    )
    async def help(self, ctx, sub=None):

        cogs = cog_list()

        if not sub:
            e = discord.Embed(
                description=f"[http://ninethree.ga/invite](https://discord.com/oauth2/authorize?client_id=718749763859775559&permissions=8&scope=bot)"
            )
            e.add_field(name="Help commands", value="`<modules` List of all modules\n`<help [module]` for commands in a module", inline=False)
            e.add_field(name="Website", value=f"[http://ninethree.ga](http://ninethree.ga)", inline=True)
            e.add_field(name="Issues", value=f"[http://ninethree.ga/issues](https://github.com/entiddie/93/issues)", inline=True)
            e.set_thumbnail(url="https://i.imgur.com/LHEykHU.png")
            e.set_author(name="Use this link to invite me", icon_url=self.client.user.avatar_url)

            return await ctx.send(embed=e)

        if sub not in cogs:
            return await ctx.send(embed=discord.Embed(description="That is not a valid module name. Use `<help` to get a list of all available modules"))
            
        e = discord.Embed(
            title=f"Command Help for {sub}"
        )
         
        await ctx.send(embed=e)
        
        
def setup(client):
    client.add_cog(Help(client))
