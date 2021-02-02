import discord
from discord.ext import commands, tasks
import asyncio
import re
from copy import deepcopy
import datetime
import os
import traceback
import utils.json_loader
import discord.utils


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check
    

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['serverleave', 'guildleave', 'leaveguild'])
    @commands.has_permissions(administrator=True)
    async def leaveserver(self, ctx):
        to_leave = self.client.get_guild(ctx.guild.id)
        try:
            await ctx.send(f"Bye fags :wave:")
            await to_leave.leave()
        except:
            await ctx.send(f"Lol no (an error occured)")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):

        if member == ctx.author:
            await ctx.send("You can't use this on yourself")
            return

        if member.guild_permissions.manage_messages:
            await ctx.send("You can't use this on a moderator")
            return

        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                await ctx.send("No muted role was found! Please create one called `Muted`")
                return

            await member.add_roles(role)
            await ctx.send(f"Muted `{member.display_name}`")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")
        

    @commands.command(aliases=['xmute'])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                await ctx.send("No muted role was found! Please create one called `Muted`")
                return

            if role not in member.roles:
                await ctx.send("This member is not muted.")
                return

            await member.remove_roles(role)
            await ctx.send(f"Unmuted `{member.display_name}`")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command(aliases=['clean', 'delete', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"Deleted the last `{amount} messages`")
            await asyncio.sleep(2)
            await msg.delete()
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command(aliases=['sm', 'slowmo', 'slow'])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds):
        try:
            if seconds == "off":
                await ctx.channel.edit(slowmode_delay=0)
                em = discord.Embed(
                    description=f"Removed slowmode",
                    color=0x94abff
                )

                await ctx.send(embed=em)
            else:
                seconds_i = int(seconds)
                await ctx.channel.edit(slowmode_delay=seconds_i)
                em = discord.Embed(
                    description=f"Set slowmode to {seconds} seconds",
                    color=0x94abff
                )

                await ctx.send(embed=em)

        except:
            em = discord.Embed(
                description=f"Usage Example: `<slowmode 10` or `<slowmode off`\nDuration needs to be more than 1 second and lesser than 10,000 seconds", color=0xff0000
            )

            await ctx.send(embed=em)



    @commands.command(aliases=['purgebots'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def pbots(self, ctx, max_messages: int = 50):
        try:
            if max_messages > 5000:
                await ctx.send("Too many messages (<= 5000)")
                return
            deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: m.author.bot)
            if len(deleted) == 0:
                x = await ctx.send(":warning: No messages found by bots within `{0}` searched messages!".format(max_messages))
            else:
                x = await ctx.send(f"Purge complete")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")



    @commands.command(aliases=['purgeusers', 'puser'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def pusers(self, ctx, member: discord.Member, max_messages: int = 50):
        try:
            if max_messages > 5000:
                await ctx.send("Too many messages (<= 5000)")
                return
            deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: m.author == member)
            if len(deleted) == 0:
                x = await ctx.send(":warning: No messages found by user within `{0}` searched messages!".format(max_messages))
            else:
                x = await ctx.send(f"Purge complete")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command(aliases=['purgeimages'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def pimages(self, ctx, max_messages: int = 50):
        try:
            if max_messages > 5000:
                await ctx.send("Too many messages (<= 5000)")
                return
            deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.attachments) or len(m.embeds))
            if len(deleted) == 0:
                x = await ctx.send(":warning: No messages found containing images within `{0}` searched messages!".format(max_messages))
            else:
                x = await ctx.send(f"Purge complete")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command(aliases=['purgeembeds'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def pembeds(self, ctx, max_messages: int = 50):
        try:
            if max_messages > 5000:
                await ctx.send("Too many messages (<= 5000)")
                return
            deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.embeds))
            if len(deleted) == 0:
                x = await ctx.send(":warning: No messages found containing embeds within `{0}` searched messages!".format(max_messages))
            else:
                x = await ctx.send(f"Purge complete")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command(aliases=['purgeattach', 'purgeattachments'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def pattach(self, ctx, max_messages: int = 50):
        try:
            if max_messages > 5000:
                await ctx.send("Too many messages (<= 5000)")
                return
            deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.attachments))
            if len(deleted) == 0:
                x = await ctx.send(":warning: No messages found containing attachments within `{0}` searched messages!".format(max_messages))
            else:
                x = await ctx.send(f"Purge complete")
        except:
            await ctx.send(f"I wasn't able to do that, check my permissions")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason="Unspecified"):

        if member.guild_permissions.manage_messages:
            await ctx.send("You can't use this on a moderator")
            return

        if not member:
            await ctx.send("Specify a member to ban")
            return

        if member == ctx.author:
            await ctx.send("You cannot ban yourself")
            return

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                description=f"{member.mention} was banned\nReason: {reason}",
                color=0xff0000)
            await ctx.send(embed=embed)

        except:
            await ctx.send("Lacking permissions")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason="Unspecified"):

        if member.guild_permissions.manage_messages:
            await ctx.send("You can't use this on a moderator")
            return

        if not member:
            await ctx.send("Specify a member to kick")
            return

        if member == ctx.author:
            await ctx.send("You cannot kick yourself")
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description=f"{member.mention} was kicked\nReason: {reason}",
                color=0xff0000)
            await ctx.send(embed=embed)

        except:
            await ctx.send("Lacking permissions")
    

    @commands.command(aliases=['unban'])
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def xban(self, ctx, id: int):
        if not id:
            embed = discord.Embed(
                description=f"**{ctx.author}** Please specify a User ID",
                color=0xff0000)
            return await ctx.send(embed=embed)

        try:
            user = await self.client.fetch_user(id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                description=f"{user.mention} was unbanned",
                color=0xff0000)
            return await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                description=f"**{ctx.author}** No permission to unban the member",
                color=0xff0000)
            return await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                description=f"**{ctx.author}** Error: Banned user not found",
                color=0xff0000)
            return await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, message):

        if member == ctx.author:
            await ctx.send("You can't use this on yourself")
            return

        if member.guild_permissions.manage_messages:
            await ctx.send("You can't use this on a moderator")
            return

        if len(message) > 750:
            await ctx.send(f"Keep the warning under 750 characters!")
            return
        em = discord.Embed(description=f"{message}")
        em.set_author(name=f"You were warned on {ctx.guild.name}", icon_url=ctx.guild.icon_url)

        try:
            await member.send(embed=em)
        except:
            await ctx.send(f"I wasn't able to warn this member, they likely aren't accepting PM")
            return

        em = discord.Embed(description=f"{message}")
        em.set_author(name=f"{member.display_name} has been warned", icon_url=member.avatar_url)

        await ctx.send(embed=em)

    
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, args):
        try:
            await member.edit(nick=args)
            await ctx.send(f"Changed nickname for {member.mention} to {args}")
        except:
            await ctx.send(f"No permissions to change member's nick. Try moving my role over their top role")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, existing_channel: discord.TextChannel):
        try:
            if existing_channel is not None:
                await existing_channel.clone(reason="Has been nuked")
                await existing_channel.delete()
                await ctx.send(f"Nuked the channel (deleted and re-added)")
            else:
                await ctx.send(f'Could not find this text channel')
        except:
            await ctx.send(f"Could not find this text channel / No permissions")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def msg(self, ctx, member: discord.Member):
        em = discord.Embed(description=f"Enter the message you would like to send", color=0xf0f0f0)
        em.set_author(name=f"Messaging {member}", icon_url=ctx.author.avatar_url)
        em.set_footer(text="There is a 5 minute timeout for this")
        await ctx.send(embed=em)
        ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
        id = str(ida.content)
        sending = id.lower()

        em = discord.Embed(description=f"Would you like to send this message anonymously? — (The receiver will not know who the sender is)\n\nReply with **yes** or **no**", color=0xf0f0f0)
        em.set_author(name=f"Anonymity Settings for {member}'s message", icon_url=ctx.author.avatar_url)
        em.set_footer(text="There is a 2 minute timeout for this")
        await ctx.send(embed=em)
        ida = await self.client.wait_for('message', check=check(ctx.author), timeout=120)
        id = str(ida.content)
        id = id.lower()

        if id == "yes" or id == "y":
            sender = "Anonymously sent"
        elif id == "no" or id == "n":
            sender = f"{ctx.author}"
        else:
            await ctx.send("Incorrectly provided! Try again.")
            return

        em = discord.Embed(description=f"{sending}", color=0xf0f0f0)
        em.set_author(name=f"New message from {ctx.guild.name} — {sender}", icon_url=ctx.guild.icon_url)
        try:
            await member.send(embed=em)
            await ctx.send(f"Sent the message to {member}")
        except:
            await ctx.send(f"{ctx.author.mention} I was unable to send the message to {member}, likely because the person is only accepting messages from friends.")

    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            self.client.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.client.unload_extension(f"cogs.{ext[:-3]}")
                        self.client.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
