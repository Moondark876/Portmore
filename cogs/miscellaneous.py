import discord
from discord.ext import commands
import utils
import random
import time as t
import datetime
from discord import app_commands
import typing

start_time = t.time()


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Miscellaneous"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.command(description="Displays a random hello message", usage="hello")
    async def hello(self, ctx):
        hello = [f"Yo Fam how ya do {ctx.author.mention}", "k", "...", "sup nerd", "ㅤ"]
        await ctx.send(random.choice(hello))

    @commands.command(description="Displays the bot's invite link.", usage="invite")
    async def invite(self, ctx):
        embed = discord.Embed(title="Add me right now enuh", color=discord.Color.green(),
        url="https://discord.com/api/oauth2/authorize?client_id=991016696322097196&permissions=8&scope=bot%20applications.commands")
        await ctx.send(embed=embed, view=utils.Link("https://discord.com/api/oauth2/authorize?client_id=991016696322097196&permissions=8&scope=bot%20applications.commands"))

    @commands.command(description="Returns the bot's latency and uptime.", usage="ping")
    async def ping(self, ctx):
        current_time = t.time()
        difference = int(round(current_time - start_time))
        text = f"`{str(datetime.timedelta(seconds=difference)).split(':')[0]}hrs`"
        embed = discord.Embed(title='Pong likkle yute', color=discord.Color.random())
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        embed.add_field(name='Uptime', value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            pass

    @commands.command(description="Quotes a member based on a message link.", usage="quote [message link]")
    async def quote(self, ctx, *, link: str = None):
        if link is None:
            await ctx.send("Please provide a link.")
            return
        link = link.split("/")
        server_id = int(link[4])
        channel_id = int(link[5])
        msg_id = int(link[6])

        server = self.bot.get_guild(server_id)
        channel = server.get_channel(channel_id)
        message = await channel.fetch_message(msg_id)

        embed = discord.Embed(title=f"{message.author.name} said in {message.channel}:", description=message.content, color=discord.Color.blue())
        embed.set_author(name=f"{message.author}", icon_url=message.author.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}.")
        await self.bot.get_channel(985221255475130378).send(embed=embed)
        await ctx.message.delete()

    @commands.command(description="Shows the avatar of a user.", usage="avatar [user]")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(title=f"Avatar Link for {ctx.author}", color=discord.Color.green(), description=f"```{ctx.author.avatar.url}```")  
            embed.set_image(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Avatar Link for {member}", color=discord.Color.green(), description=f"```{member.avatar.url}```")
            embed.set_image(url=member.avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author}.")
            await ctx.send(embed=embed)

    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(description="Takes a suggestion for this server and/or the bot!")
    async def suggest(self, interaction):
        await interaction.response.send_modal(utils.Suggestion())

    @commands.command(description="Command with a random usage, depending on what I am testing at the time you see it.", usage="test [members] [message]")
    async def test(self, ctx, members: commands.Greedy[discord.Member] = "no one", *, message: str = "nothing"):
        if members == "no one":
            await ctx.send(f"{ctx.author.mention} you said {message} to {members}")
        else:
            await ctx.send(f"{ctx.author.mention} you said {message} to {', '.join(str(i.mention) for i in members)}")

    @suggest.error
    async def suggest_error(self, interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(title="Wow wow bro, yuh sound thirsty man", color=discord.Color.red(), description=f"This command is on cooldown.")
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Misc(bot))
    