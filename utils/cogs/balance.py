import disnake
from disnake.ext import commands
from utils.db import *
class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Посмотреть баланс")
    async def balance(self, interaction: disnake.AppCommandInteraction, member: disnake.Member=None):
        if not member:
            b = await getbalancedb(interaction.author.id)
            url = interaction.author.display_avatar
        else:
            b = await getbalancedb(member.id)
            url = member.display_avatar
        embed = disnake.Embed(title="Баланс", description=f">>> баланс {b}")
        embed.set_thumbnail(url=url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(BalanceCommand(bot))