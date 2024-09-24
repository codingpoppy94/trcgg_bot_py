import discord
from discord.ext import commands
import os

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='전적')
async def record(ctx):
    await ctx.send('전적 보여줌')
    
@bot.command(name='장인')
async def master(ctx):
    print(ctx)
    await ctx.send('장인 보여줌')
    

    
    
# bot.add_command(_record)


# client = discord.Client(intents=intents)
# 
# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('!hello'):
#         await message.channel.send('Hello!')

# client.run(token)
bot.run(token)