import discord
from discord.ext import commands
import os
from service import RecordNotFoundException, Service

service = Service()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

## 검색

@bot.command(name='전적')
async def record(ctx, riot_name: str):
    try:
        await ctx.send(embed=service.all_record(riot_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
    
@bot.command(name='장인')
async def master(ctx, champ_name: str):
    try:
        await ctx.send(embed=service.champ_record(champ_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='라인')
async def line(ctx, champ_name: str):
    try:
        await ctx.send(embed=service.get_line(champ_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='결과')
async def game_result(ctx, game_id: str):
    try:
        await ctx.send(embed=service.get_game_result(game_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='통계')
async def stats(ctx, type: str, date: str=None):
    try:
        await ctx.send(embed=service.get_league_stat(type, date))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='클랜통계')
async def clan_stats(ctx, date: str=None):
    try:
        await ctx.send(service.get_clan_game_stat(date))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
    
## 관리자 명령어
    
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