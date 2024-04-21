import disnake
from disnake.ext import commands
from utils.db import *

class RoleCreateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def role(self, interaction: disnake.AppCommandInteraction, t: str):
        role = await interaction.guild.create_role(name=t)
        await addroledb(interaction.guild.id, role.id)
        await interaction.send("ок")

def setup(bot):
    bot.add_cog(RoleCreateCommand(bot))