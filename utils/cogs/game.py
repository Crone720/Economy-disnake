import disnake
from disnake.ext import commands
import aiosqlite
import random
import asyncio

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Подбросить монетку с возможностью выигрыша")
    async def coinflip(self, interaction: disnake.AppCommandInteraction, bet: int, choice = commands.Param(name='действие', choices=['орёл','решка'])):
        user_id = interaction.author.id

        async with aiosqlite.connect('economy.db') as conn:
            cursor = await conn.cursor()

            await cursor.execute("SELECT money FROM eco WHERE memberid=?", (user_id,))
            user_coins = (await cursor.fetchone() or [0])[0]

            coins = bet

            if bet > user_coins:
                embed = disnake.Embed(
                    title="Ошибка",
                    description="У вас недостаточно монет для ставки.",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if bet <= 49:
                embed = disnake.Embed(
                    title="Ошибка",
                    description="Минимальная ставка 50 <:coin:1207748043445637220> ",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            await cursor.execute("UPDATE eco SET money = money - ? WHERE memberid=?", (coins, user_id))

            tsfembed = disnake.Embed(title="Подкидываем Монетку")
            tsfembed.set_image(url="https://i.pinimg.com/originals/78/21/9b/78219b1a3793cbf6f8abb754c8270f48.gif")
            await interaction.send(embed=tsfembed)
            await asyncio.sleep(5)

            result = random.choice(["орёл", "решка"])

            if choice.lower() == result:
                winnings = int(coins * 1.25)
                await cursor.execute("UPDATE eco SET money = money + ? WHERE memberid=?", (winnings, user_id))
                message = f"Поздравляем! Вы выиграли {winnings} <:coin:1207748043445637220> "
                imagef = "https://i.pinimg.com/originals/fe/a5/bd/fea5bd4fd1dffa91aeaca894bd419ff1.gif"
            else:
                imagef = "https://i.pinimg.com/originals/e8/58/bc/e858bc07cf939c1516e0536144cd6b98.gif"
                message = f"Увы, вы проиграли {coins} <:coin:1207748043445637220> "

            await conn.commit()

            coinflip_embed = disnake.Embed(description=f"**{interaction.author.mention}** подбрасывает монетку")
            coinflip_embed.add_field(name="Результат:", value=message, inline=False)
            coinflip_embed.set_image(url=imagef)

            await interaction.edit_original_message(embed=coinflip_embed)

    @commands.slash_command(
        description="Бросить кубик с возможностью угадывания",
    )
    async def dice(
        self,
        interaction: disnake.AppCommandInteraction,
        bet: int,
        num: int
    ):
        user_id = interaction.author.id

        async with aiosqlite.connect('economy.db') as conn:
            cursor = await conn.cursor()

            await cursor.execute("SELECT money FROM eco WHERE memberid=?", (user_id,))
            user_coins = (await cursor.fetchone() or [0])[0]

            if num > 7:
                await interaction.send("Введите число от 2 до 6", ephemeral=True)
                return

            if bet > user_coins:
                embed = disnake.Embed(
                    title="Ошибка",
                    description="У вас недостаточно монет для ставки.",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if bet <= 49:
                embed = disnake.Embed(
                    title="Ошибка",
                    description="Минимальная ставка 50 <:coin:1207748043445637220> ",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            await cursor.execute("UPDATE eco SET money = money - ? WHERE memberid=?", (bet, user_id))
            await conn.commit()

            dicesoon = disnake.Embed(title="Игральные Кости")
            dicesoon.set_image(url="https://64.media.tumblr.com/f7c65d1694546efdf42e654e704b6411/181af668b9f8e414-e7/s640x960/6d5a5cbeec977464adcc47b9ea72f6354f110792.gif")
            await interaction.send(embed=dicesoon)
            await asyncio.sleep(3)
            dice_result = random.randint(2, 6)

            if num == dice_result:
                winnings = bet * dice_result
                await cursor.execute("UPDATE eco SET money = money + ? WHERE memberid=?", (winnings, user_id))
                message = f"Поздравляем! Вы угадали число {dice_result} и выиграли {winnings} <:coin:1207748043445637220> "
                imaged = "https://i.pinimg.com/originals/a1/5a/6a/a15a6a3a9fdd92a55d7f244a2aeb0623.gif"
            else:
                message = f"Увы, вы не угадали. Выпало число {dice_result}."
                imaged = "https://i.pinimg.com/originals/9d/23/99/9d2399ac88785cd20580400a351ec82f.gif"

            await conn.commit()

            dice_embed = disnake.Embed(description=f"**{interaction.author.mention}** бросает кубик")
            dice_embed.add_field(name="Результат:", value=message, inline=False)
            dice_embed.set_image(url=imaged)

            await interaction.edit_original_message(embed=dice_embed)
            
def setup(bot):
    bot.add_cog(Game(bot))
