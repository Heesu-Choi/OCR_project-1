import os
import sys
import json
import pymysql
from pymysql import DATE, NULL

# db 연결
project_db = pymysql.connect(
    user='',
    passwd='',
    host='',
    db='project_test',
    charset='utf8',
    autocommit=True
)
# 커서 생성
try:
    with project_db.cursor(pymysql.cursors.DictCursor) as cursor:
        # 모델 돌려서 음식이름이 나오면 db에 Query 던지기
        # SQL문 실행
        food_name = '닭고기볶음밥'    # 모델에서 받아오는 코드 짜야 함
        sql = "select * from food_nutritions where `food_name` like %s;"
        cursor.execute(sql, food_name)

        # 데이타 Fetch
        rows = cursor.fetchall()

        ### 여러개의 항목이 검색됨 어떤 기준으로 하나만 선택해서 넣어줄 것인가...

    with project_db.cursor(pymysql.cursors.DictCursor) as cursor:
    
        # 받아온 데이터를 유저 정보랑 엮어서 저장하기
        # 로그인 정보에서 유저정보 어떻게 받아올 것인가... 일단은 임의로 작성...ㅠ
        user_num = 1
        date = '2020-11-02 12:30:00'
        food_num = rows[0]['food_num']

        if date == NULL or date == '':
            sql = "insert into user_intake(user_num, eaten_food) values (%s,%s)"
            data = (user_num, food_num)
            cursor.execute(sql, data)

        else:
            sql = "insert into user_intake(user_num, eaten_food, date) values (%s,%s,%s)"
            data = (user_num, food_num, date)
            cursor.execute(sql, data)

finally:        
    project_db.close()


# 누적된 정보에서 만들어내자 무언가...

# 유저연령 및 성별에 따른 기준 검색



# 섭취 상태 평가 (탄단지 비율, 과다섭취 or 섭취부족)

# 추천음식