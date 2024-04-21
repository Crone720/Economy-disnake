from typing import Optional
import disnake
from disnake.ext import commands
from utils.db import *

class AwardButton(disnake.ui.View):
    def __init__(self, author, member, amm):
        self.author = author
        self.member = member
        self.amm = amm
        super().__init__(timeout=None)

    @disnake.ui.button(label="Выдать", custom_id="invest")
    async def invest(self, button: disnake.Button, interaction: disnake.Interaction):
        if interaction.author == self.author:
            await addmoneydb(self.member.id, self.amm)
            embed = disnake.Embed(title="Управление монетами", description=f"Вы успешно выдали `{self.amm}` пользователю {self.member.mention}")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.defer()
    @disnake.ui.button(label="Снять", custom_id="withdraw")
    async def witndraw(self, button: disnake.Button, interaction: disnake.Interaction):
        if interaction.author == self.author:
            b = await getbalancedb(self.member.id)
            if b < self.amm:
                return await interaction.send(f"Вы не можете снять `{self.amm}` ведь это больше баланса пользователя.", ephemeral=True)
            await removemoneydb(self.member.id, self.amm)
            embed = disnake.Embed(title="Управление монетами", description=f"Вы успешно сняли `{self.amm}` пользователю {self.member.mention}")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.defer()
class AwardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Управление монетами")
    async def award(self, interaction: disnake.AppCommandInteraction, target: disnake.Member, amount: int):
        embed = disnake.Embed(title="Управление монетами", description=f"Указаный Участник: {target.mention} Указанная сумма: {amount}")
        await interaction.response.send_message(embed=embed, view=AwardButton(interaction.author, target, amount))

def setup(bot):
    bot.add_cog(AwardCommand(bot))