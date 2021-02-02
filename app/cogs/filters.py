import discord
from discord.ext import commands
import requests
import os
from PIL import Image


class Filters(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blur(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url


            url = f"https://api.alexflipnote.dev/filter/blur?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('blur.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("blur.png", filename="blur.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def magik(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url
                img = str(img)
                img = img.replace("webp", "png")
                img = img.replace("gif", "png")

            url=f"https://api.alexflipnote.dev/filter/magik?image={img}"
            
            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('magik.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("magik.png", filename="magik.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def invert(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/invert?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('invert.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("invert.png", filename="invert.png")
            await ctx.send(f"{ctx.author.mention}", file=file)

        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bw(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/b&w?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('bw.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("bw.png", filename="bw.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def deepfry(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/deepfry?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('deep.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("deep.png", filename="deep.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def sepia(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/sepia?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('sepia.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)


            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("sepia.png", filename="sepia.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pixelate(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/pixelate?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('pix.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)


            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("pix.png", filename="pix.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wide(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/wide?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('wide.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)


            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("wide.png", filename="wide.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def snow(self, ctx, member: discord.Member = None):
        try:
            if not member:
                img = ctx.message.attachments[0].url

            else:
                img = member.avatar_url

            url = f"https://api.alexflipnote.dev/filter/snow?image={img}"

            head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

            r = requests.request('GET', url, headers=head)

            if r.status_code == 200:
                with open('snow.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)


            else:
                await ctx.send(":warning: Maintainance")
                return

            file = discord.File("snow.png", filename="snow.png")
            await ctx.send(f"{ctx.author.mention}", file=file)


        except:
            await ctx.send(f"Please mention someone or attach a file")


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def salty(self, ctx, member: discord.Member = None):
        if member == None:
            a = ctx.author.avatar_url

        else:
            a = member.avatar_url

        urla = f"https://api.alexflipnote.dev/salty?image={a}"

        head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

        r = requests.request('GET', urla, headers=head)

        if r.status_code == 200:
            with open('salty.png', 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        else:
            await ctx.send(":warning: Maintainance")
            return

        file = discord.File("salty.png", filename="salty.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ship(self, ctx, membera: discord.Member, memberb: discord.Member = None):

        response = requests.get(membera.avatar_url)
        
        if not memberb:
            responsetwo = requests.get(ctx.author.avatar_url)
        else:
            responsetwo = requests.get(memberb.avatar_url)

        file = open("ship1.png", "wb")
        file.write(response.content)
        file.close()

        file = open("ship2.png", "wb")
        file.write(responsetwo.content)
        file.close()

        im1 = Image.open('ship.png')

        im2 = Image.open('ship1.png')
        im3 = Image.open('ship2.png')

        im2 = im2.resize((128, 128))
        im3 = im3.resize((128, 128))

        back_im = im1.copy()
        back_im.paste(im2, (0, 0))
        back_im.paste(im3, (256, 0))
        back_im.save('ship_final.png', quality=95)

        file = discord.File("ship_final.png", filename="ship_final.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def facts(self, ctx, *text):
        text = "+".join(text)

        urla = f"https://api.alexflipnote.dev/facts?text={text}"

        head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

        r = requests.request('GET', urla, headers=head)

        if r.status_code == 200:
            with open('facts.png', 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        else:
            await ctx.send(":warning: Maintainance")
            return

        file = discord.File("facts.png", filename="facts.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def trash(self, ctx, member: discord.Member = None):
        if member == None:
            b = ctx.author.avatar_url

        else:
            b = member.avatar_url

        a = ctx.author.avatar_url

        urla = f"https://api.alexflipnote.dev/trash?face={a}&trash={b}"

        head = {
                'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
            }

        r = requests.request('GET', urla, headers=head)

        if r.status_code == 200:
            with open('trash.png', 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        else:
            await ctx.send(":warning: Maintainance")
            return

        file = discord.File("trash.png", filename="trash.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


def setup(client):
    client.add_cog(Filters(client))
