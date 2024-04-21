import disnake, random, datetime
from disnake.ext import commands
from utils.db import *
class TimelyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ежедневная награда")
    @commands.cooldown(1, 14400, commands.BucketType.user)
    async def timely(self, interaction: disnake.AppCommandInteraction):
        t = random.randint(50, 100)
        time = datetime.datetime.now() + datetime.timedelta(hours=4)
        MNEVIPALLEON_LEEEEEONNN = disnake.utils.format_dt(time, style="R")
        await addmoneydb(interaction.author.id, t)
        timelyembed = disnake.Embed(description=f"**Временная награда - {interaction.author.display_name}**")
        timelyembed.add_field(name=">>> Вы Забрали:", value="", inline=False)
        timelyembed.add_field("", value=f"```{t} Монет```", inline=False)
        timelyembed.set_footer(text="Возвращайтесь через 6ч")
        timelyembed.set_thumbnail(url=interaction.author.display_avatar)

        await interaction.send(embed=timelyembed)

def setup(bot):
    bot.add_cog(TimelyCommand(bot))