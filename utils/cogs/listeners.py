import disnake, datetime
from disnake.ext import commands
from utils.db import *
class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await create_db()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await adddb(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await removedb(member.id)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
                await inter.send("У вас недостаточно прав", ephemeral=True)
        if isinstance(error, commands.CommandOnCooldown):
            time = disnake.utils.format_dt(datetime.datetime.now() + datetime.timedelta(seconds=error.retry_after), 'R')
            embed = disnake.Embed(
                title='Ошибка',
                description=f'{inter.author.mention}, Вы сможете использовать эту команду '
                            f'через {time}',
                color=0x2F3136
            )
            print(error.retry_after)
            await inter.response.send_message(embed=embed, ephemeral=True)
def setup(bot):
    bot.add_cog(Listener(bot))