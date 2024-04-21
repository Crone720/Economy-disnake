import disnake
from disnake.ext import commands
from typing import List
from utils.db import *

class EntriesPaginator(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0
        self._update_state()

    def _update_state(self) -> None:
        self.prev_page.disabled = self.index == 0
        self.next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(label="<<", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.index -= 1
        self._update_state()
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(label=">>", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.index += 1
        self._update_state()
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="market")
    async def market(self, interaction):
        ...
    @market.sub_command(name="buy", description="Посмотреть магазин")
    async def marketbuy(self, interaction: disnake.AppCommandInteraction):
        roles = await fetch_market_role()
        
        if not roles:
            embed = disnake.Embed(description="Никто не продаёт.", color=0x2F3136)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embeds = []
            for i in range(0, len(roles), 50):
                role_info = "\n".join([f"> <@&{role[1]}>\n- Цена: {role[2]}\n" for i, role in enumerate(roles[i:i+50])])
                embed = disnake.Embed(title="Магазин", description=role_info, color=0x2F3136)
                embed.set_thumbnail(url=interaction.author.avatar.url if interaction.author.avatar else interaction.author.default_avatar.url)
                embeds.append(embed)
            await interaction.response.send_message(embed=embeds[0], view=EntriesPaginator(embeds), ephemeral=True)

def setup(bot):
    bot.add_cog(Market(bot))