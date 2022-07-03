import discord
from discord.ext import commands

# class cooldownError(commands.CommandOnCooldown):
#     """Raised when a command is on cooldown."""
#     def __init__(self, cooldown, retry_after):
#     super().__init__(cooldown, retry_after)
#     embed = discord.Embed(title=f"Wow wow bro, yuh sound thirsty man", description=f"This command is on cooldown. It will be ready <t:{int(int(ctx.message.created_at.timestamp()) + error.retry_after)}:R>.",
#                                color=discord.Color.red())
#     msg = await ctx.send(embed=embed)
#     await msg.delete(delay=error.retry_after)