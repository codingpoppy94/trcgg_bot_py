import requests
import json
import os 

contextPath = os.getenv('CONTEXTPATH')

class RequestUtil:
    # 생성자?
    # def __init__(self, url):
    
    def call(self, url, method="GET", data=None):
        try:
            if method == "GET":
                res = requests.get(url)
            elif method == "POST":
                res = requests.post(url, json=data)
            elif method == "PUT":
                res = requests.put(url, params=data)
            elif method == "DELETE":
                res = requests.delete(url, params=data)
            else:
                raise ValueError("Unsupported HTTP method")
            
            # 상태 코드와 JSON 데이터를 함께 반환
            return {"status_code": res.status_code, "data": json.loads(res.content)}
            # return json.loads(res)
        
        except requests.exceptions.RequestException as e:
            print(f"Error while making request: {e}")
            return {"status_code": res.status_code, "data": None}

# GET 

    # 전체전적조회
    def get_record(self, riot_name):
        url = contextPath + 'league/getRecord/' + riot_name
        return self.call(url)

    # 최근한달조회
    def get_record_month(self, riot_name):
        url = contextPath + 'league/getRecordMonth/' + riot_name
        return self.call(url)
    
    # 최근 Top 10 게임 조회
    def get_top_ten(self, riot_name):
        url = contextPath + 'league/getTopTen/' + riot_name
        return self.call(url)
    
    # 모스트픽
    def get_most_pick(self, riot_name):
        url = contextPath + 'league/getMostPick/' + riot_name
        return self.call(url)

    # 최근 두달간 같은 팀 시너지
    def get_record_with_team(self, riot_name):
        url = contextPath + 'league/getRecordWithTeam/' + riot_name
        return self.call(url)

    # 나와 인간상성 찾기
    def get_record_other_team(self, riot_name):
        url = contextPath + 'league/getRecordOtherTeam/' + riot_name
        return self.call(url)

    # 장인
    def get_champ_master(self, champ_name):
        url = contextPath + 'league/master/' + champ_name
        return self.call(url)

    # 챔프 통계
    def get_champ_stats(self, year, month):
        url = contextPath + f'league/champStats/{year}/{month}'
        return self.call(url)

    # 게임 통계
    def get_game_stats(self, year, month):
        url = contextPath + f'league/gameStats/{year}/{month}'
        return self.call(url)

    # 라인별 승률 조회
    def get_record_line(self, position):
        url = contextPath + 'league/lineStats/' + position
        return self.call(url)

    # 게임 결과
    def get_record_game_id(self, game_id):
        url = contextPath + 'league/gameResult/' + game_id
        return self.call(url)

    # 부캐닉 조회 
    def get_mapping_name(self):
        url = contextPath + 'league/getMappingName'
        return self.call(url)

    # # 중복 리플 파일 조회
    # def get_replay_name(game_id):
    #     url = contextPath + 'league/getReplayName/' + game_id
    #     return self.call(url)

# POST

    # 리플 데이터 저장 url 만 보내줄거양
    def save_league(self, file_url, file_name, create_user):
        url = contextPath + 'league/parse'
        data = {
            "file_url": file_url,
            "file_name": file_name,
            "create_user": create_user
        }
        return self.call(url, method="POST", data=data)

    # 부캐 저장
    def save_mapping_name(self, sub_name, main_name):
        url = contextPath + 'league/mapping'
        data = {"sub_name": sub_name, "main_name": main_name}
        return self.call(url, method="POST", data=data)

# PUT

    # 탈퇴 - 리그 정보
    def update_delete_yn(self, delete_yn, riot_name):
        url = contextPath + 'league/deleteYn'
        data = {"delete_yn": delete_yn, "riot_name": riot_name}
        return self.call(url, method="PUT", data=data)

    # 탈퇴 - 부캐 닉네임
    def update_mapping_delete_yn(self, delete_yn, riot_name):
        url = contextPath + 'league/mapping/deleteYn'
        data = {"delete_yn": delete_yn, "riot_name": riot_name}
        return self.call(url, method="PUT", data=data)

    # 닉변 - 리그 정보
    def update_riot_name(self, new_name, old_name):
        url = contextPath + 'league/riotName'
        data = {"new_name": new_name, "old_name": old_name}
        return self.call(url, method="PUT", data=data)

    # 닉변 - 부캐 닉네임 
    def update_mapping_riot_name(self, new_name, old_name):
        url = contextPath + 'league/mapping/riotName'
        data = {"new_name": new_name, "old_name": old_name}
        return self.call(url, method="PUT", data=data)

# DELETE

    # 리플 삭제
    def delete_league_by_game_id(self, game_id):
        url = contextPath + 'league/game'
        data = {"game_id" : game_id}
        return self.call(url, method="DELETE", data=data)

    # 부캐삭제
    def delete_mapping_sub_name(self, riot_name):
        url = contextPath + 'league/mapping/subName'
        data = {"riot_name" : riot_name}
        return self.call(url, method="DELETE", data=data)