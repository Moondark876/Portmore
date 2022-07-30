import discord
from discord.ext import commands
import utils
import random
import time as t
import datetime
from discord import app_commands
import typing
import re
import urllib.parse
from easy_pil import Editor, load_image_async
import io
import PIL
from functools import partial
from bs4 import BeautifulSoup

start_time = t.time()


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = "Miscellaneous"
        self.ctx_menu = app_commands.ContextMenu(name="Preview", callback=self.preview)
        self.bot.tree.add_command(self.ctx_menu)

    async def get_avatar(self, user: typing.Union[discord.User, discord.Member]) -> bytes:

        # generally an avatar will be 1024x1024, but we shouldn't rely on this
        avatar_url = user.avatar.url

        async with self.bot.session.get(avatar_url) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        return avatar_bytes

    async def get_site_content(self, link):
        hdr = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.107 Mobile Safari/537.36'}
        async with self.bot.session.get(link, headers=hdr) as resp:
            text = await resp.read()
        return text

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple) -> io.BytesIO:

        # we must use BytesIO to load the image here as PIL expects a stream instead of
        # just raw bytes.
        with PIL.Image.open(io.BytesIO(avatar_bytes)) as im:

            # this creates a new image the same size as the user's avatar, with the
            # background colour being the user's colour.
            with PIL.Image.new("RGBA", im.size, colour) as background:

                # this ensures that the user's avatar lacks an alpha channel, as we're
                # going to be substituting our own here.
                rgb_avatar = im.convert("RGBA")

                # this is the mask image we will be using to create the circle cutout
                # effect on the avatar.
                with PIL.Image.new("L", im.size, 0) as mask:

                    # ImageDraw lets us draw on the image, in this instance, we will be
                    # using it to draw a white circle on the mask image.
                    mask_draw = PIL.ImageDraw.Draw(mask)

                    # draw the white circle from 0, 0 to the bottom right corner of the image
                    mask_draw.ellipse([(0, 0), im.size], fill=255)

                    # paste the alpha-less avatar on the background using the new circle mask
                    # we just created.
                    background.paste(rgb_avatar, (0, 0), mask=mask)

                # prepare the stream to save this image into
                final_buffer = io.BytesIO()

                # save into the stream, using png format.
                background.save(final_buffer, "png")

        # seek back to the start of the stream
        final_buffer.seek(0)

        return final_buffer


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.command(description="Displays a random hello message", usage="hello")
    async def hello(self, ctx):
        hello = [f"Yo Fam how ya do {ctx.author.mention}", "k", "...", "sup nerd", "ㅤ"]
        await ctx.send(random.choice(hello))

    @commands.command(description="Displays the bot's invite link.", usage="invite")
    async def invite(self, ctx):
        embed = discord.Embed(title="Add mi right now enuh", color=discord.Color.green(),
        url="https://discord.com/api/oauth2/authorize?client_id=991016696322097196&permissions=8&scope=bot%20applications.commands")
        view = discord.ui.View()
        view.add_item(utils.Link(name="Invite mi yute.", link="https://discord.com/api/oauth2/authorize?client_id=991016696322097196&permissions=8&scope=bot%20applications.commands"))
        view.add_item(utils.Link(name="Pree di website", link="https://Moondark876.github.io/Portmore/"))
        await ctx.send(embed=embed, view=view)

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

    @app_commands.command(description="Shows the avatar of a user.")
    async def avatar(self, interaction, member: discord.Member = None):
        embed = discord.Embed(title=f"Avatar", color=discord.Color.green())
        if member is None:
            member = interaction.user

        member_colour = (255, 255, 255, 0)

        # grab the user's avatar as bytes
        avatar_bytes = await self.get_avatar(member)

        # create partial function so we don't have to stack the args in run_in_executor
        fn = partial(self.processing, avatar_bytes, member_colour)

        # runs our processing in an executor, stopping it from blocking the thread loop
        # as we already seeked back the buffer in the other thread, we good
        final_buffer = await self.bot.loop.run_in_executor(None, fn)

        file = discord.File(filename="circle.png", fp=final_buffer)

        embed.set_image(url=f"attachment://{file.filename}")
        
        await interaction.response.send_message(file=file, embed=embed)

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

    async def preview(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(thinking=True)
        urls = [i.endswith('/') and i or i+'/' for i in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)]
        results = []
        embed = discord.Embed(title=urls[0])
        async with self.bot.session.get(f"https://shot.screenshotapi.net/screenshot?token={utils.SCREENSHOT_KEY}&url={urllib.parse.quote_plus(urls[0])}&full_page=true&fresh=true&output=json&file_type=png&wait_for_event=load") as resp:
            data = await resp.json()
            embed.set_image(url=data['screenshot'])
            results.append([data['screenshot'], data['url']])
        if len(urls) > 1:
            async with self.bot.session.get(f"https://shot.screenshotapi.net/screenshot?token={utils.SCREENSHOT_KEY}&url={urllib.parse.quote_plus(urls[1])}&full_page=true&fresh=true&output=json&file_type=png&wait_for_event=load") as resp:
                data = await resp.json()
                results.append([data['screenshot'], data['url']])
        await interaction.followup.send(embed=embed, view=len(urls) > 1 and None or utils.PreView(interaction.user, results))

    @commands.command(name="lmgtfy", description="Returns a link to a google search for the given query.", usage="lmgtfy [query]")
    async def lmgtfy(self, ctx, *, query: str = None):
        if query is None:
            await ctx.send("Please provide a query.")
            return
        await ctx.send(f"https://letmegooglethat.com/?q={urllib.parse.quote_plus(query)}")

    # @commands.command(name="would you rather", aliases=['wyr'], description="Returns a random question for the would you rather game.", usage="would you rather [question]")
    # async def would_you_rather(self, ctx):
    #     async with self.bot.session.get("http://either.io/0/") as resp:
    #         soup = BeautifulSoup(await resp.text(), 'html.parser')
    #         tag = soup.find_all('div', id_='question')
    #         print([t.prettify() for t in tag])


    @suggest.error
    async def suggest_error(self, interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(title="Wow wow bro, yuh sound thirsty man", color=discord.Color.red(), description=f"This command is on cooldown.")
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
    