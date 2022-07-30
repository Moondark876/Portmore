"""
Docstring cause yes.
"""
import discord
from discord.ext import commands
import time as t
import random
import os
import aiohttp
import motor.motor_asyncio
import asyncio
import aiofiles
import traceback
import utils

class Client(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all(), help_command=None, case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.watching, name="yuh madda"))


    async def setup_hook(self):
        print(f'Logged in as\n------\n{self.user.name}\n------')
        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                name = cog[:-3]
                try:
                    await self.load_extension(f'cogs.{name}')
                except Exception as e:
                    print(f'Failed to load cog {name}\n-----')
                    async with aiofiles.open("runtime_errors.txt", "a") as f:
                        await f.write(t.strftime("%m/%d/%Y, %I:%M") + " || " + str(e) + "\n")
        await self.tree.sync()
        ready_task = asyncio.create_task(self.ready_message())
        ready_task.add_done_callback(self.error_handler)

    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title=f"**Error:** {error}", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
           async with aiofiles.open("runtime_errors.txt", "a") as f:
                await f.write(t.strftime("%m/%d/%Y, %I:%M") + " || " + str(error) + "\n")

    async def on_message(self, message):
        global last_message
        last_message = message
        if message.author == self.user:
            return
        
        if random.randint(1, 100) == 1:
            if message.author.id in utils.blacklist:
                return
            choice = random.choice(["do you have a father?", "yuh naave nth fi do?", "yah claffy?", "lock off.", "mute.", "yuh mout cyaa lock?"])
            await message.channel.send(f"{message.author.mention} {choice}")

        if self.user in message.mentions:
            if message.author.id in utils.blacklist:
                await message.reply("yo!")
                return
            await message.reply("Doe chat to mi enuh.")

        await self.process_commands(message)

client = Client()

async def main():
    async with client:
        client.session = aiohttp.ClientSession(loop=client.loop)
        client.cluster = motor.motor_asyncio.AsyncIOMotorClient(utils.MONGOKEY)
        await client.start(utils.TOKEN)


asyncio.run(main())

