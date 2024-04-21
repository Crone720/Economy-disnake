import disnake, random, datetime
from disnake.ext import commands
from utils.db import *
class tt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def t(self, ctx, t: disnake.Member):
        await adddb(t.id)

def setup(bot):
    bot.add_cog(tt(bot))