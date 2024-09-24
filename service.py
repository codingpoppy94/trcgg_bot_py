from call_util import RequestUtil
import json
import discord
        

ru = RequestUtil()

class Service:
    
    # !전적
    def all(self, riot_name:str):
        
        # 통합 전적
        all_count = 0
        all_win = 0
        all_lose = 0
        max_count = 0
        all_win_rate = 0
        thumbs_up_str = ":thumbsup: "
        line_str = ""
        
        all_data = ru.get_record(riot_name)
        
        if(all_data["status_code"] == 200):
            # print(all_data["data"])
            for data in all_data["data"]:
                all_count += data.get("total_count", 0)
                all_win += data.get("win", 0)
                all_lose += data.get("lose", 0)
                
                if(data.get("total_count") > max_count):
                    max_count = data.get("total_count")
            
            for data in all_data["data"]:
                if(data.get("total_count") == max_count):
                    line_str += thumbs_up_str
                line_str += self.make_stat(data.get("position"), data.get("win"), data.get("win_rate"), data.get("kda"))    
                    

        all_win_rate = round((all_win * 100 / all_count) * 100) / 100.0    
        all_str = f"통합전적 - {all_count}전 {all_win}승/{all_win_rate}% \n"  
                
        # 이번달 전적
        month_data = ru.get_record_month(riot_name)
        month_str = ""
        if(month_data["status_code"] == 200):
            for data in month_data["data"]:
                month_str = self.make_stat("이번달 전적", data.get("win"), data.get("win_rate"), data.get("kda"))
        
        # 최근 전적
        recent_total = 0
        recent_win = 0
        recent_lose = 0
        color_str = ""
        recent_value = ""
        
        recent_data = ru.get_top_ten(riot_name)
        if(recent_data["status_code"] == 200):
            for data in recent_data["data"]:
                recent_total += 1
                if data.get("game_result") == "승":
                    recent_win += 1
                    color_str = ":blue_circle: "
                else:
                    recent_lose += 1
                    color_str = ":red_circle: "
                kda = f"{data.get('kill')}/{data.get('death')}/{data.get('assist')}"
                recent_value += f"{color_str} {data.get('champ_name')} {kda} \n"
               
        recent_header = f"최근 {recent_total}전 {recent_win}승 {recent_lose}패"
        
        
        most_pick_data = ru.get_most_pick(riot_name)
        with_team_data = ru.get_record_with_team(riot_name)
        other_team_data = ru.get_record_other_team(riot_name)
        
        desc = month_str + "\n" + all_str + line_str
        
        embed = discord.Embed(title=riot_name, description=desc)
        embed.add_field(name=recent_header, value=recent_value, inline=True)
        return embed
        
        
    ################ #######################    
     
    # prefix: 승/패 - 승률 form
    def make_team_stat(self, prefix, win, lose, win_rate):
        return f"{prefix}: {win}승/{lose}패 {win_rate}%\n"
        
    # prefix - 승/승률 - kda form    
    def make_stat(self, prefix, win, win_rate, kda):
        stats = f"{prefix} - {win}승/{win_rate}%"
        
        if kda != 9999:
            stats += f" KDA: {kda}"
        
        stats += "\n"
        
        return stats
    
    # 통계 챔프/게임 form
    def make_stats_list(self, stats_list, stat_type):
        result = []
        i = 1

        if stat_type == "champ":
            for vo in stats_list:
                result.append(f"{i}. {self.make_team_stat(vo.get_champ_name(), vo.get_win(), vo.get_lose(), vo.get_win_rate())}")
                i += 1

        elif stat_type == "riotname":
            for vo in stats_list:
                result.append(f"{i}. {self.make_stat(vo.get_riot_name(), vo.get_win(), vo.get_win_rate(), vo.get_kda())}")
                i += 1

        return ''.join(result)

