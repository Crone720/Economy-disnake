import disnake, aiosqlite
from disnake.ext import commands
class TransferCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Передача монет другому участнику",
    )
    async def transfer(
        self,
        interaction: disnake.AppCommandInteraction,
        member: disnake.Member,
        coins: int
    ):
        if member.bot:
            await interaction.send("Вы не можете взаимодействовать с ботами!", ephemeral=True)
            return

        sender_id = interaction.author.id
        receiver_id = member.id

        async with aiosqlite.connect('economy.db') as conn:
            cursor = await conn.cursor()

            await cursor.execute("SELECT money FROM eco WHERE memberid=?", (sender_id,))
            sender_coins = (await cursor.fetchone() or [0])[0]

            if coins > sender_coins:
                embed = disnake.Embed(
                    title="Перевод Монет",
                    description="У вас недостаточно монет для перевода",
                )
                embed.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            commission = int(coins * 0.05)
            coins_after_commission = coins - commission

            await cursor.execute("UPDATE eco SET money = money - ? WHERE memberid=?", (coins, sender_id))
            await cursor.execute("INSERT OR IGNORE INTO eco (memberid) VALUES (?)", (receiver_id,))
            await cursor.execute("UPDATE eco SET money = money + ? WHERE memberid=?", (coins_after_commission, receiver_id))

            await conn.commit()

        transfer_embed = disnake.Embed(
            title="Перевод Монет",
            description=f"Вы успешно перевели {coins} <:coin:1207748043445637220>  {member.mention}. "
                        f"Комиссия в размере {commission} монет была удержана банке."
        )
        transfer_embed.set_thumbnail(url=member.display_avatar)
        await interaction.send(embed=transfer_embed)


def setup(bot):
    bot.add_cog(TransferCommand(bot))