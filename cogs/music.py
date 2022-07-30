import discord
from discord.ext import commands
import os
import utils


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    # helper function 
    async def get_track(self, search):
        """
        Gets the access token for spotify API
        """
        async with self.bot.session.post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'client_credentials',
        'client_id': utils.SPOTIFY_ID,
        'client_secret': utils.SPOTIFY_SECRET,
    }) as resp:
            data = await resp.json()
            access_token = data["access_token"]
            
            headers = {
                'Authorization': 'Bearer {token}'.format(token=access_token)
            }

            async with self.bot.session.get(f"https://api.spotify.com/v1/search?q={search}&type=track&limit=25", headers=headers) as resp:
                data = await resp.json()
                track_id = []
                track_name = []
                artist_name = []
                for _, track in enumerate(data['tracks']['items']):
                    track_id.append(track['id'])
                    track_name.append(track['name'])
                    artist_name.append(track['artists'][0]['name'])

                return track_id, track_name, artist_name


    @commands.command(help="Gets a spotify track by name", usage="track <name>")
    async def track(self, ctx, *, search: str):
        ids, names, artists = await self.get_track(search)
        await ctx.send(f"https://open.spotify.com/track/{ids[0]}", view=utils.Tracks(author=ctx.author, results=zip(ids, names, artists)))

    @commands.command(help="Joins the voice channel of the user", usage="join")
    async def join(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()
            embed = discord.Embed(title=":white_check_mark: Connected", description=f"Connected to {ctx.author.voice.channel.mention}", color=discord.Color.green())
        else:
            embed = discord.Embed(title=":x: Error", description="You are not in a voice channel", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(help="Disconnects the bot from the voice channel", usage="disconnect")
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            embed = discord.Embed(title=":white_check_mark: Disconnected", description="Disconnected from voice channel", color=discord.Color.green())
        else:
            embed = discord.Embed(title=":x: Error", description="I am not connected a voice channel", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.group(help="Returns the queue list", usage="queue")
    async def queue(self, ctx):
        if ctx.voice_client:
            embed = discord.Embed(title=":white_check_mark: Queue", description="\n".join(ctx.voice_client.queue), color=discord.Color.green())
        else:
            embed = discord.Embed(title=":x: Error", description="I am not connected to a voice channel", color=discord.Color.red())
        await ctx.send(embed=embed)

    queue.command(name="queue add", help="Adds a track to the queue", usage="queue add <name>")
    async def queue_add(self, ctx, *, search: str):
        if ctx.voice_client:
            ids, names, artists = await self.get_track(search)
            ctx.voice_client.queue.append(f"{names[0]} - {artists[0]}")
            embed = discord.Embed(title=":white_check_mark: Added", description=f"Added {names[0]} - {artists[0]} to the queue", color=discord.Color.green())
        else:
            embed = discord.Embed(title=":x: Error", description="I am not connected to a voice channel", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(help="Plays a track from the queue", usage="play")
    async def play(self, ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                await ctx.voice_client.stop()
            await ctx.voice_client.play()
            embed = discord.Embed(title=":white_check_mark: Playing", description=f"Now playing {ctx.voice_client.queue[0]}", color=discord.Color.green())
        else:
            embed = discord.Embed(title=":x: Error", description="I am not connected to a voice channel", color=discord.Color.red())
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Music(bot))