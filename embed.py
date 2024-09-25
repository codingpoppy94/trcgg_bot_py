import discord

class TemplateUtil:
    # JSON 데이터를 받아 embed 생성
    def create_embed(json_data):
        embed = discord.Embed(
            title=json_data["title"],
            description=json_data["description"]
        )
        
        for field in json_data["fields"]:
            embed.add_field(
                name=field["name"], 
                value=field["value"], 
                inline=field["inline"]
            )
        
        return embed
    
    # !라인 value set
    def set_line_value(records, team):
        # 결과를 저장할 리스트 초기화
        result = []
        
        for record in records:
            if team == "blue" and record["game_team"] == "blue":
                # 블루 팀인 경우
                result.append(f" {record['riot_name']}   {record['champ_name']} {record['kill']}/{record['death']}/{record['assist']} "
                            f"피해량: {record['total_damage_champions']} 핑와: {record['vision_bought']}\n")
            elif team == "red" and record["game_team"] == "red":
                # 레드 팀인 경우
                result.append(f" {record['riot_name']}   {record['champ_name']} {record['kill']}/{record['death']}/{record['assist']} "
                            f"피해량: {record['total_damage_champions']} 핑와: {record['vision_bought']}\n")
        
        # 리스트를 하나의 문자열로 반환
        return ''.join(result)

    # !라인 header set
    def set_line_field_header(dto, team):
        result = ""
        
        if team == "blue":
            result += ":blue_circle: 블루 "
            # 블루 팀이면서 승리한 경우
            if dto["game_team"] == "blue" and dto["game_result"] == "승":
                result += ":v:"
        else:
            result += ":red_circle: 레드 "
            # 레드 팀이면서 패배한 경우
            if dto["game_team"] == "blue" and dto["game_result"] == "패":
                result += ":v:"
        
        return result
    
    
    # prefix: 승/패 - 승률 form
    def make_team_stat(prefix, win, lose, win_rate):
        return f"{prefix}: {win}승/{lose}패 {win_rate}%\n"
        
    # prefix - 승/승률 - kda form    
    def make_stat(prefix, win, win_rate, kda):
        stats = f"{prefix} - {win}승/{win_rate}%"
        
        if kda != 9999:
            stats += f" KDA: {kda}"
        
        stats += "\n"
        
        return stats
    
    # 통계 챔프/게임 form
    def make_stats_list(stats_list, type):
        result = []
        i = 1

        if type == "champ":
            for vo in stats_list:
                result.append(f"{i}. {TemplateUtil.make_team_stat(vo['champ_name'], vo['win'], vo['lose'], vo['win_rate'])}")
                i += 1

        elif type == "game":
            for vo in stats_list:
                result.append(f"{i}. {vo['riot_name']} - {vo['total_count']}판 \n")
                i += 1
                
        elif type == "game_high":
            for vo in stats_list:
                result.append(f"{i}. {TemplateUtil.make_stat(vo['riot_name'], vo['win'], vo['win_rate'], vo['kda'])}")
                i += 1

        return ''.join(result)

    # 필터링 및 정렬 함수
    def filter_and_sort_by_win_rate(records, win_rate, greater_than=True, limit=10):
          # 판수 순으로 먼저 sort, limit 하고 filter     
        if greater_than:
            sorted_records = sorted(records, key=lambda x: x.get("win_rate", 0), reverse=True)
            filtered_records = [record for record in sorted_records[:limit] if record.get("win_rate", 0) >= win_rate]
        else:
            sorted_records = sorted(records, key=lambda x: x.get("win_rate", 0), reverse=False)
            filtered_records = [record for record in sorted_records[:limit] if record.get("win_rate", 0) <= win_rate]

        return filtered_records
