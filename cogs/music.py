import discord
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")



async def setup(bot):
    await bot.add_cog(Music(bot))