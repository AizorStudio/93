import discord
from discord.ext import commands
import requests
from PIL import Image, ImageFont, ImageDraw
import random


class Img(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def worthless(self, ctx, member: discord.Member):
        response = requests.get(member.avatar_url)

        file = open("av.png", "wb")
        file.write(response.content)
        file.close()

        im1 = Image.open('worthless.jpg')
        im2 = Image.open('av.png')

        im3 = im2.resize((300, 300))

        back_im = im1.copy()
        back_im.paste(im3, (600, 340))
        back_im.save('worth.png', quality=95)

        file = discord.File("worth.png", filename="worth.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slap(self, ctx, member: discord.Member):
        response = requests.get(ctx.author.avatar_url)
        responsetwo = requests.get(member.avatar_url)

        file = open("slap1.jpg", "wb")
        file.write(response.content)
        file.close()

        file = open("slap2.jpg", "wb")
        file.write(responsetwo.content)
        file.close()

        im1 = Image.open('slap.jpg')
        im2 = Image.open('slap1.jpg')
        im3 = Image.open('slap2.jpg')

        im4 = im2.resize((200, 200))
        im5 = im3.resize((215, 215))

        back_im = im1.copy()
        back_im.paste(im4, (465, 55))
        back_im.paste(im5, (81, 465))
        back_im.save('slapfinal.png', quality=95)
        file = discord.File("slapfinal.png", filename="slapfinal.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def spank(self, ctx, member: discord.Member):
        response = requests.get(ctx.author.avatar_url)
        responsetwo = requests.get(member.avatar_url)

        file = open("spank1.jpg", "wb")
        file.write(response.content)
        file.close()

        file = open("spank2.jpg", "wb")
        file.write(responsetwo.content)
        file.close()

        im1 = Image.open('spank.jpg')
        im2 = Image.open('spank1.jpg')
        im3 = Image.open('spank2.jpg')

        im4 = im2.resize((70, 70))
        im5 = im3.resize((70, 70))

        back_im = im1.copy()
        back_im.paste(im4, (220, 60))
        back_im.paste(im5, (365, 130))
        back_im.save('spankfinal.png', quality=95)
        file = discord.File("spankfinal.png", filename="spankfinal.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command(aliases=['kill'])
    async def stab(self, ctx, membera: discord.Member):

        memberb = ctx.author

        responsea = requests.get(membera.avatar_url)
        responseb = requests.get(memberb.avatar_url)

        file = open("stab_av2.png", "wb")
        file.write(responsea.content)
        file.close()

        file = open("stab_av1.png", "wb")
        file.write(responseb.content)
        file.close()

        im1 = Image.open("stab.png")

        im2 = Image.open("stab_av1.png")
        im3 = Image.open("stab_av2.png")

        im2 = im2.resize((270, 270))
        im3 = im3.resize((220, 220))

        back_im = im1.copy()
        back_im.paste(im2, (900, 60))
        back_im.paste(im3, (20, 10))
        back_im.save('stab_final.png', quality=95)

        file = discord.File("stab_final.png", filename="stab_final.png")
        await ctx.send(f"{ctx.author.mention}", file=file)


    @commands.command()
    async def coffee(self, ctx, member: discord.Member):
        cof = [
            'https://media1.tenor.com/images/84ad0ed50036d581e174084a959ebe9f/tenor.gif?itemid=10236772',
            'http://s11.favim.com/orig/7/764/7649/76497/anime-coffee-anime-food-gif-Favim.com-7649722.gif',
            'https://pa1.narvii.com/7020/5581181c4a8892e8f4c7c5bda396bf88542d1f8cr1-500-281_00.gif',
            'https://giffiles.alphacoders.com/184/184258.gif',
            'https://cdn.discordapp.com/attachments/712551176633319469/749598599561740338/tenor_5.gif',
            'https://media.discordapp.net/attachments/712551176633319469/749598598722748536/tenor_4.gif',
        ]

        embed = discord.Embed(color=0xb3d4ff, description=f"**{member.mention}**, **{ctx.author.mention}** made you coffee!"

                            )

        embed.set_image(url=f"{random.choice(cof)}")

        await ctx.send(embed=embed)


    # Tea
    @commands.command()
    async def tea(self, ctx, member: discord.Member):
        tea = [
            'https://i.pinimg.com/originals/d8/b9/60/d8b9602aa8395a4d99c1a3a6a16118c1.gif',
            'https://cdn52.picsart.com/171700590000201.gif?to=min&r=640',
            'https://i.pinimg.com/originals/b3/02/8e/b3028e78fb16193aab522a9a4ae22591.gif',
            'https://i.gifer.com/DWYs.gif',
            'https://data.whicdn.com/images/321720066/original.gif',
        ]

        embed = discord.Embed(color=0xb3d4ff, description=f"**{member.mention}**, **{ctx.author.mention}** made you tea!"

                            )

        embed.set_image(url=f"{random.choice(tea)}")

        await ctx.send(embed=embed)


    # Kiss
    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        kisses = [
            'https://cutewallpaper.org/21/anime-kiss-on-cheek/Kiss-Anime-Gif-AS21-Jornalagora.gif',
            'https://media1.tenor.com/images/503bb007a3c84b569153dcfaaf9df46a/tenor.gif?itemid=17382412',
            'https://i.skyrock.net/5079/88775079/pics/3174561165_1_11_1IKppSSS.gif',
            'https://i.pinimg.com/originals/32/d4/f0/32d4f0642ebb373e3eb072b2b91e6064.gif',
            'https://64.media.tumblr.com/642760eca89625f5dcb7a7b0110310db/tumblr_mqy0f19TPY1rfgw56o1_400.gifv',

        ]
        
        embed = discord.Embed(color=0xb3d4ff,
                                description=f"Looks like {ctx.author.mention} gave **{member.mention}** a kiss"

                                )

        embed.set_image(url=f"{random.choice(kisses)}")

        await ctx.send(embed=embed)


    @commands.command()
    async def wave(self, ctx, member: discord.Member=None):
        waves= [
            'https://media.tenor.com/images/6870fd2f3f7be6bc6f08083a899c4889/tenor.gif',
            'https://media1.tenor.com/images/e16def45f8b0e39cfc93440517695fbd/tenor.gif?itemid=12217237',
            'https://i.pinimg.com/originals/b9/20/3a/b9203a9105c523d68ef3c8e1c4b889ca.gif',
            'https://i0.wp.com/drunkenanimeblog.com/wp-content/uploads/2018/06/anime-wave-gif.gif?resize=620%2C345&ssl=1',
            'https://image.myanimelist.net/ui/ueRS3W4eVdEzb4WVsqz9NxKLFp5nl6jHa8uiUIheMEnX_L0D76abl5COrE3_q8GWOi23wCEAYn5z3tK25lB-zKYd7m98IY7EpDbzjTccopmTjzfI9w5tfCOskaUiiKrX',
            'https://2.bp.blogspot.com/-V2q6IOsnPLk/V4P5d_ESyEI/AAAAAAAAg_o/P9pTua0vAlAdjwJa3_Tq62vdbmDAoEa3wCKgB/s1600/Omake%2BGif%2BAnime%2B-%2BLove%2BLive%2521%2BSunshine%2521%2521%2B-%2BEpisode%2B2%2B-%2BChika%2BWaves.gif',
            'https://image.myanimelist.net/ui/5LYzTBVoS196gvYvw3zjwIKkMZCvVDBrVg3ou5Xk858',
            'https://media.tenor.com/images/33ee3367675a99d39888a7ad273e0291/tenor.gif',


        ]
        
        if not member:
          embed = discord.Embed(color=0xb3d4ff,
                                description=f"{ctx.author.mention} waves :wave:"

                                )

          embed.set_image(url=f"{random.choice(waves)}")

          await ctx.send(embed=embed)
        else:
          embed = discord.Embed(color=0xb3d4ff,
                                description=f"{ctx.author.mention} waved to **{member.mention}** :wave:"

                                )

          embed.set_image(url=f"{random.choice(waves)}")

          await ctx.send(embed=embed)


    # Tea
    @commands.command()
    async def punch(self, ctx, member: discord.Member):
        punch = [
            'https://i.kym-cdn.com/photos/images/original/001/117/646/bf9.gif',
            'https://media1.tenor.com/images/31686440e805309d34e94219e4bedac1/tenor.gif?itemid=4790446',
            'https://media3.giphy.com/media/AlsIdbTgxX0LC/giphy.gif',
            'https://thumbs.gfycat.com/SecondFeminineDuckbillcat-small.gif',
            'https://media.tenor.com/images/b96f63d9382fe52cfe43feac4a8a40d6/tenor.gif',
            'https://i.kym-cdn.com/photos/images/newsfeed/001/856/131/1af.gif',
            'https://media1.tenor.com/images/51816a61dee943f4428908ecb552c922/tenor.gif?itemid=7611317',
            'https://media1.tenor.com/images/4e1c688f7666adb0f68bb4995e47e0ef/tenor.gif?itemid=16634439',
        ]

        embed = discord.Embed(color=0xb3d4ff,
                            description=f"**{member.mention}**, **{ctx.author.mention}** punched you in the face"

                            )

        embed.set_image(url=f"{random.choice(punch)}")

        await ctx.send(embed=embed)


    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        links = [
            'https://api.storage.ksoft.si/media/i-6q7n2f5c-10.gif',
            'https://api.storage.ksoft.si/media/i-az8kxtaw-71.gif',
            'https://api.storage.ksoft.si/media/i-9b7wd730-42.gif',
            'https://api.storage.ksoft.si/media/i-3p12mdha-74.gif',
            'https://api.storage.ksoft.si/media/i-1t1kv6sm-66.gif',
            'https://i.pinimg.com/originals/02/7e/0a/027e0ab608f8b84a25b2d2b1d223edec.gif',
            'https://i.pinimg.com/originals/02/7e/0a/027e0ab608f8b84a25b2d2b1d223edec.gif',
            'https://media1.tenor.com/images/7e30687977c5db417e8424979c0dfa99/tenor.gif?itemid=10522729',
            'https://cdn.lowgif.com/full/86fdce8550402b45-.gif',
            'https://steamuserimages-a.akamaihd.net/ugc/784103565766330825/3D42253804E4AC3D92DC416B306CEA572EF860A0/',
            'https://cdn.lowgif.com/medium/d6a08bbe22fee4a9-.gif',
            'https://cutewallpaper.org/21/hugs-anime/Hugs-for-everyone-3-image-Anime-Fans-of-DBolical-Indie-DB.gif',
        ]

        embed = discord.Embed(color=0xb3d4ff,
                            description=f"**{member.mention}**, **{ctx.author.mention}** gave you a hug"

                            )

        embed.set_image(url=f"{random.choice(links)}")

        await ctx.send(embed=embed)


    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        url = "https://api.ksoft.si/images/random-image"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
            'nsfw': 'False'
        }

        para = {'tag': 'pat'}

        response = requests.request("GET", url, headers=headers, params=para)

        im = response.json()

        link = im['url']

        embed = discord.Embed(color=0xb3d4ff,
                            description=f"**{member.mention}**, **{ctx.author.mention}** gave you a head pat!"

                            )

        embed.set_image(url=f"{link}")

        await ctx.send(embed=embed)


    @commands.command()
    async def fbi(self, ctx, member: discord.Member):
        url = "https://api.ksoft.si/images/random-image"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
            'nsfw': 'False'
        }

        para = {'tag': 'fbi'}

        response = requests.request("GET", url, headers=headers, params=para)

        im = response.json()

        link = im['url']

        embed = discord.Embed(color=0xb3d4ff, description=f"**{member.mention}**, **{ctx.author.mention}** called the FBI"

                            )

        embed.set_image(url=f"{link}")

        await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Img(client))