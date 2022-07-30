import discord 

class HelpSelect(discord.ui.Select):
    def __init__(self, author, bot):
        self.author = author
        self.bot = bot
        cogs = [c for c in self.bot.cogs.keys()]
        options = [discord.SelectOption(label=cog,
                                        description=f"{str(cog.lower())} commands",
                                        value=f"{cog.title()}") for cog in cogs]
        super().__init__(placeholder='Select a category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            embed = discord.Embed(title="Yuh look dunce.", description="This is not yours.", color=discord.Colour.random())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title=f"{self.values[0]} Commands", color=discord.Colour.random(), description="\n".join(f"**{command}**" for command in self.bot.get_cog(self.values[0]).get_commands()))
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.edit_message(embed=embed)

class TrackSelect(discord.ui.Select):
    def __init__(self, author, results):
        self.author = author
        options = [discord.SelectOption(label=name,
                                        description=artist,
                                        value=id) for id, name, artist in results]
        super().__init__(placeholder='Select a track', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            embed = discord.Embed(title="Yuh look dunce.", description="This is not yours.", color=discord.Colour.random())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.edit_message(content=f"https://open.spotify.com/track/{self.values[0]}")


class PreviewSelect(discord.ui.Select):
    def __init__(self, author, results):
        self.author = author
        self.labels = [result[1] for result in results]
        options = [discord.SelectOption(label=result[1],
                                        value=result[0]) for result in results]
        super().__init__(placeholder='Select one of the two urls', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            embed = discord.Embed(title="Yuh look dunce.", description="This is not yours.", color=discord.Colour.random())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title=''.join([option == self.values[0] and option.label for option in self.options]), color=discord.Colour.random())
        embed.set_image(url=self.values[0])
        await interaction.response.edit_message(embed=embed)
