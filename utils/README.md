This is the utils library for the "Portmore" discord bot. It contains various utility functions that are used by the bot.

> [Dependencies](requirements.txt)

If you are using this library in your project, you will need to install the dependencies listed in the `requirements.txt` file.

However, if you plan to use this library in your project, you will have to modify the source code to suit your own bot and server.


The library can be used as easily as follows:
    
```py
import utils
from discord.ext import commands

client = commands.Bot(command_prefix = '!', case_insensitive = True)

@client.command(name="time", help="Returns the current time", aliases=["time"])
async def time(ctx: commands.Context) -> None:
    await ctx.send("Here's the time!", view=utils.Link("https://time.is/"))

client.run(token)
```


