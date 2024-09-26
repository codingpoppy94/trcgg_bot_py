import discord
from discord.ext import commands
import os
from service import Service
from admin_service import AdminService
from exceptions import RecordNotFoundException

service = Service()
admin_service = AdminService()

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

@bot.command(name='doc')
async def help(ctx):
    try:
        await ctx.send(embed=admin_service.help())
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='부캐목록')
async def help(ctx):
    try:
        await ctx.send(embed=admin_service.get_mapping_name())
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='부캐저장')
async def add_sub_name(ctx, command: str):
    try:
        await ctx.send(admin_service.save_mapping_name(ctx, command))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='부캐삭제')
async def delete_sub_name(ctx, riot_name: str):
    try:
        await ctx.send(admin_service.delete_mapping_name(ctx, riot_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))

@bot.command(name='닉변')
async def change_riot_name(ctx, command: str):
    try:
        await ctx.send(admin_service.update_riot_name_league_and_mapping(ctx, command))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='탈퇴')
async def with_draw(ctx, riot_name: str):
    try:
        await ctx.send(admin_service.update_delete_yn_league_and_mapping(ctx, "Y", riot_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='복귀')
async def recover(ctx, riot_name: str):
    try:
        await ctx.send(admin_service.update_delete_yn_league_and_mapping(ctx, "N", riot_name))
    except RecordNotFoundException as e:
        await ctx.send(str(e))

# 리플 삭제
@bot.command(name='drop')
async def delete_replay(ctx, game_id: str):
    try:
        await ctx.send(admin_service.delete_league(ctx, game_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
# CommandNotFound 에러 핸들러
@bot.event
async def on_command_error(ctx, error):
    # CommandNotFound 에러 처리
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("없는 명령어입니다.")
    else:
        # 다른 에러 처리 (선택 사항)
        raise error

    
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