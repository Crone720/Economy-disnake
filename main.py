import disnake
from disnake.ext import commands
from utils.config import TOKEN

bot = commands.Bot(
    command_prefix="help/", 
    intents=disnake.Intents.all(), 
    help_command=None,
    reload=True,
    test_guilds=[1218482629255368857]
)

@bot.event
async def on_ready():
    print(f'Бот запустился')

bot.load_extensions("./utils/cogs")
bot.run(TOKEN)