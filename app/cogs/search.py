import discord
from discord.ext import commands
from youtubesearchpython import SearchVideos
import requests
import datetime
from googleapiclient.discovery import build


now = datetime.datetime.now()
now_date = now.strftime("%c")

my_api_key = ""
my_cse_id = ""


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


class Searches(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, query):
        search = SearchVideos(f"{query}", offset=1, mode="dict", max_results=1)

        search = search.result()

        await ctx.send(search['search_result'][0]['link'])


    @commands.command()
    async def urban(self, ctx, *, word):
        try:
            word_a = str(word)

            word_r = word_a.replace(" ", "+")

            url = 'http://api.urbandictionary.com/v0/define?term=' + word_r

            x = requests.get(url)

            resp = x.json()

            defin = resp['list'][0]['definition']
            ex = resp['list'][0]['example']

            a = defin.translate({ord('['): None})
            final_def = a.translate({ord(']'): None})

            b = ex.translate({ord('['): None})
            final_ex = b.translate({ord(']'): None})

            em = discord.Embed(description=f"{final_def}\n\n*{final_ex}*", color=0xb3d4ff)
            em.set_author(name=f"Urban Dictionary — {resp['list'][0]['word']}", icon_url='https://i.imgur.com/he2iV0Y.png')
            em.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=em)

        except:
            em = discord.Embed(
                description=f"No definitions founds", color=0xb3d4ff
            )

            await ctx.send(embed=em)


    @commands.command()
    async def movie(self, ctx, *, arg):
        url = "http://www.omdbapi.com/?apikey=&"
        year = ''
        params = {
            't' : arg,
            'type' : 'movie',
            'y' : year,
            'plot' : 'full'
        }
        response = requests.get(url, params=params).json()
        try:
            title = response['Title']
            year = response['Year']
            rated = response['Rated']
            released = response['Released']
            runtime = response['Runtime']
            genre = response['Genre']
            director = response['Director']
            actors = response['Actors']
            plot = response['Plot']
            language = response['Language']
            poster = response['Poster']
            imdb_ratings = response['imdbRating']
            production = response['Production']

            embed = discord.Embed(
                title = f'Movie Search — {title}', 
                color = 0xffcc99
            )    

            embed.set_thumbnail(url = poster)

            embed.add_field(name = ':page_with_curl: Title', value = title, inline = False)
            embed.add_field(name = ':grey_question: Rated', value = rated, inline = False)
            embed.add_field(name = ':calendar_spiral: Year', value = year, inline = False)
            embed.add_field(name = ':calendar: Released', value = released, inline = False)
            embed.add_field(name = ':triangular_flag_on_post: Genre', value = genre, inline = False)
            embed.add_field(name = ':clock1030: Runtime', value = runtime, inline = False)
            embed.add_field(name = ':mega: Director', value = director, inline = False)
            embed.add_field(name = ':person_curly_hair: Actors', value = actors, inline = False)
            embed.add_field(name = ':page_with_curl: Synopsis', value = plot, inline = False)
            embed.add_field(name = ':speech_left: Languages', value = language, inline = False)
            embed.add_field(name = ':star: IMdB ratings', value = imdb_ratings, inline = False)
            embed.add_field(name = ':mega: Production', value = production, inline = False)
            await ctx.send(embed = embed)
        
        except:
            await ctx.send(f"No results found"


    @commands.command()
    async def google(self, ctx, *, query=None):

        if not query:
            return await ctx.send("You didn't tell me what to search for")

        try:
            result = google_search(query, my_api_key, my_cse_id)

            res = result['items'][0]

            e = discord.Embed(
                color=0x7a7a7a,
                title=f"{res['title']}",
                url=f"{res['link']}",
                description=f"{res['snippet']}"
            )

            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)

        except:
            em = discord.Embed(description=f"An error occured", color=0x7a7a7a)
            await ctx.send(embed=em)
            
    
    @commands.command(aliases=['dict', 'dictionary'])
    async def define(self, ctx, *, word=None):
        if not word:
            await ctx.send("You didn't tell me what to define")
            return

        word_n = str(word).replace(' ', '+')

        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word_n

        r = requests.request('GET', url).json()

        if 'title' in r:
            await ctx.send(f"I couldn't find a relevant definition on the (unofficial) Google Dictionary API")
            return

        defi = r[0]['meanings'][0]['definitions'][0]['definition']
        part = r[0]['meanings'][0]['partOfSpeech']
        text = r[0]['phonetics'][0]['text']
        pronunciation = r[0]['phonetics'][0]['audio']

        e = discord.Embed(
            color=0xfcfcfc,
            description=f"""
{text} {part}: {defi}

[Pronunciation]({pronunciation})
"""
        )

        e.set_author(name=f"Definition for '{word}' - {ctx.author}", icon_url='https://i.imgur.com/SdZP9sF.png')
        
        await ctx.send(embed=e)
        

def setup(client):
    client.add_cog(Searches(client))
