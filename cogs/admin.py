import discord
from discord.ext import commands
from utils.button import *


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Administration"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.has_permissions(administrator=True)
    @commands.command(description="Bans a member from the server.", usage="ban [member] [reason]")
    async def ban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str=None):
        for member in members:
            await member.ban(reason=reason)
        embed = discord.Embed(title=f"Banned {', '.join(member for member in members)}", color=discord.Color.red(), description=f"Reason: {reason}")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(description="Kicks a member from the server.", usage="kick [members] [reason]")
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason: str=None):
        if members is list:
            for member in members:
                await member.kick(reason=reason)
        else:
            await members.kick(reason=reason)
        embed = discord.Embed(title=f"Kicked {members is list and ', '.join(str(member) for member in members) or members}", color=discord.Color.red(), description=f"Reason: {reason}")
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions", color=discord.Color.red(), description="You do not have the required permissions to use this command.")
            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions", description="You do not have the required permissions to use this command.", color=discord.Color.red())
            embed.set_author(name="Missing Permissions", icon_url=self.bot.user.avatar.url)
            embed.set_footer(text=f"Bot made by Moondark876#4269")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
