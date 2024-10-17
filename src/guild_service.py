from call_util import RequestUtil
from exceptions import RecordNotFoundException

ru = RequestUtil()

class GuildService:
    
    # 길드 동기화
    def save_guild(self, ctx):
        guild_id = str(ctx.guild.id)
        guild_name = ctx.guild.name
        
        guild = ru.get_guild(guild_id)
        if guild['status_code'] != 200:
            raise RecordNotFoundException("connection error")
        
        if len(guild['data']) > 0 :
            return "체크 완료"
        else :
            guild_save = ru.save_guild(guild_id, guild_name)
            if guild_save['status_code'] != 200:
                raise RecordNotFoundException("connection error")
            return f"{guild_name} 추가 완료"
        