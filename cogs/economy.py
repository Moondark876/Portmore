import discord
from discord.ext import commands
from utils import cluster
import random
from utils import Confirm


async def open_account(user: discord.Member):
    try:
        post = {"_id": str(user.id), "Balance": 0}
        await cluster.Botswag.Accounts.insert_one(post)
    except:
        pass


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        await open_account(ctx.author)
        stats = await cluster.Botswag.Accounts.find_one({"_id": str(ctx.author.id)})
        embed = discord.Embed(description=f"You currently have ${stats['Balance']}.",
                              color=discord.Color.green())
        embed.set_author(name=f"{ctx.author.name.title()}'s Balance:", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['swaggy', 'swagger'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def swag(self, ctx):
        await open_account(ctx.author)

        swagger = ["Your fans give you $* for being a swag master.",
                   "You swagged so hard you forgot to breathe, and they paid you $* to stay alive.",
                   "When you step into the building, everybody's hands go up and stay there, and you take the "
                   "opportunity to rob them all of a collective $*."]
        money = random.randint(100, 500)

        await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)}, {"$inc": {"Balance": money}})
        embed = discord.Embed(description=random.choice(swagger).replace('*', str(money)),
                              color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                         icon_url='https://cdn.discordapp.com/avatars/748609140896694394'
                                  '/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
        await ctx.send(embed=embed)

    @commands.command(aliases=["lend", "send"])
    async def give(self, ctx, user: discord.Member, amount):
        view = Confirm()
        embed = discord.Embed(title='Are you sure?',
                              description=f'Are you sure you want to give **{user.name}** your money?',
                              color=discord.Color.green())
        msg = await ctx.send(embed=embed, view=view)
        await view.wait()
        await msg.delete()
        if view.value is None:
            view.stop()
        elif view.value:
            await open_account(ctx.author)
            await open_account(user)

            stats = await cluster.Botswag.Accounts.find_one({"_id": str(ctx.author.id)})

            if not amount.isnumeric() and amount.lower() not in ["all", 'half']:
                embed = discord.Embed(title="Invalid `amount` Argument Given",
                                      description="Your `amount` argument is unrecognised.",
                                      color=discord.Color.red())
                embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
                embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                                 icon_url='https://cdn.discordapp.com/avatars/748609140896694394'
                                          '/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
                await ctx.send(embed=embed)
                return

            elif amount.isnumeric():
                if int(amount) > stats['Balance'] or int(amount) <= 0:
                    embed = discord.Embed(title="Invalid `amount` Argument Given",
                                          description="Your `amount` argument is either above your balance, "
                                                      "0 or below 0.",
                                          color=discord.Color.red())
                    embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
                    embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                                     icon_url='https://cdn.discordapp.com/avatars/748609140896694394'
                                              '/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
                    await ctx.send(embed=embed)
                    return
                else:
                    amount = int(amount)
                    await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)},
                                                              {"$inc": {"Balance": -amount}})
                    await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})

            elif not amount.isnumeric():
                if amount.lower() == 'all':
                    amount = stats['Balance']
                    await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)},
                                                              {"$inc": {"Balance": -amount}})
                    await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})
                elif amount.lower() == 'half':
                    amount = stats['Balance'] // 2
                    await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)},
                                                              {"$inc": {"Balance": -amount}})
                    await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})

            embed = discord.Embed(title="Sharing is Caring",
                                  description=f"You gave **{user.name}** ${amount}!",
                                  color=discord.Color.green())
            embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
            embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                             icon_url='https://cdn.discordapp.com/avatars/748609140896694394'
                                      '/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
            await ctx.send(embed=embed)
        else:
            pass

    @swag.error
    async def swag_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"Wow wow bro, yuh sound thirsty man", description=f"This command is on cooldown. It will be ready <t:{int(int(ctx.message.created_at.timestamp()) + error.retry_after)}:R>.",
                               color=discord.Color.red())
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=error.retry_after)


async def setup(bot):
    await bot.add_cog(Economy(bot))