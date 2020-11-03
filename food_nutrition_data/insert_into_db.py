import os
import sys
import json
import pymysql

project_db = pymysql.connect(
    user='root',
    passwd='Pi#141592',
    host='127.0.0.1',
    db='project_test',
    charset='utf8',
    # autocommit=True
)

cursor = project_db.cursor(pymysql.cursors.DictCursor)

start = [str(n) for n in range(1,29280, 1000)]
end = [str(j) for j in range(1000, 30001, 1000)]

trimed_data = []

# api에서 데이터 불러오기
for k in range(len(end)):
    
    # url = "http://openapi.foodsafetykorea.go.kr/api/e1521f6c3d9e4d68b209/I2790/json/"+start[k]+"/"+end[k]
    # request = urllib.request.Request(url)
    # response = urllib.request.urlopen(request)

    with open('origianl_data/nutrition_db_'+start[k]+'-'+end[k]+'.json', 'r', encoding='utf-8') as f:

        data = json.load(f)

        # 필요 없는 컬럼 버리기...
        row_data = data['I2790']['row']

        trimed_data = []
        for i in row_data:
            get_v = lambda x : None if i[x] == "" else i[x]

            temp = (
                i['NUM'],               # 번호  INT
                i['FOOD_CD'],           # 식품코드 VARCHAR(45)
                i['DESC_KOR'],          # 식품명 VARCHAR(45)
                i['SERVING_SIZE'],      # 총내용량 INT
                get_v('NUTR_CONT1'),    # 열량(kcal)(1회제공량당) INT
                get_v('NUTR_CONT2'),    # 탄수화물(g)(1회제공량당) FLOAT
                get_v('NUTR_CONT3'),    # 단백질(g)(1회제공량당) FLOAT
                get_v('NUTR_CONT4'),    # 지방(g)(1회제공량당) FLOAT
                get_v('NUTR_CONT5'),    # 당류(g)(1회제공량당) FLOAT
                get_v('NUTR_CONT6'),    # 나트륨(mg)(1회제공량당) FLOAT
                get_v('NUTR_CONT7'),    # 콜레스테롤(mg)(1회제공량당) FLOAT
                get_v('NUTR_CONT8'),    # 포화지방산(g)(1회제공량당) FLOAT
                get_v('NUTR_CONT9')     # 트랜스지방(g)(1회제공량당) FLOAT
            )
            print(temp)
            trimed_data.append(temp)

        # print(trimed_data)

        # 바로 mySQL에 넣어보기
        # INSERT 
        sql = "INSERT INTO `food_nutritions` (`food_num`, `food_code`, `food_name`, `food_servesize`, `ntr1_calorie`, `ntr2_carbon`, \
            `ntr3_protein`, `ntr4_fat`, `ntr5_sugars`, `ntr6_sodium`, `ntr7_cholesterol`, `ntr8_saturatedFat`, `ntr9_transFat` ) \
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.executemany(sql, trimed_data)
        project_db.commit()
    f.close()
project_db.close()
