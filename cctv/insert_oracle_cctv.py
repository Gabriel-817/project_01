import pymongo
import cx_Oracle as oci

# 접속하기(아이디/암호@서버주소:포트번호/SID)
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
# 커서 생성
cursor = conn.cursor()

# 정규표현식
import re
seoul = re.compile('.*서울특별시.*', re.IGNORECASE)  # compile the regex
conn_p = pymongo.MongoClient('192.168.99.100',32766)
db = conn_p.get_database("db1") #없으면 db1생성
coll_cctv = db.get_collection("cctv") #collection 생성


# 몽고DB에서 소재지도로명 주소가 서울특별시인것을 설치년도 내림차순으로 가져와서 data_cctv에 넣음
data_cctv = coll_cctv.find({'$or': [{'소재지지번주소':seoul},{'관리기관명':seoul},{'소재지도로명주소':seoul}, {'제공기관명':seoul}]}, {'_id':False})
print(type(data_cctv))
for tmp in data_cctv:

    
    # INSERT
    sql = """
        INSERT INTO CCTV(INSTITUTE,C_ADDRESS,O_ADDRESS,PURPOSE,CAMERA_N,PIXEL,FILM,SAVE,INSTALL_DATE,PHONE,LAT,LON,DATA,CODE,NAME) 
        VALUES(:1, :2, :3, :4, :5, :6, :7, :8,:9, :10, :11, :12,:13, :14, :15)
        """
    arr = [tmp['관리기관명'],tmp['소재지도로명주소'],tmp['소재지지번주소'],tmp['설치목적구분'],tmp['카메라대수'],tmp['카메라화소수'],tmp['촬영방면정보'],tmp['보관일수'],tmp['설치년월'],tmp['관리기관전화번호'],tmp['위도'],tmp['경도'],tmp['데이터기준일자'],tmp['제공기관코드'],tmp['제공기관명']]               
    print(arr)

    cursor.execute(sql, arr)
    conn.commit()




