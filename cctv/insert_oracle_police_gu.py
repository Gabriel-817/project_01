import pymongo
import cx_Oracle as oci

# 접속하기(아이디/암호@서버주소:포트번호/SID)
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
# 커서 생성
cursor = conn.cursor()

# 정규표현식
"""
import re
a = re.compile('.*서울.*', re.IGNORECASE)  # compile the regex
"""
conn_p = pymongo.MongoClient('192.168.99.100',32766)
db = conn_p.get_database("db1") #없으면 db1생성
coll_police_gu = db.get_collection("police_gu") #collection 생성



# 몽고DB를 POLICE_GU에 넣음
data_police_gu = coll_police_gu.find({},{'_id':False})



for tmp in data_police_gu:
    
    #print(tmp)

    sql = """
        INSERT INTO POLICE_GU(REGION,NAME,GU_NAME) 
        VALUES(:1, :2, :3)
        """
     
    arr = [tmp['지방청'],tmp['관서'],tmp['구']]           
    cursor.execute(sql, arr)
    conn.commit()

