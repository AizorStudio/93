import discord
from discord.ext import commands
from jikanpy import Jikan
from jikanpy.exceptions import APIException
import requests
from bs4 import BeautifulSoup
import nhentai


jikan = Jikan()


class Animanga(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def anime(self, ctx, *args):
        try:
            query = " ".join(args)
            try:
                mid = jikan.search("anime", query).get("results")[0].get("mal_id")
            except APIException:
                await ctx.send("Error connecting to service, try again with a different name")
            if mid:
                anime = jikan.anime(mid)
                atitle = anime.get("title")
                japanese = anime.get("title_japanese")
                typ = anime.get("type")
                duration = anime.get("duration")
                synopsis = anime.get("synopsis")
                if len(synopsis) > 1500:
                    synopsis = synopsis[:1500] + "..."
                source = anime.get("source")
                status = anime.get("status")
                episodes = anime.get("episodes")
                score = anime.get("score")
                rating = anime.get("rating")
                genre_lst = anime.get("genres")
                genres = ""
                for genre in genre_lst:
                    genres += genre.get("name") + ", "
                studios = ""
                studio_lst = anime.get("studios")
                for studio in studio_lst:
                    studios += studio.get("name") + ", "
                duration = anime.get("duration")
                premiered = anime.get("premiered")
                image_url = anime.get("image_url")
            else:
                await ctx.send("No results found!")
            embed = discord.Embed(
                title=atitle + f" ({japanese})",
                description=synopsis, color=0xffb3fc

            )
            embed.set_footer(text='MyAnimeList.net ID: {}'.format(str(mid)))
            embed.set_thumbnail(url=image_url)
            embed.add_field(name='**:grey_question: Type | Rating**', value=str(typ) + ' | ' + str(rating), inline=False)
            embed.add_field(name='**:bookmark_tabs: Source**', value=source, inline=False)
            embed.add_field(name='**:mega: Status**', value=status, inline=False)
            embed.add_field(name='**:triangular_flag_on_post: Genres**', value=genres, inline=False)
            embed.add_field(name='**:tv: Episodes**', value=str(episodes), inline=False)
            embed.add_field(name='**:star: Score**', value=score, inline=False)
            embed.add_field(name='**:microphone2: Studio(s)**', value=studios, inline=False)
            embed.add_field(name='**:calendar_spiral: Premiered**', value=premiered, inline=False)
            embed.add_field(name='**:clock4: Duration**', value=duration, inline=False)
            embed.add_field(name=':link: MyAnimeList Link', value='https://myanimelist.net/anime/' + str(mid), inline=False)

            await ctx.send(embed=embed)

        except:
            await ctx.send(f"No results found, try with a diffferent name!")


    @commands.command()
    async def manga(self, ctx, *args):
        query = " ".join(args)
        try:
            try:
                mid = jikan.search("manga", query).get("results")[0].get("mal_id")
            except APIException:
                await ctx.send("Error connecting to service, try again with a different name")
            if mid:
                manga = jikan.manga(mid)
                typ = manga.get("type")
                score = manga.get("score")
                mtitle = manga.get("title")
                chapters = manga.get("chapters")
                status = manga.get("status")
                volumes = manga.get("volumes")
                japanese = manga.get("title_japanese")
                synopsis = manga.get("synopsis")
                if len(synopsis) > 2000:
                    synopsis = synopsis[:2000] + "..."
                image = manga.get("image_url")
                genre_lst = manga.get("genres")
                genres = ""
                for genre in genre_lst:
                    genres += genre.get("name") + ", "
            else:
                await ctx.send("No results found!")
            embed = discord.Embed(
                title=mtitle + f" ({japanese})",
                description=synopsis,
                color=0xbfb3ff
            )
            embed.set_footer(text='MyAnimeList.net ID: {}'.format(str(mid)))
            embed.set_thumbnail(url=image)
            embed.add_field(name='**:grey_question: Type:**', value=typ, inline=False)
            embed.add_field(name='**:mega: Status:**', value=status, inline=False)
            embed.add_field(name='**:triangular_flag_on_post: Genres:**', value=genres, inline=False)
            embed.add_field(name='**:star: Score:**', value=score, inline=False)
            embed.add_field(name='**:bookmark_tabs: Volumes | Chapters:**', value=str(volumes) + ' @ ' + str(chapters),
                            inline=False)
            embed.add_field(name=':link: MyAnimeList Link', value='https://myanimelist.net/manga/' + str(mid), inline=False)

            await ctx.send(embed=embed)

        except:
            await ctx.send(f"No results found, try with a diffferent name!")


    @commands.command()
    async def character(self, ctx, *args):
        query = " ".join(args)
        try:
            try:
                mid = jikan.search("character", query).get("results")[0].get("mal_id")
            except APIException:
                await ctx.send("Character not found, try again with a different name")
            if mid:
                char = jikan.character(mid)
                english = char.get("name")
                japanese = char.get("name_kanji")
                about = char.get("about")
                about = about.replace("\n", " ")
                if len(about) > 2000:
                    about = about[:2000] + "..."
                img_url = char.get("image_url")
            else:
                await ctx.send("No results found!")
            embed = discord.Embed(
                title=english + f" ({japanese})",
                description=about,
                color=0xb3d4ff
            )
            embed.set_footer(text='MyAnimeList.net ID: {}'.format(str(mid)))
            embed.set_thumbnail(url=img_url)
            embed.add_field(name=':link: MyAnimeList Link', value='https://myanimelist.net/character/' + str(mid), inline=False)

            await ctx.send(embed=embed)

        except:
            await ctx.send(f"No results found, try with a diffferent name!")


    @commands.command()
    async def upcoming(self, ctx):
        up = jikan.season_later()
        animu = up.get("anime")
        embed = discord.Embed(
            title='Upcoming Anime',
            color=0xb4ffb3
        )
        ct = 0
        for animes in animu:
            ct += 1
            embed.add_field(name=f'{animes.get("title")}', value=animes.get("url"), inline=False)
            if ct > 20:
                break
        embed.set_footer(text='MyAnimeList.net')
        await ctx.send(embed=embed)

# Ctrl-K + Ctrl+C to comment and to un-comment Ctrl-K + Ctrl-U 
    @commands.command()
    async def sauce(self, ctx, arg):
        if ctx.channel.is_nsfw():
            try:
                URL = f"https://nhentai.net/g/{arg}"
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find('h1', class_="title").text
                doujin = nhentai.get_doujin(arg)
                url = doujin[0].url
                doujinTags = doujin.__dict__
                englishTitle = doujinTags['titles']['english']
                japaneseTitle = doujinTags['titles']['japanese']
                if japaneseTitle == '':
                    japaneseTitle = '\u200b'
                else:
                    pass

                if englishTitle == '':
                    englishTitle = '\u200b'
                else:
                    pass

                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=title, url=URL
                )
                tagList = []
                for tag2 in doujinTags['tags']:
                    tagList.append(tag2[2])

                def listToString(s):
                    str1 = ", "
                    return (str1.join(s))

                embed.add_field(name="Title-Eng", value=f"{englishTitle}\n", inline=True)
                embed.add_field(name="Title-Jap", value=f"{japaneseTitle}\n", inline=True)
                embed.add_field(name="Tags", value=f"```{listToString(tagList)}```", inline=False)
                embed.set_thumbnail(url=url)
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)
            except AttributeError:
                embed2 = discord.Embed(
                    colour=discord.Colour.red(),
                    description="No matches found"
                )
                await ctx.send(embed=embed2)
        else:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="This is not a NSFW channel!"
            )
            await ctx.send(embed=embed)


    @commands.command()
    async def randsauce(self, ctx):
        if ctx.channel.is_nsfw():
            arg = nhentai.get_random_id()
            URL = f"https://nhentai.net/g/{arg}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find('h1', class_="title").text
            doujin = nhentai.get_doujin(arg)
            url = doujin[0].url
            doujinTags = doujin.__dict__
            englishTitle = doujinTags['titles']['english']
            japaneseTitle = doujinTags['titles']['japanese']
            if japaneseTitle == '':
                japaneseTitle = '\u200b'
            else:
                pass

            if englishTitle == '':
                englishTitle = '\u200b'
            else:
                pass

            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=title, url=URL
            )
            tagList = []
            for tag2 in doujinTags['tags']:
                tagList.append(tag2[2])

            def listToString(s):
                str1 = ", "
                return (str1.join(s))

            embed.add_field(name="Title-Eng", value=f"{englishTitle}\n", inline=True)
            embed.add_field(name="Title-Jap", value=f"{japaneseTitle}\n", inline=True)
            embed.add_field(name="Tags", value=f"```{listToString(tagList)}```", inline=False)
            embed.add_field(name = 'Sauce', value = f"``{arg}``")
            embed.set_thumbnail(url=url)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="This is not a NSFW channel!"
            )
            await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Animanga(client))
