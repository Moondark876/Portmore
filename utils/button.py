import discord
from discord.ext import commands


class Vote(discord.ui.View):

    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        self.upvotes = 0
        self.downvotes = 0
        self.upvote_users = []
        self.downvote_users = []

    @discord.ui.button(label="⬆️", style=discord.ButtonStyle.green)
    async def upvote_callback(self, interaction, button):
        if interaction.user.id in self.upvote_users:
            return
        elif interaction.user.id in self.downvote_users:
            self.downvote_users.remove(interaction.user.id)
            self.downvotes -= 1
        self.upvote_users.append(interaction.user.id)
        self.upvotes += 1
        self.embed.set_field_at(index=0, name="Upvotes", value=self.upvotes)
        self.embed.set_field_at(index=1, name="Downvotes", value=self.downvotes)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label="⬇️", style=discord.ButtonStyle.red)
    async def downvote_callback(self, interaction, button):
        if interaction.user.id in self.downvote_users:
            return
        elif interaction.user.id in self.upvote_users:
            self.upvote_users.remove(interaction.user.id)
            self.upvotes -= 1
        self.downvote_users.append(interaction.user.id)
        self.downvotes += 1
        self.embed.set_field_at(index=1, name="Downvotes", value=self.downvotes)
        self.embed.set_field_at(index=0, name="Upvotes", value=self.upvotes)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @commands.has_permissions(administrator=True)
    @discord.ui.button(label="End Poll", style=discord.ButtonStyle.grey)
    async def end_poll_callback(self, interaction, button):
        del self.upvote_users
        del self.downvote_users
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=self.embed, view=self)

class Paginate(discord.ui.View):

    def __init__(self, embed, info):
        super().__init__()
        self.embed = embed
        self.info = info
        self.pages = info
        self.per_page = 5
        self.page = 0

    @discord.ui.button(label=":arrow_backward:", style=discord.ButtonStyle.grey)
    async def previous_page_callback(self, interaction, button):
        if self.page == 0:
            return
        self.page -= 1
        self.embed = self.pages[self.page]
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label="End Interaction", style=discord.ButtonStyle.danger)
    async def end_interaction_callback(self, interaction, button):
        await interaction.response.delete()
        await interaction.cancel()

    @discord.ui.button(label=":arrow_forward:", style=discord.ButtonStyle.grey)
    async def next_page_callback(self, interaction, button):
        if self.page == len(self.pages) - 1:
            return
        self.page += 1
        self.embed = self.pages[self.page]
        await interaction.response.edit_message(embed=self.embed, view=self)

class Link(discord.ui.View):

    def __init__(self, link):
        super().__init__()
        self.link = link

        button = discord.ui.Button(label="Link", style=discord.ButtonStyle.link, url=self.link)
        self.add_item(button)

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title='Confirmed ✅', color=discord.Color.green())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.value = True
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title='Cancelled ❌', color=discord.Color.red())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.value = False
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

class Next(discord.ui.View):
    def __init__(self, func):
        super().__init__()
        self.func = func

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        val = await self.func()
        if isinstance(val, discord.Embed):
            await interaction.response.edit_message(embed=val)
        else:
            await interaction.response.edit_message(val)

    @discord.ui.button(label='Stop Interaction', style=discord.ButtonStyle.grey)
    async def stop_interaction_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Interaction halted.", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
