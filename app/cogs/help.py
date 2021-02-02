import discord
from discord.ext import commands


class Helpnew(commands.Cog):

    def __init__(self, client):
        self.client = client
        
        
    @commands.command()
    async def about(self, ctx):
        e = discord.Embed(color=0xfcfcfc,
            description="""
Created by [Aizor Studio](https://www.instagram.com/aizorstudio/)'s bot developers. Written in Python, using discord.py library

Report Issues: [Support server](https://discord.gg/kS9yP26BBH)
"""
        )

        e.set_author(name="93, Discord Bot for Moderation and Utility", icon_url=self.client.user.avatar_url)

        await ctx.send(embed=e)


    @commands.command(aliases=['module'])
    async def modules(self, ctx):

        em = discord.Embed(
            title="ナインスリー Folders",
            color=0xfcfcfc,
            description="""
• Basic
• Moderation
• Memory
• Animanga
• Search
• Utility
• Economy
• Games
• Fun
• Misc
"""

        )

        em.set_footer(text="<help 'module' to get sub-commands and usage")

        await ctx.send(embed=em)


    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                color=0xfafafa, description=f"[http://ninethree.ga/invite](https://discord.com/oauth2/authorize?client_id=718749763859775559&permissions=8&scope=bot)"
            )
            em.add_field(name="Help commands", value="`<modules` List of all modules\n`<help [module]` for commands in a module", inline=False)
            em.add_field(name="Website", value=f"[http://ninethree.ga](http://ninethree.ga)", inline=True)
            em.add_field(name="Issues", value=f"[http://ninethree.ga/issues](https://github.com/entiddie/93/issues)", inline=True)
            em.set_thumbnail(url="https://i.imgur.com/LHEykHU.png")
            em.set_author(name="Use this link to invite me", icon_url=self.client.user.avatar_url)

            await ctx.send(embed=em)


    @help.command(aliases=['Basic'])
    async def basic(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Basic Commands",
                color=0xfcfcfc,
                description="""
`ping` - Gives you my latency
`hello` - Greetings
`repeat` - Make me repeat 
`help` - Help page
`cmd` - Help for specific commands
`invite` - Invite me to your server
`about` - About me and my developers
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)

    @help.command(aliases=['Moderation'])
    async def moderation(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Moderation Commands",
                color=0xfcfcfc,
                description="""
`nuke`- Deletes and clones a channel
`mute` - Mute a user
`unmute` - Unmute a user
`warn` - Warn a user
`clear` - Clear an amount of message
`slowmode` - Activates slowmode 
`purge` - Purge commands
`ban` - Ban a user
`kick` - Kick a user
`xban` - Unban a user
`channelstats` - Details about the channel
`lockdown` - Changes permissions so people can no longer type
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


    @help.command(aliases=['Memory'])
    async def memory(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Memory Commands",
                color=0xfcfcfc,
                description="""
`tag` - Creates tags that can contain any kind of data, call out the tag and the bot responds accordingly
`createtag` - Creates a new tag
`updatetag` - Update an existing tag
`deletetag` - Deletes an existing tag
`alltags` - Sends you a list of all your tags

`afk` - Sets AFK for you while you're away, with an optional message you want to give to others when they mention you

`profile` - Set a profile for you and others to see. Add connections, and other information
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)

    
    @help.command(aliases=['Misc'])
    async def misc(self, ctx, page=1):
        if ctx.invoked_subcommand is None:
            if page == 1:
                em = discord.Embed(
                    title="Miscellaneous Commands",
                    color=0xfcfcfc,
                    description="""
`slap` - Slap someone
`spank` - Spank em'
`kill` - Kill em'
`worthless` - You're worthless
`salty` - Salty people
`ship` - Ship people
`facts` - Facts
`trash` - Complete garbage
`supreme` - Cool text
`hug` - Give someone a nice hug
`wave` - Wave to the chat
"""

                )

                em.set_footer(text="<help to go to main embed, <help misc [Page] • Page 1/3")

                await ctx.send(embed=em)

            if page == 2:
                em = discord.Embed(
                    title="Miscellaneous Commands",
                    color=0xfcfcfc,
                    description="""
`supreme` - Cool text
`floor` - The floor is-
`blur` - Blur out an image
`magik` - Magik magik
`invert` - Invert colours
`bw` - Black & White
`deepfry` - Completety ruin the image
`sepia` - Sepia filter
`pixelate` - Pixelation
`pat` - Head pat
`punch` - Punch in the face
`coffee` - Hot Coffee
`kiss` - Kiss someone
"""

                )

                em.set_footer(text="<help to go to main embed, <help misc [Page] • Page 2/3")

                await ctx.send(embed=em)
            
            if page == 3:
                em = discord.Embed(
                    title="Miscellaneous Commands",
                    color=0xfcfcfc,
                    description="""
`wide` - Makes people look fat?
`snow` - Snow filter
`joke` - Make me tell you lame jokes
`showerthought` - Shower thoughts
`8ball` - Makes me answer yes/no questions
`motivate` - Motivational stuff
`chucknorris` - Chuck Norris facts
`iss` - ISS location (useless)
`memes` - Fresh memes from reddit
`aww` - Cute pictures from reddit
`reddit` - Random images from provided subreddit
`cat` - Random cat images
`dog` - Random dog images
`fox` - Random fox images
"""

                )

                em.set_footer(text="<help to go to main embed, <help misc [Page] • Page 3/3")

                await ctx.send(embed=em)


    @help.command(aliases=['Animanga'])
    async def animanga(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Animanga Commands",
                color=0xfcfcfc,
                description="""
`anime` - Search for an anime
`manga` - Search for some manga
`character` - Search for a character
`upcoming` - List of upcoming anime
`sauce` - Sauce
`randsauce` - Random sauce
`animetrivia` - Trivia but for weebs
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


    @help.command(aliases=['Search'])
    async def search(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Search Commands",
                color=0xfcfcfc,
                description="""
`yt` - Search YouTube
`google` - Search the internet
`multisearch` - Same as Google, but gives 3 instead of 1 result
`urban` - Urban Dictionary Search
`define` - Defines a word
`gif` - GIF search
`movie` - Search for a movie
`reddit` - Get random images from provided subreddit
`lyrics` - Get lyrics for a song
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


    @help.command(aliases=['Utility'])
    async def utility(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Utility Commands",
                color=0xfcfcfc,
                description="""
`expand` - Expand a custom emote
`avy` - Get avatar for a user
`color` - Color preview
`serverinfo` - Server information
`userinfo` - User information
`roleinfo` - Role information
`channelstats` - Channel Info
`archive` - Archive messages to provided limit
`cleanme` - Delete your own messages and get an archive
`weather` - Weather for provided location
`timer` - Set a timer
`choose` - Make me choose
`remind` - Set a reminder
`flip` - Flip a coin!
`poll` - Post a poll
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


    @help.command(aliases=['Economy'])
    async def economy(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Economy Commands",
                color=0xfcfcfc,
                description="""
`balance` - Shows you your, or another members balance
`beg` - Beg Harder
`timely` - Get a timely reward, this can be claimed once every 3 hours
`work` - Get money by working
`crime` - Commit a crime, gain big or lose big
`withdraw` - Withdraw an amount from your bank
`deposit` - Deposit an amount to your bank
`leaderboard` - Shows the global leaderboard
`send` - Send someone an amount
`bflip` - Bet flip, flip a coin and guess what face it is
`broll` - Bet roll, roll the wheel and multiply the amount you bet
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


    @help.command(aliases=['games', 'Game'])
    async def game(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Game Utility Commands",
                color=0xfcfcfc,
                description="""
`osu` - OSU! commands
`minecraft` - Minecraft commands
`overwatch` - Overwatch commands
`game` - Game search
`pokedex` - Pokemon Search
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)
            
            
    @help.command()
    async def nsfw(self, ctx):
        em = discord.Embed(
            color=0x919191,
            description="""
`hentaigif` - hentai gifs
`neko` - neko pics
`lesbian` - lesbian shit
`boobs` - boobs
`hentai` - hentai
`lewdk` - lewd
`pussy` - pussy
`yuri` - yuri
`lewd` - more lewd
`anal` - anal
`waifu` - waifu (not really nsfw)
`tits` - tiddies

"""
        )

        await ctx.send(embed=em)


    @help.command(aliases=['Fun'])
    async def fun(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Fun Commands",
                color=0xfcfcfc,
                description="""
`irc` - IRC quotes from bash.org
`nhie` - Never have I ever
`owoify` - OwOify text
`memegen` - Meme maker
`trivia` - Random trivia questions
`fml` - F*ck my life
`rps` - Rock, paper, scissors
"""

            )

            em.set_footer(text="<help to go to main embed, <modules for all modules")

            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Helpnew(client))