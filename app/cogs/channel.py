import discord
from discord.ext import commands
import random


class Channels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cs'])
    async def channelstats(self, ctx):
        """
        Sends a nice fancy embed with some channel stats
        !channelstats
        """
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**", color=0xa3cbff, description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}")
        embed.add_field(name="Channel Guild", value=ctx.guild.name)
        embed.add_field(name="Channel Id", value=channel.id)
        embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}")
        embed.add_field(name="Channel Position", value=channel.position)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay)
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw())
        embed.add_field(name="Channel is news?", value=channel.is_news())
        embed.add_field(name="Channel Creation Time", value=channel.created_at)
        embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced)
        embed.add_field(name="Channel Hash", value=hash(channel))

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def createcategory(self, ctx, role: discord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Created new category: {category.name} ")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, role: discord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        await ctx.send(f"Created new channel: {channel.name}")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def deletecategory(self, ctx, category: discord.CategoryChannel, *, reason=None):
        await category.delete(reason=reason)
        await ctx.send(f"Deleted category: {category.name}")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"Deleted channel: {channel.name}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        try:

            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await channel.edit(overwrites=overwrites)
                await ctx.send(f"I have put `{channel.name}` on lockdown.")
            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(f"I have put `{channel.name}` on lockdown.")
            else:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(f"I have removed `{channel.name}` from lockdown.")

        except:
            await ctx.send("Couldn't lock channel, not enough permissions")


def setup(client):
    client.add_cog(Channels(client))
