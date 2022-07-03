import discord
from utils.button import Vote


class Suggestion(discord.ui.Modal, title='Suggestion'):

    suggestion = discord.ui.TextInput(
        label='What would you like to suggest?',
        style=discord.TextStyle.long,
        placeholder='Suggestion for the server and/or bot:'
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Suggestion", color=discord.Color.green(), description=f"```{self.suggestion.value}```")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text=f"Suggest new feature(s) for {interaction.client.user.name} or this server using -suggest!")
        embed.add_field(name="Upvotes", value=0)
        embed.add_field(name="Downvotes", value=0)
        await interaction.client.get_channel(984998259116367912).send(embed=embed, view=Vote(embed))
        await interaction.response.send_message(f"{interaction.user.mention}, see your suggestion in {interaction.client.get_channel(984998259116367912).mention}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong. Error: ```{error}```', ephemeral=True)
