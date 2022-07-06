import discord
from discord.ext import commands
import utils

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Guidance"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.command(description="The help command.", usage="help [command]")
    async def help(self, ctx, *, entity=None):
        if not entity:
            embed = discord.Embed(title="Need Help?", description="Use `help [command]` to get help on a command, and `help [category]` to get help on a specific group of commands.", color=discord.Color.random())
            embed.set_author(name="Help", icon_url=self.bot.user.avatar.url)
            embed.set_footer(text=f"Bot made by Moondark876#4269")
            await ctx.send(embed=embed)
            return
        else:
            cog = self.bot.get_cog(entity.title())
            if cog:
                embed = discord.Embed(title=f"{cog.__cog_name__} commands", color=discord.Color.random(), description='\n'.join(f'**{i+1}| {c}**' for i, c in enumerate(cog.get_commands())))
            else:
                command = self.bot.get_command(entity.lower())
                if command:
                        embed = discord.Embed(title=f"`{command.usage}`", color=discord.Color.random(), description=command.description)
                        # embed = discord.Embed(title="No help found", color=discord.Color.red(), description="No help found for this command.")
                else:
                    await ctx.send("`Category/Command` not found.")
                    return
        await ctx.send(embed=embed)

    @commands.command(description="Gives a list of all of the categories.", usage="categories")
    async def categories(self, ctx):
        embed = discord.Embed(title="Categories", description="\n".join(f"**{i+1}| {c}**" for i, c in enumerate(self.bot.cogs)), color=discord.Color.random())
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))