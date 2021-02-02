import discord
from discord.ext import commands
import requests
import json
import praw
import random
import aiohttp
import datetime
import asyncio
import requests
from requests import get
import json
from json import loads
from bs4 import BeautifulSoup


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joke(self, ctx):
        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': "3538e1cd82mshd4a0fa5710bb64ap1693c0jsn20c8189a8a7d"
        }

        response = requests.request("GET", url, headers=headers).json()

        em = discord.Embed(colour=0x99afff, description=f"{response['content']}")

        await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def showerthought(self, ctx):
        reddit = praw.Reddit(client_id = "D3_kdqla6zxekw",
        client_secret = "E5iQm1WvPLNUEyMy9TfYUPAWewE",
        username = "SK_47DEstROyeR42069",
        password = "uncrackablepassword",
        user_agent = "pythonpraw")
        sub = reddit.subreddit("showerthoughts")
        hot = sub.hot(limit = 50)
        posts = []
        for subs in hot:
            posts.append(subs)
        rand_post = random.choice(posts)
        name = rand_post.title 

        embed = discord.Embed(
           color = 0xfffff
        )
        embed.add_field(name = "Shower thoughts :star: :shower: ", value = name)
        await ctx.send(embed = embed)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def trivia(self, ctx):

        urls = ["https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple", "https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple"]

        url = random.choice(urls)

        response = requests.request("GET", url).json()

        results = response['results'][0]

        correct = str(results['correct_answer'])
        correct = correct.replace("&quot;", "'")
        incorrect_a = str(results['incorrect_answers'][0])
        incorrect_a = incorrect_a.replace("&quot;", "'")
        incorrect_b = str(results['incorrect_answers'][1])
        incorrect_b = incorrect_b.replace("&quot;", "'")
        incorrect_c = str(results['incorrect_answers'][2])
        incorrect_c = incorrect_c.replace("&quot;", "'")

        options = [correct, incorrect_a, incorrect_b, incorrect_c]

        shuffled = random.sample(options, len(options))

        category = results['category']
        diff = str(results['difficulty'])
        diff = diff.capitalize()
        ques = str(results['question'])
        ques = ques.replace("&quot;", "'")
        ques = ques.replace("&#039;", "'")

        desc = f"<:1382_dot:772666700117573652> a) {shuffled[0]}\n<:1382_dot:772666700117573652> b) {shuffled[1]}\n<:1382_dot:772666700117573652> c) {shuffled[2]}\n<:1382_dot:772666700117573652> d) {shuffled[3]}"

        em = discord.Embed(title=f":question: {ctx.author.display_name}'s trivia question", description=f"{ques}\n\n{desc}\n\nType your choice (a, b, c or d)\n", color=0xf6ff75)

        em.add_field(name="Category", value=f"{category}")
        em.add_field(name="Difficulty", value=f"{diff}")
        em.set_footer(text="You have 20 seconds to answer")

        await ctx.send(embed=em)

        try:
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
            choice = str(ida.content)
            choice = choice.lower()

            if choice == "a":
                chosen = shuffled[0]

            elif choice == "b":
                chosen = shuffled[1]

            elif choice == "c":
                chosen = shuffled[2]

            elif choice == "d":
                chosen = shuffled[3]

            else:
                chosen = "dummy"

            yup = ['You got it!', 'Correct!', 'Yup, you got it', "That's right!"]
            nope = ["That's not right!", "Nope!", "Bruh,", "Oops!"]

            if chosen == correct:
                await ctx.send(f"✅ {random.choice(yup)}")
            else:
                await ctx.send(f"❌ {random.choice(nope)} It was: **{correct}**")

        except asyncio.TimeoutError:
            await ctx.send(f":clock10: Too slow! Your time is up. The answer was: **{correct}**")


    @commands.command(aliases=['anitrivia', 'anitriv'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def animetrivia(self, ctx):

        url = "https://opentdb.com/api.php?amount=1&category=31&type=multiple"

        response = requests.request("GET", url).json()

        results = response['results'][0]

        correct = str(results['correct_answer'])
        correct = correct.replace("&quot;", "'")
        incorrect_a = str(results['incorrect_answers'][0])
        incorrect_a = incorrect_a.replace("&quot;", "'")
        incorrect_b = str(results['incorrect_answers'][1])
        incorrect_b = incorrect_b.replace("&quot;", "'")
        incorrect_c = str(results['incorrect_answers'][2])
        incorrect_c = incorrect_c.replace("&quot;", "'")

        options = [correct, incorrect_a, incorrect_b, incorrect_c]

        shuffled = random.sample(options, len(options))

        category = results['category']
        diff = str(results['difficulty'])
        diff = diff.capitalize()
        ques = str(results['question'])
        ques = ques.replace("&quot;", "'")
        ques = ques.replace("&#039;", "'")

        desc = f"<:1382_dot:772666700117573652> a) {shuffled[0]}\n<:1382_dot:772666700117573652> b) {shuffled[1]}\n<:1382_dot:772666700117573652> c) {shuffled[2]}\n<:1382_dot:772666700117573652> d) {shuffled[3]}"

        em = discord.Embed(title=f":cherry_blossom: {ctx.author.display_name}'s trivia question", description=f"{ques}\n\n{desc}\n\nType your choice (a, b, c or d)\n", color=0xfbc7ff)

        em.add_field(name="Category", value=f"{category}")
        em.add_field(name="Difficulty", value=f"{diff}")
        em.set_footer(text="You have 20 seconds to answer")

        await ctx.send(embed=em)

        try:
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
            choice = str(ida.content)
            choice = choice.lower()

            if choice == "a":
                chosen = shuffled[0]

            elif choice == "b":
                chosen = shuffled[1]

            elif choice == "c":
                chosen = shuffled[2]

            elif choice == "d":
                chosen = shuffled[3]

            else:
                chosen = "dummy"

            yup = ['You got it!', 'Correct!', 'Yup, you got it', "That's right!"]
            nope = ["That's not right!", "Nope!", "Bruh,", "Oops!"]

            if chosen == correct:
                await ctx.send(f"✅ {random.choice(yup)}")
            else:
                await ctx.send(f"❌ {random.choice(nope)} It was: **{correct}**")

        except asyncio.TimeoutError:
            await ctx.send(f":clock10: Too slow! Your time is up. The answer was: **{correct}**")


    @commands.command(aliases=['8ball'])
    async def eball(self, ctx, *, question):
        responses = ['Absolutely.',
                    'Definitely not.',
                    'It is certain.',
                    'Not at all.',
                    'My sources say no',
                    'Not sure',
                    'Yeah',
                    'Very doubtful',
                    "Don't count on it",
                    'Outlook not so good',
                    'Most likely',
                    'Without a doubt',
                    "That's for sure",
                    'As I see it, yes',
                    'Yup',
                    'Yeah lol',
                    "Lmao yeah",
                    'Why not',
                    "Yes, but actually no.",
                    "Yes and no.",
                    "No",
                    "Nah",
                    "Sure",
                    ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    

    @commands.command()
    async def rps(self, ctx, arg=None):

        if not arg:
            await ctx.send(f"You didn't tell me what you chose, valid choices: `rock`, `paper`, `scissors`")
            return

        rpschoice = [
            "rock",
            "paper",
            "scissors",
        ]

        if arg not in rpschoice:
            await ctx.send(f"Invalid choice, valid choices: `rock`, `paper`, `scissors`")
            return

        choicebot = random.choice(rpschoice)

        if choicebot == "rock":
            emoji = "<:rock:783941279771262986>"
        elif choicebot == "paper":
            emoji = "<:paper:783941281285799958>"
        else:
            emoji = "<:scissors:783941282019934219>"

        if arg == "rock":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
        elif arg == "paper":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
        elif arg == "scissors":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie!")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def trump(self, ctx, member: discord.Member = None):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://api.whatdoestrumpthink.com/api/v1/quotes") as r:
                    data = await r.json()

                    trump_response_p = data['messages']['personalized']
                    trump_response_n = data['messages']["non_personalized"]

                    if member == None:
                        await ctx.send(f"Trump: {random.choice(trump_response_n)}")

                    else:
                        await ctx.send(f"Trump thinks {member.mention} {random.choice(trump_response_p)}")


    @commands.command(aliases=['meme', 'dankmemes'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def memes(self, ctx):
        url = f"https://api.ksoft.si/images/rand-reddit/dankmemes"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
        }

        para = {
            'remove_nsfw': True,
            'span': 'day',
        }

        response = requests.request("GET", url, headers=headers, params=para).json()

        try:
            em = discord.Embed(title=f"{response['title']}", url=f"{response['source']}", color=discord.Colour.gold()

                            )

            em.set_image(url=f"{response['image_url']}")

            em.set_footer(text=f"{response['upvotes']} 👍 ・ {response['author']}")

            await ctx.send(embed=em)

        except:
            embed = discord.Embed(
                description=f"**{ctx.author}** an error occured",
                color=0xff0000)
            await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def aww(self, ctx):
        url = "https://api.ksoft.si/images/random-aww"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
        }

        response = requests.request("GET", url, headers=headers)

        im = response.json()

        em = discord.Embed(title=f"{im['title']}", colour=discord.Colour.gold())
        em.set_image(url=f"{im['image_url']}")
        em.set_footer(text=f"{im['upvotes']} Upvotes ・ {im['author']}")

        await ctx.send(embed=em)

        
    @commands.command()
    async def wikihow(self, ctx):
        url = f"https://api.ksoft.si/images/random-wikihow"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
            'nsfw': 'False'
        }

        response = requests.request("GET", url, headers=headers)

        im = response.json()

        em = discord.Embed(title=f"How to {im['title']}", url=f"{im['article_url']}", colour=discord.Colour.gold())
        em.set_image(url=f"{im['url']}")

        await ctx.send(embed=em)


    @commands.command(aliases=['reddit', 'sr'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def sreddit(self, ctx, sub):
        url = f"https://api.ksoft.si/images/rand-reddit/{sub}"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
        }

        para = {
            'remove_nsfw': True,
            'span': 'day',
        }

        response = requests.request("GET", url, headers=headers, params=para).json()

        try:
            em = discord.Embed(title=f"{response['title']}", url=f"{response['source']}", color=0xfcccff

                            )

            em.set_image(url=f"{response['image_url']}")

            em.set_footer(text=f"{response['upvotes']} 👍 ・ {response['author']}")

            await ctx.send(embed=em)

        except:
            embed = discord.Embed(
                description=f"**{ctx.author}** Unable to get posts, make sure the subreddit exists and it isn't NSFW",
                color=0xff0000)
            await ctx.send(embed=embed)


    @commands.command(aliases=['kitty', 'meow', 'kitten'])
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Here's a cat! :cat:", color=0xb3d4ff)
                    embed.set_image(url=data['file'])

                    await ctx.send(embed=embed)


    @commands.command(aliases=['puppy', 'doggo', 'bark'])
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Here's a dog! :dog:", color=0xb3d4ff)
                    embed.set_image(url=data['url'])

                    await ctx.send(embed=embed)


    @commands.command()
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Fox :fox:", color=0xb3d4ff)
                    embed.set_image(url=data['image'])

                    await ctx.send(embed=embed)


    @commands.command(aliases=['chucknorris', 'norris'])
    async def chuck(self, ctx):
        url = 'https://api.chucknorris.io/jokes/random'

        x = requests.get(url)

        resp = x.json()

        embed = discord.Embed(description=f"{resp['value']}", color=0xffee00)

        await ctx.send(embed=embed)


    @commands.command()
    async def fml(self, ctx):
        url = "https://api.alexflipnote.dev/fml"

        head = {
            'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
        }

        r = requests.request('GET', url, headers=head).json()

        await ctx.send(f"{r['text']}")


    @commands.command()
    async def supreme(self, ctx, *, text):
        text = text.replace(" ", "+")

        url = f"https://api.alexflipnote.dev/supreme?text={text}"

        try:

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('supreme.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")


            file = discord.File("supreme.png", filename="supreme.png")
            await ctx.send(f"{ctx.author.mention}", file=file)

        except:
            await ctx.send(f"Wasn't able to create that, usually happens when the APIs are down. Try again later")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def supremedark(self, ctx, *, text):
        text = text.replace(" ", "+")

        url = f"https://api.alexflipnote.dev/supreme?text={text}&dark=true"

        head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

        r = requests.request('GET', url, headers=head)

        if r.status_code == 200:
            with open('supreme.png', 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        else:
            await ctx.send(":warning: Maintainance")


        file = discord.File("supreme.png", filename="supreme.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def supremelight(self, ctx, *, text):
        text = text.replace(" ", "+")

        url = f"https://api.alexflipnote.dev/supreme?text={text}&light=true"

        head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

        r = requests.request('GET', url, headers=head)

        if r.status_code == 200:
            with open('supreme.png', 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        else:
            await ctx.send(":warning: Maintainance")


        file = discord.File("supreme.png", filename="supreme.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    async def floor(self, ctx, member: discord.Member, *text):
        try:
            text = " ".join(text)

            pic = member.avatar_url

            x = f"https://api.alexflipnote.dev/floor?image={pic}&text={text}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', x, headers=head)

            if r.status_code == 200:
                with open('floor.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")


            file = discord.File("floor.png", filename="floor.png")
            await ctx.send(f"{ctx.author.mention}", file=file)

        except:
            await ctx.send(f"Usage: <floor (tag user) (text)")

    @commands.command()
    async def iss(self, ctx):
        url = 'http://api.open-notify.org/iss-now.json'

        x = requests.get(url)

        resp = x.json()

        time_iss = resp['timestamp']

        time_iss_c = datetime.datetime.fromtimestamp(int(time_iss)).strftime('%Y-%m-%d %H:%M:%S')

        embed = discord.Embed(title=f":earth_africa: International Space Station Location", color=0xffffff)

        embed.add_field(name=f"Longitude: {resp['iss_position']['longitude']}",
                        value=f"**Latitude: {resp['iss_position']['latitude']}**")

        embed.set_footer(text=f"Updated: {time_iss_c} | api.open-notify.org")

        await ctx.send(embed=embed)
        
        
    @commands.command()
    async def irc(self, ctx):
        url = "http://bash.org/?random1"
        page = requests.get(url)
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            q = soup.find('p', class_='qt').text
            await ctx.send(f"```{q}\n\nbash.org```")
        except:
            await ctx.send("API error")
            
            
    @commands.command(aliases=['neverhaveiever'])
    async def nhie(self, ctx):
        url = "https://never-have-i-ever-online.com/"
    
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            quote = soup.find('span', id='ajaxQuestion').text
    
            em = discord.Embed(
                color=0xd6d6d6,
                description=f"Never have I ever {quote}"
            )
    
            await ctx.send(embed=em)
    
        except:
            await ctx.send("API error")
      

    @commands.command(aliases=['simp'])
    async def simprate(self, ctx, member: discord.Member = None):
        eighty = [
            'YOOOOOOOO',
            'Shit bro',
            'Calm down',
            'Lmao simp',
            'STOP RIGHT THERE',
            'UNACCEPTABLE',
            'Chill dude',
            'S I M P'
        ]

        fifty = [
            'Damn simp',
            'Stop',
            'Bruh simp',
            'Understandable',
        ]

        twenty = [
            'Still less',
            'Lol simp',
            'Kid',
        ]

        zero = [
            'Pass',
            'Ok',
            'Cool',
            "You're cool",
        ]

        perc = random.randrange(0, 101)
        if member == None:
            if perc >= 80:
                embed = discord.Embed(description=f"{ctx.author.mention} is **{perc}%** simp ― {random.choice(eighty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 50:
                embed = discord.Embed(description=f"{ctx.author.mention} is **{perc}%** simp ― {random.choice(fifty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 20:
                embed = discord.Embed(description=f"{ctx.author.mention} is **{perc}%** simp ― {random.choice(twenty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 0:
                embed = discord.Embed(description=f"{ctx.author.mention} is **{perc}%** simp ― {random.choice(zero)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

        else:
            if perc >= 80:
                embed = discord.Embed(description=f"{member.mention} is **{perc}%** simp ― {random.choice(eighty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 50:
                embed = discord.Embed(description=f"{member.mention} is **{perc}%** simp ― {random.choice(fifty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 20:
                embed = discord.Embed(description=f"{member.mention} is **{perc}%** simp ― {random.choice(twenty)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)

            elif perc >= 0:
                embed = discord.Embed(description=f"{member.mention} is **{perc}%** simp ― {random.choice(zero)}",
                                    color=0xb3d4ff)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
