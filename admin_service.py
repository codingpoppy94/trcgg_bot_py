from exceptions import RecordNotFoundException
from call_util import RequestUtil
from embed import TemplateUtil

ru = RequestUtil()

class AdminService:
    
    # doc
    def help(self):
        
        # 검색 명령어
        field_one_value = (
            "`!전적 !전적 {name}` 자신의 전적, name의 전적 검색 \n"
            "`!결과 {gameId}` 내전 게임 결과 검색 \n"
            "`!장인 {champ}` 픽률-승률 장인 목록 \n"
            "`!통계 게임|챔프` 게임,챔프 통계 \n"
            "`!라인 {탑|정글|미드|원딜|서폿}` {라인}별 승률\n\n"
        )

        # 관리자 명령어
        field_two_value = (
            "1. 닉네임 띄어쓰기 없이, 대소문자구분 해서 사용 \n"
            "2. 운영진 권한 필요\n"
            "`!탈퇴 {name}` 탈퇴한 회원 추가, 전적검색제외 \n"
            "`!복귀 {name}` 탈퇴한 회원 복구, 전잭검색포함 \n"
            "`!부캐목록` 등록된 모든 부캐닉/본캐닉 닉네임 목록 \n"
            "`!부캐저장 {부캐닉/본캐닉}` 부캐닉네임 등록, 데이터저장할때 부캐닉네임은 본캐닉네임으로 변경되서 저장 \n"
            "`!부캐삭제 {부캐닉}` 등록된 부캐닉네임 삭제 \n"
            "`!닉변 {oldName/newName}` 닉네임 변경 \n"
            "`!drop {gameId}` {리플레이 파일 이름} 데이터 삭제 \n"
        )
        
        json_data = {
            "title": "doc",
            "description":"help",
            "fields": [
                {
                    "name": "검색 명령어",
                    "value": field_one_value,
                    "inline": False
                },
                {
                    "name": "관리자 명령어",
                    "value": field_two_value,
                    "inline": False
                },
            ]
        }
        return TemplateUtil.create_embed(json_data)
        
    # 부캐목록
    def get_mapping_name(self):
        
        json_data = {}
        
        title = "부캐 목록"
        
        desc = (
            "``` \n"
            "|  부캐  |  본캐  |\n"
            "\n"
        )
        
        records = ru.get_mapping_name()
        if records["status_code"] != 200:
            raise RecordNotFoundException("connection error")
        
        if not records.get("data"):
            raise RecordNotFoundException("not found data")
        for record in records.get("data"):
            desc += f"|  {record['sub_name']}  |  {record['main_name']}\n"
            
        size = len(records.get("data"))
        desc += "\n"
        desc += f"총: {str(size)} \n"
        desc += "```" 
        
        json_data = {
            "title": title,
            "description": desc,
            "fields": []
        }
        
        return TemplateUtil.create_embed(json_data)

    # 부캐저장
    def save_mapping_name(self, ctx, command):
        
        if self.check_auth(ctx):
            
            sub_name, main_name = self.split_str(command)
            result = ru.save_mapping_name(sub_name, main_name)
            
            if result["status_code"] != 200:
                raise RecordNotFoundException("connection error")
            return "등록 및 변경 완료"

    # 부캐삭제
    def delete_mapping_name(self, ctx, riot_name):
        
        if self.check_auth(ctx):
    
            result = ru.delete_mapping_sub_name(riot_name)
            if result["status_code"] != 200:
                raise RecordNotFoundException("connection error")
            
            if result["data"] >= 1 :
                return "부캐 삭제 완료"
            
            else :
                return "not found data"

    # 닉변
    def update_riot_name_league_and_mapping(self, ctx, command: str):
        
        if self.check_auth(ctx):
            
            old_name, new_name = self.split_str(command)
    
            result = ru.update_riot_name(new_name, old_name)
            ru.update_mapping_riot_name(new_name, old_name)
            if result["status_code"] != 200:
                raise RecordNotFoundException("connection error")
            
            if result["data"] >= 1 :
                return "닉변 완료"
            
            else :
                return "not found data"

    # 탈퇴/복귀
    def update_delete_yn_league_and_mapping(self, ctx, delete_yn, riot_name):
        
        if self.check_auth(ctx):
            
            result = ru.update_delete_yn(delete_yn, riot_name)
            ru.update_mapping_delete_yn(delete_yn, riot_name)
            if result["status_code"] != 200:
                raise RecordNotFoundException("connection error")
            
            if result["data"] >= 1 :
                if delete_yn == "Y" : 
                    return "탈퇴 완료"
                else:
                    return "복귀 완료"
            
            else :
                return "not found data"

    # 리플삭제
    def delete_league(self, ctx, game_id):
    
        if self.check_auth(ctx):
    
            result = ru.delete_league_by_game_id(game_id)
            if result["status_code"] != 200:
                raise RecordNotFoundException("connection error")
            
            if result["data"] >= 1 :
                return f":orange_circle:데이터 삭제완료: {game_id}"
            
            else :
                return "not found data"

## util 
    
    # / split
    def split_str(self, command: str):
        if command is not None:
            try:
                sub_name , main_name = command.split('/')
                return sub_name, main_name
            except ValueError:  # split이 실패할 경우
                raise RecordNotFoundException("잘못된 형식")
    
    # 권한 체크
    def check_auth(self, ctx):
        roles = ctx.author.roles  
        role_names = [role.name for role in roles] 
        if "난민디코관리자" in role_names or "난민운영진" in role_names:
            return True
        else:
            raise RecordNotFoundException("권한 없음")

        
        
        