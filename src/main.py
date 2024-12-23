import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os
from service import Service
from admin_service import AdminService
from guild_service import GuildService
from exceptions import RecordNotFoundException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

service = Service()
admin_service = AdminService()
guild_service = GuildService()

# .env 파일에서 환경 변수 로드
load_dotenv()

# os 설정
token = os.getenv('DISCORD_TOKEN')
trc_channel_id = int(os.getenv('TRC_CHANNEL_ID'))

# Discord 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 스케줄러 설정
scheduler = AsyncIOScheduler()

## 검색
@bot.command(name='전적')
async def record(ctx, *, riot_name: str= None):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.all_record(ctx, riot_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))

@bot.command(name='최근전적')
async def record(ctx, riot_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.topten_record(riot_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
    
@bot.command(name='장인')
async def master(ctx, champ_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.champ_record(champ_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='라인')
async def line(ctx, champ_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.get_line(champ_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='결과')
async def game_result(ctx, game_id: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.get_game_result(game_id, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='통계')
async def stats(ctx, type: str, date: str=None):
    try:
        guild_id = ctx.guild.id
        await ctx.send(embed=service.get_league_stat(type, guild_id, date))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='클랜통계')
async def clan_stats(ctx, date: str=None):
    try:
        guild_id = ctx.guild.id
        await ctx.send(service.get_clan_game_stat(guild_id, date))
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
        guild_id = ctx.guild.id
        await ctx.send(embed=admin_service.get_mapping_name(guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='부캐저장')
async def add_sub_name(ctx, command: str):
    try:
        guild_id = str(ctx.guild.id)
        await ctx.send(admin_service.save_mapping_name(ctx, command, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='부캐삭제')
async def delete_sub_name(ctx, riot_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(admin_service.delete_mapping_name(ctx, riot_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))

@bot.command(name='닉변')
async def change_riot_name(ctx, command: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(admin_service.update_riot_name_league_and_mapping(ctx, command, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='탈퇴')
async def with_draw(ctx, riot_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(admin_service.update_delete_yn_league_and_mapping(ctx, "Y", riot_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
@bot.command(name='복귀')
async def recover(ctx, riot_name: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(admin_service.update_delete_yn_league_and_mapping(ctx, "N", riot_name, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))

# 리플 삭제
@bot.command(name='drop')
async def delete_replay(ctx, game_id: str):
    try:
        guild_id = ctx.guild.id
        await ctx.send(admin_service.delete_league(ctx, game_id, guild_id))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
## 길드 관리
@bot.command(name='길드')
async def manage_guild(ctx):
    try:
        await ctx.send(guild_service.save_guild(ctx))
    except RecordNotFoundException as e:
        await ctx.send(str(e))
        
## event
        
# 첨부파일(리플레이) event
@bot.event
async def on_message(message):
    # 메시지가 봇이 전송한 것이라면 무시    
    if message.author.bot:
        return
    elif message.attachments:
        result = service.send_discord_attachment_url(message)
        if result is None:
            return
        else:
            await message.channel.send(result)
    else:
        # 명령어 처리
        await bot.process_commands(message)

        
# CommandNotFound 에러 핸들러
@bot.event
async def on_command_error(ctx, error):
    # CommandNotFound 에러 처리
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("없는 명령어입니다.")
    else:
        # 다른 에러 처리 (선택 사항)
        raise error

# bot 실행시    
@bot.event
async def on_ready():
   scheduler.start()
    
## 스케쥴

# 내전 출석에 오후 5시마다 메시지 전송
@scheduler.scheduled_job('cron', hour=17, minute=0)
async def scheduled_message():
    channel = bot.get_channel(trc_channel_id)
    if channel:
        channel.send("```19:30 시작합니다. 시작 5분전에 대기해주세요.```")
        
# 롤체 출석 오후 10시
@scheduler.scheduled_job('cron', hour=21, minute=59)
async def lolchess_message():
    url = 'https://discord.com/api/webhooks/1315616035222589492/0Hi3t2hmXTPiQdfnaYOg2Ff1uDSDb6zZ3m84QVNdOLg4dCYDgLlyB3806QnId9I7nNxh?thread_id=1234521788432650261'
    message = {"content": "```출석은 22:00부터 게임은 23:00 시작합니다. 시작 5분전에 대기해주세요.\n롤토체스 진행자는 첫 출석찍은 사람입니다. 막판과 대기자관리 부탁드립니다. ```" }
    requests.post(url, data=message)
        
# 칼바 출석 오후 10시
# @scheduler.scheduled_job('cron', hour=22, minute=00)
# async def kalba_message():
#     url = 'https://discord.com/api/webhooks/1315616054965174302/usGs8FlqC_3cgnCl68xDViKuSGYuDTujMdbd6kiTho3da-RQbptZqdCPd_JQiPQose10?thread_id=1234521842434183198'
#     message = {"content": "```꿈과 행복이 가득한 겨울왕국❄️ 칼바람 나락! 당신의 얼어붙은 마음을 녹이고 싶지는 않으신가요?\n출석은 22:00부터 게임은 23:00시작!! 대기하는 사람들이 추위에 떨지 않게 시작 5분전에는 꼭 와주세요!```"}
#     requests.post(url, data=message)        


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