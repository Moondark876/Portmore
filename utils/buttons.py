import discord
from discord.ext import commands, menus
from .selects import *


class Vote(discord.ui.View):

    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        self.upvotes = 0
        self.downvotes = 0
        self.upvote_users = []
        self.downvote_users = []

    @discord.ui.button(emoji="⬆️", style=discord.ButtonStyle.green)
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

    @discord.ui.button(emoji="⬇️", style=discord.ButtonStyle.red)
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

# class Paginate(discord.ui.View, menus.MenuPages):
#     def __init__(self, source, *, delete_message_after=False):
#         super().__init__(timeout=60)
#         self._source = source
#         self.current_page = 0
#         self.ctx = None
#         self.message = None
#         self.delete_message_after = delete_message_after

#     async def start(self, ctx, *, channel=None, wait=False):
#         await self._source._prepare_once()
#         self.ctx = ctx
#         self.message = await self.send_initial_message(ctx, ctx.channel)

#     async def _get_kwargs_from_page(self, page):
#         """This method calls ListPageSource.format_page class"""
#         value = await super()._get_kwargs_from_page(page)
#         if 'view' not in value:
#             value.update({'view': self})
#         return value

#     async def interaction_check(self, interaction):
#         """Only allow the author that invoke the command to be able to use the interaction"""
#         return interaction.user == self.ctx.author

#     @discord.ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
#     async def first_page(self, interaction, button):
#         await self.show_page(0)
#         await interaction.response.defer()

#     @discord.ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
#     async def before_page(self, interaction, button):
#         await self.show_checked_page(self.current_page - 1)
#         await interaction.response.defer()

#     @discord.ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
#     async def stop_page(self, interaction, button):
#         await interaction.response.defer()
#         self.stop()
#         if self.delete_message_after:
#             await self.message.delete(delay=0)

#     @discord.ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
#     async def next_page(self, interaction, button):
#         await self.show_checked_page(self.current_page + 1)
#         await interaction.response.defer()

#     @discord.ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
#     async def last_page(self, interaction, button):
#         await self.show_page(self._source.get_max_pages() - 1)
#         await interaction.response.defer()
    
class Link(discord.ui.Button):

    def __init__(self, name, link):
        super().__init__(label=name, style=discord.ButtonStyle.link, url=link)

        
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


class HelpView(discord.ui.View):
    def __init__(self, author, bot):
        super().__init__()
        self.add_item(HelpSelect(author, bot))

# class Tracks(discord.ui.View):
#     def __init__(self, author, results):
#         super().__init__()
#         self.results = results
#         self.current_page = 0
#         self.author = author
#         self.ids = [i for i, _, _ in self.results]
#         self.button = discord.ui.Button(label="{}/{}".format(self.current_page+1, len(self.ids)))
#         self.button.disabled = True
#         self.add_item(self.button)

#     async def interaction_check(self, interaction):
#         return interaction.user == self.author

#     @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
#     async def previous_callback(self, interaction, button):
#         if self.current_page > 0:
#             self.current_page -= 1
#             self.button.label = "{}/{}".format(self.current_page+1, len(self.ids))
#             await interaction.response.edit_message(content=f"https://open.spotify.com/track/{self.ids[self.current_page]}", view=self)
#         else:
#             await interaction.response.send_message(content="You are on the first page.", ephemeral=True)
#             await interaction.response.defer()

#     @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
#     async def forward_callback(self, interaction, button):
#         if self.current_page < len(self.ids) - 1:
#             self.current_page += 1
#             self.button.label = "{}/{}".format(self.current_page+1, len(self.ids))
#             await interaction.response.edit_message(content=f"https://open.spotify.com/track/{self.ids[self.current_page]}", view=self)
#         else:
#             await interaction.response.send_message(content="You are on the last page.", ephemeral=True)
#             await interaction.response.defer()   

class Tracks(discord.ui.View):
    def __init__(self, author, results):
        super().__init__()
        self.add_item(TrackSelect(author, results))

class PreView(discord.ui.View):
    def __init__(self, author, results):
        super().__init__()
        self.add_item(PreviewSelect(author, results))