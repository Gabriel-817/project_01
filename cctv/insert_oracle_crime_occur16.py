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
coll_occur16 = db.get_collection("crime_occur16") #collection 생성



# 몽고DB에서 지방청 이름이 서울인것을 data_cctv에 넣음
a = coll_occur16.find({'지방청':a},{'_id':False})
data_crime_occur16 = list(a)
print(data_crime_occur16)
for tmp in data_crime_occur16:

    sql = """
        INSERT INTO CRIME_OCCUR16(REGION,NAME,NUM) 
        VALUES(:1, :2, :3)
        """
    arr = [tmp['지방청'],tmp['관서'],tmp['발생건수(2016년)'].replace(",","")]           
    print(arr)
    cursor.execute(sql, arr)
    conn.commit()