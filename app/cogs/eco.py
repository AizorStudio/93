import discord
from discord.ext import commands
import json 
import random


emoji = "<:93_coin:803910969834602536>"
yellow = 0xf7ff8a
gray = 0xc9c9c9


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal



class Eco(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['$', 'bal'])
    async def balance(self, ctx, member: discord.Member=None):
        await open_account(ctx.author)

        users = await get_bank_data()

        if not member:
            user = ctx.author
        else:
            user = member

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        embed = discord.Embed(
            description=f"**{user}** has {round(wallet_amt)} coins in their wallet and {round(bank_amt)} coins in the bank",
            colour=yellow)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randrange(101)

        users[str(user.id)]["wallet"] += earnings

        embed = discord.Embed(
            description=f"**{ctx.author}** You begged and got {earnings} coins. You can beg once every 15 minutes",
            color=gray)
        await ctx.send(embed=embed)

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def work(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randrange(100, 300)

        users[str(user.id)]["wallet"] += earnings

        reactions = [
            'You babysitted and got',
            'You cleaned a toilet and got',
            'You found money in your wallet',
            'You took your neightbors dog for a walk and earned',
            'You did an actual job for a change',
            'Someone just handed you over',
            'Have my money',
            'You work as YouTuber and earned',
            'You pretty much robbed a bank and got',
            'You robber your dog. You got',
            'You got expelled from your school. Have',
            'Where did this come from?',
            'You took the trash out, have',
            'You are poor, have',
        ]

        embed = discord.Embed(
            description=f"**{ctx.author}** {random.choice(reactions)} {earnings} coins",
            color=gray)
        await ctx.send(embed=embed)

        with open("mainbank.json", "w") as f:
            json.dump(users, f)


    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def crime(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randrange(100, 500)

        bank_amt = users[str(user.id)]["bank"]

        if bank_amt < 500:
            await ctx.send(f"You need to have atleast 500 coins in your bank")
            return

        idk = ['a', 'b']
        x = random.choice(idk)
        if x == "a":
            users[str(user.id)]["bank"] += earnings
            reactions = [
                'You stole your friends phone. You earned',
                'You hacked someone. You made',
                'You stole pumpkins. You made',
                'You stole credit cards. Made',
                'Kidnapping. Easy money',
                'You bullied and stole from a kid. You got',
            ]
        else:
            users[str(user.id)]["bank"] -= earnings
            reactions = [
                'Most definitely caught for stealing my cat. You lost',
                'Got caught robbing a bank. You lost',
                'The police are here. You lost',
                'You got arrested. Bailed for',
                'You were caught stealing pink phallic objects. You lost',
                "Tried stealing your mom's car. You lost that pocket money",
            ]


        embed = discord.Embed(
            description=f"**{ctx.author}** {random.choice(reactions)} {earnings} coins",
            color=gray)
        await ctx.send(embed=embed)

        with open("mainbank.json", "w") as f:
            json.dump(users, f)
            

    @commands.command(aliases=['reward', 't'])
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def timely(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings_timely = 500

        users[str(user.id)]["wallet"] += earnings_timely

        embed = discord.Embed(
            description=f"**{ctx.author}** You collected your timely reward of 500 coins. Come back after 3 hours.",
            color=yellow)
        await ctx.send(embed=embed)

        with open("mainbank.json", "w") as f:
            json.dump(users, f)


    @commands.command(aliases=['w', 'with'])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter an amount to withdraw")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("You don't have enough money")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        embed = discord.Embed(
            description=f"**{ctx.author}** You withdrew {amount} coins from your bank account",
            color=gray)
        await ctx.send(embed=embed)


    @commands.command(aliases=['d', 'dep'])
    async def deposit(self, ctx, amount: str=None):
        await open_account(ctx.author)
        users = await get_bank_data()
        wallet_amt = users[str(ctx.author.id)]["wallet"]
        if amount == None:
            await ctx.send("Please enter an amount")
            return

        if amount == "all" or amount == "All":
            amount = wallet_amt

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send("You don't have that much money")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")

        embed = discord.Embed(description=f"You deposited {amount} coins to your bank",
                              color=gray)
        await ctx.send(embed=embed)



    @commands.command(aliases=['s'])
    async def send(self, ctx, member: discord.Member=None, amount=None):
        if not member:
            return await ctx.send("No member parameter given")

        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("You don't have enough money!")
            return
        if amount < 0:
            await ctx.send("amount must be positive!")
            return

        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        embed = discord.Embed(
            description=f"**{ctx.author}** You gave **{member.mention}** {amount} coins",
            color=yellow)

        await ctx.send(embed=embed)


    @commands.command(aliases=["bflip", "betflip"])
    async def bf(self, ctx, amt: int, choice: str):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        wallet_amt = users[str(user.id)]["wallet"]

        if amt <= 0:
            await ctx.send(f"Please choose a great amount!")

        elif amt > wallet_amt:
            await ctx.send(f"You don't have enough money in your wallet!")

        else:
            ch = [
                'h', 't', ]

            bot_ch = random.choice(ch)

            if choice == "h":
                if bot_ch == "h":
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You guessed it right! You win {amt * 2} coins",
                        color=yellow,
                    )
                    embed.set_image(url='https://i.imgur.com/zCRK8FG.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, amt)

                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You lost {amt} coins better luck next time ^_^",
                        color=gray)
                    embed.set_image(url='https://i.imgur.com/eG2XLck.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, -1 * amt)

            elif choice == "t":
                if bot_ch == "t":
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You guessed it right! You win {amt * 2} coins",
                        color=yellow)
                    embed.set_image(url='https://i.imgur.com/eG2XLck.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, amt)
                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You lost {amt} coins better luck next time ^_^",
                        color=gray)
                    embed.set_image(url='https://i.imgur.com/zCRK8FG.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, -1 * amt)

            else:
                embed = discord.Embed(
                    description=f"**{ctx.author}** Usage: <bf <amt> <h/t>",
                    color=gray)
                await ctx.send(embed=embed)


    @commands.command(aliases=['br', 'betroll'])
    async def broll(self, ctx, amt: int=None):

        if not amt:
            return await ctx.send("No amount given to roll")

        ch = ['↘️', '↙️', '↖️', '↗️', '⬇️', '⬆️', '➡️', '⬅️']

        ran_ch = random.choice(ch)

        msg = f"""**[ 0.7 ] ‎  [ 1.2 ]‎  ‎ [ 1.7 ]**\n\n**[ 0.2]**   ‎ ‎‎‎ ‎ {ran_ch}  ‎‎‎‎ ‎‎‎  **[ 0.9 ]**\n\n**[ 1.2 ]  ‎  [ 0.5 ]  ‎ [ 1.3 ]**"""

        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        wallet_amt = users[str(user.id)]["wallet"]

        if amt <= 0:
            await ctx.send(f"Please choose a greater amount")

        elif amt > wallet_amt:
            await ctx.send(f"You don't have enough money in your wallet")

        else:
            amt = round(amt)
            if ran_ch == ch[0]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.3 * amt)
                winning = 1.3 * amt
            elif ran_ch == ch[1]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.2 * amt)
                winning = 1.2 * amt
            elif ran_ch == ch[2]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.7 * amt)
                winning = 0.7 * amt
            elif ran_ch == ch[3]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.7 * amt)
                winning = 1.7 * amt
            elif ran_ch == ch[4]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.5 * amt)
                winning = 0.5 * amt
            elif ran_ch == ch[5]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.2 * amt)
                winning = 1.2 * amt
            elif ran_ch == ch[6]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.9 * amt)
                winning = 0.9 * amt
            elif ran_ch == ch[7]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.2 * amt)
                winning = 0.2 * amt

            em = discord.Embed(
                title=f"{ctx.author} won {winning} coins", description=msg, color=yellow
            )

            await ctx.send(embed=em)


    @commands.command()
    async def add(self, ctx, member: discord.Member=None, amount=None):
        if ctx.message.author.id == 353416871350894592:

            if not member:
                return await ctx.send("No member parameter given")

            await open_account(member)
            if amount == None:
                await ctx.send("Please enter something!")
                return

            amount = int(amount)

            await update_bank(member, amount, "bank")

            embed = discord.Embed(
                description=f"**{ctx.author}** You added {amount} coins to **{member.mention}**'s account",
                color=gray)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"**{ctx.author}** This command can only be used by the bot owners",
                color=gray)

            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Eco(client))