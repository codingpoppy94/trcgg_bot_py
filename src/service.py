from call_util import RequestUtil
from datetime import datetime
import re
from embed import TemplateUtil
from exceptions import RecordNotFoundException

ru = RequestUtil()

class Service:
    
    # !전적
    def all_record(self, ctx, riot_name:str):
        
        if riot_name is None:
            riot_name = self.get_member_nick(ctx)
            
        riot_name = riot_name.replace(" ", "").replace("й","n").strip()
            
        all_data = ru.get_all_record(riot_name)
        if all_data['status_code'] != 200:
            raise RecordNotFoundException("connection error")
        
        if not all_data.get("data").get("record_data"):
            raise RecordNotFoundException("not found data")
        all_data = all_data['data']
        
        # 통합 전적
        all_count = 0
        all_win = 0
        all_lose = 0
        max_count = 0
        all_win_rate = 0
        thumbs_up_str = ":thumbsup: "
        line_desc = ""
        
        record_data = all_data['record_data']
        for data in record_data:
            all_count += data.get("total_count", 0)
            all_win += data.get("win", 0)
            all_lose += data.get("lose", 0)
            
            if(data.get("total_count") > max_count):
                max_count = data.get("total_count")
        
        for data in record_data:
            if(data.get("total_count") == max_count):
                line_desc += thumbs_up_str
            line_desc += TemplateUtil.make_stat(data.get("position"), data.get("win"), data.get("win_rate"), data.get("kda"))    
                    
        all_win_rate = round((all_win * 100 / all_count) * 100) / 100.0    
        all_desc = f"통합전적 - {all_count}전 {all_win}승/{all_win_rate}% \n"  
                
        # 이번달 전적
        month_data = all_data['month_data']
        month_desc = ""
        for data in month_data:
            month_desc = TemplateUtil.make_stat("이번달 전적", data.get("win"), data.get("win_rate"), data.get("kda"))
        
        # 최근 전적
        recent_total = 0
        recent_win = 0
        recent_lose = 0
        color_str = ""
        recent_value = ""
        
        recent_data = all_data['recent_data']
    
        for data in recent_data:
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
        
        # 팀워크
        good_team_haeder = "팀워크:blue_heart:"
        good_team_value = ""
        
        low_team_header = "팀워크:broken_heart:"
        low_team_value = ""
        
        with_team_data = all_data['with_team_data']
        team_data = with_team_data
        
        # 팀워크 높은 순
        high_team_data = TemplateUtil.filter_and_sort_by_win_rate(team_data, 52, greater_than=True)
        for data in high_team_data:
            good_team_value += TemplateUtil.make_team_stat(data.get("riot_name"), data.get("win"), data.get("lose"), data.get("win_rate"))
        
        # 팀워크 낮은 순
        low_team_data = TemplateUtil.filter_and_sort_by_win_rate(team_data, 48, greater_than=False)
        for data in low_team_data:
            low_team_value += TemplateUtil.make_team_stat(data.get("riot_name"), data.get("win"), data.get("lose"), data.get("win_rate"))
        
        # 맞라인
        easy_rival_header = "맞라인:thumbsup:"
        easy_rival_value = ""
        
        hard_rival_header = "맞라인:thumbsdown:"
        hard_rival_value = ""
        
        other_team_data = all_data['other_team_data']
        team_data = other_team_data

        # 라이벌 자주 이기는 순
        easy_rival_data = TemplateUtil.filter_and_sort_by_win_rate(team_data, 52, greater_than=True)
        for data in easy_rival_data:
            easy_rival_value += TemplateUtil.make_team_stat(data.get("riot_name"), data.get("win"), data.get("lose"), data.get("win_rate"))
        
        # 라이벌 자주 지는 순
        hard_rival_data = TemplateUtil.filter_and_sort_by_win_rate(team_data, 48, greater_than=False)
        for data in hard_rival_data:
            hard_rival_value += TemplateUtil.make_team_stat(data.get("riot_name"), data.get("win"), data.get("lose"), data.get("win_rate"))
        
        # Most Pick
        most_pick_header = "MostPick 10"
        most_pick_value = ""
        
        most_pick_data = all_data['most_pick_data']
        for data in most_pick_data:
            most_pick_value += f"{data.get('champ_name')}: {data.get('total_count')}판 {data.get('win_rate')}% \n"
            
        desc = month_desc + "\n" + all_desc + line_desc
        
        # 호칭ex
        if riot_name == "크넹":
           riot_name = f"<:__:1197186572433490090> <:__:1197186590968139836> :crown:"

        json_data = {
            "title": riot_name,
            "description": desc,
            "fields": [
                {
                    "name": recent_header,
                    "value": recent_value,
                    "inline": True
                },
                {
                    "name": good_team_haeder,
                    "value": good_team_value,
                    "inline": True
                },
                {
                    "name": low_team_header,
                    "value": low_team_value,
                    "inline": True
                },
                {
                    "name": most_pick_header,
                    "value": most_pick_value,
                    "inline": True
                },
                {
                    "name": easy_rival_header,
                    "value": easy_rival_value,
                    "inline": True
                },
                {
                    "name": hard_rival_header,
                    "value": hard_rival_value,
                    "inline": True
                },
            ]
        }   
        
        return TemplateUtil.create_embed(json_data)

    # !장인    
    def champ_record(self, champ_name):
        
        title = ""
        field_one_name = "판수(10판 이상)"
        field_one_value = ""
        
        field_two_name = "승률(50% 이상)"
        field_two_value = ""
        
        records = ru.get_champ_master(champ_name)
        if records["status_code"] != 200:
            raise RecordNotFoundException("connection error")
        
        if not records["data"]:
            raise RecordNotFoundException("not found data")
        
        for record in records["data"]:
            field_one_value += TemplateUtil.make_team_stat(record["riot_name"], record["win"], record["lose"], record["win_rate"])
        
        high_records = [record for record in records["data"] if record.get("win_rate", 0) >= 50]
        high_records = sorted(high_records, key=lambda x: x.get("win_rate", 0), reverse=True)[:20]
        
        for record in high_records:
            field_two_value += TemplateUtil.make_team_stat(record["riot_name"], record["win"], record["lose"], record["win_rate"])
        
        title = champ_name
        
        json_data = {
            "title":title,
            "description":None,
            "fields": [
                {
                    "name": field_one_name,
                    "value": field_one_value,
                    "inline": True
                },
                {
                    "name": field_two_name,
                    "value": field_two_value,
                    "inline": True
                },
            ]
        }   
        return TemplateUtil.create_embed(json_data)
    
    # !라인
    def get_line(self, position):
        
        position = self.dict_postition(position)
        
        records = ru.get_record_line(position)
        if records["status_code"] != 200:
            raise RecordNotFoundException("connection error")
        
        if not records["data"]:
            raise RecordNotFoundException("not found data")
        
        desc = ""
        for i, record in enumerate(records["data"], start=1):  
            
            if i == 1:
                desc += ":one: "
            elif i == 2:
                desc += ":two: "
            elif i == 3:
                desc += ":three: "
            elif i == 4:
                desc += ":four: "
            elif i == 5:
                desc += ":five: "
            else:
                desc += f"{i}. "  
                
            desc += f"{record['riot_name']}{TemplateUtil.make_stat('',record['win'], record['win_rate'], record['kda']) }"
        
        title = f"{position} 라인"
        
        json_data = {
            "title": title,
            "description": desc, 
            "fields": []  
        }
        return TemplateUtil.create_embed(json_data)   
    
    # !결과
    def get_game_result(self, game_id):
        
        records = ru.get_record_game_id(game_id)       
        if records["status_code"] != 200:
            raise RecordNotFoundException("connection error")
        
        if not records["data"]:
            raise RecordNotFoundException("not found data")
        
        dto = records["data"][0]
        title = dto["game_id"]
        
        # 필드 헤더 생성 및 각각의 팀에 대한 데이터를 생성
        blue_team_field = TemplateUtil.set_line_field_header(dto, "blue")
        red_team_field = TemplateUtil.set_line_field_header(dto, "red")

        # 필드에 들어갈 실제 데이터를 빌드하는 부분
        blue_team_value = TemplateUtil.set_line_value(records["data"], "blue")
        red_team_value = TemplateUtil.set_line_value(records["data"], "red")

        json_data = {
            "title": title,
            "description": None,
            "fields": [
                {
                    "name": blue_team_field,
                    "value": blue_team_value,
                    "inline": False
                },
                {
                    "name": red_team_field,
                    "value": red_team_value,
                    "inline": False
                }
            ]
        }
        return TemplateUtil.create_embed(json_data) 
    
    # !통계
    def get_league_stat(self, type, date: str=None):
        
        year, month = self.split_date(date)
        
        json_data = {}
        title = f"{year}-{month} {type} 통계"
        
        if type == "게임":
            records = ru.get_game_stats(year, month)
            if records["status_code"] != 200:
                raise RecordNotFoundException("connection error")
        
            if not records["data"]:
                raise RecordNotFoundException("not found data")   
            field_one_header = "판수 20위"
            field_one_value = ""
            
            game_records = records["data"]
            field_one_value = TemplateUtil.make_stats_list(game_records[:20], "game")
            
            field_two_header = "승률 20위(20판 이상)"
            field_two_value = ""
            
            # 판수 20 이상 필터
            game_reocrds_high = [record for record in game_records if record.get("total_count", 0) >= 20]
            
            # 승률 순 정렬            
            game_reocrds_high = sorted(game_reocrds_high, key=lambda x: x.get("win_rate", 0), reverse=True)
            field_two_value = TemplateUtil.make_stats_list(game_reocrds_high[:20], "game_high")
            
            json_data = {
                "title": title,
                "description": None,
                "fields": [
                    {
                        "name": field_one_header,
                        "value": field_one_value,
                        "inline": True
                    },
                    {
                        "name": field_two_header,
                        "value": field_two_value,
                        "inline": True
                    }
                ]
            }
            return TemplateUtil.create_embed(json_data) 
                            
        elif type == "챔프":
            records = ru.get_champ_stats(year, month)
            if records["status_code"] != 200:
                raise RecordNotFoundException("connection error")
        
            if not records["data"]:
                raise RecordNotFoundException("not found data")
            
            record_list = records["data"]
            
            field_one_header = "MostPick"
            pick_list = sorted(record_list, key=lambda x: x.get("total_count", 0), reverse=True)
            field_one_value = TemplateUtil.make_stats_list(pick_list[:15], "champ")
            
            field_two_header = "1티어:partying_face:"
            high_list = sorted(record_list, key=lambda x: x.get("win_rate", 0), reverse=True)
            field_two_value = TemplateUtil.make_stats_list(high_list[:15], "champ")
            
            field_three_header = "5티어:scream:"
            low_list = sorted(record_list, key=lambda x: x.get("win_rate", 0), reverse=False)
            field_three_value = TemplateUtil.make_stats_list(low_list[:15], "champ")
            
            json_data = {
                "title": title,
                "description": None,
                "fields": [
                    {
                        "name": field_one_header,
                        "value": field_one_value,
                        "inline": True
                    },
                    {
                        "name": field_two_header,
                        "value": field_two_value,
                        "inline": True
                    },
                    {
                        "name": field_three_header,
                        "value": field_three_value,
                        "inline": True
                    }
                ]
            }
            return TemplateUtil.create_embed(json_data)
        
        else:
            raise RecordNotFoundException("unexpected value")
        
    # !클랜통계
    def get_clan_game_stat(self, date: str=None):
        
        year, month = self.split_date(date)
        
        title = f"{year}-{month}\n"
        str = ""
        
        records = ru.get_game_stats(year, month)
        if records["status_code"] != 200:
            raise RecordNotFoundException("connection error")
        
        if not records["data"]:
            raise RecordNotFoundException("not found data")
        
        for i, record in enumerate(records["data"], start=1):  
            str += f"{record['riot_name']} {record['total_count']}판 \n"
            
        result = ''.join(title+str)
        if len(result) > 2000:
            return result[:2000]
        
        return result
    
    # 리플레이 저장
    def send_discord_attachment_url(self, message):
        file_url = ""
        file_name = ""
        create_user = ""
        
        for attachment in message.attachments:
            # 첨부파일의 URL을 가져옴
            file_url = attachment.url
            file_name = attachment.filename
        create_user = message.author.nick or message.author.name
        
        # 확장자 .rofl 아닐경우 무시
        if not file_name.endswith('.rofl') : 
            return None
            
        # 리플 파일명 체크
        if self.file_name_check(file_name) :
            # file_name = file_name.split(".")[-1]
            parts = file_name.split(".")
            file_name = ".".join(parts[:-1])
            # 리플 저장 call
            return ru.save_league(file_url, file_name, create_user)['data']
        else :
            return f":red_circle:등록실패: {file_name} 잘못된 리플 파일 형식"
         
    ################ #######################    
        
    # 라인 dict
    def dict_postition(self, position):
        if position == "탑":
            real_position = "TOP"
        elif position == "정글":
            real_position = "JUG"
        elif position == "미드":
            real_position = "MID"
        elif position == "원딜":
            real_position = "ADC"
        elif position == "서폿":
            real_position = "SUP"
        else:
            raise RecordNotFoundException(f"unexpected value: {position}")
        return real_position
    
    def split_date(self, date: str = None):
        if date is None:
            now = datetime.now()
            year = str(now.year)
            month = str(now.month).zfill(2)
            return year, month
        else:   
            try:
                year, month = date.split('-')  # '2024-08'을 '-' 기준으로 분리
                return year, month
            except RecordNotFoundException("잘못된 형식"):
                return

    # 본인 member nickname 가져오기            
    def get_member_nick(self, ctx):
        riot_name = ctx.author.nick 
        if riot_name is None:
            raise RecordNotFoundException("별명 설정 필요")
        else :
            riot_name = riot_name.split("/")[0]
            return riot_name
    
    # 리플 파일명 정규식 체크
    def file_name_check(self, file_name):
        # 정규 표현식 패턴
        regexp = r"^[a-zA-Z0-9]*_\d{4}_\d{4}\.rofl$"
        
        # 정규식 매칭 여부 확인
        if re.match(regexp, file_name):
            return True
        else:
            return False
        