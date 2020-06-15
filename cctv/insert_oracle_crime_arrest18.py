import pymongo
import cx_Oracle as oci

# 접속하기(아이디/암호@서버주소:포트번호/SID)
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
# 커서 생성
cursor = conn.cursor()

# 정규표현식
import re
a = re.compile('.*서울.*', re.IGNORECASE)  # compile the regex
conn_p = pymongo.MongoClient('192.168.99.100',32766)
db = conn_p.get_database("db1") #없으면 db1생성
coll_arrest18 = db.get_collection("crime_arrest18") #collection 생성



a = coll_arrest18.find({'지방청':a},{'_id':False})
data_crime_arrest18 = list(a)
print(data_crime_arrest18)

for tmp in data_crime_arrest18:

    sql = """
        INSERT INTO CRIME_ARREST18(REGION,NAME,NUM) 
        VALUES(:1, :2, :3)
        """
    arr = [tmp['지방청'],tmp['경찰서'],tmp['검거건수(2018년)'].replace(",","")]           
    print(arr)
    cursor.execute(sql, arr)
    conn.commit()