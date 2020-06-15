#########파일명crime_occ18.py##########
import csv
import readline
import pymongo

conn = pymongo.MongoClient('192.168.99.100', 32766)
db = conn.get_database("db1")
coll = db.get_collection("crime_occur12") 

f = open('./cctv/hero/crime_occur12.csv', 'r', encoding="utf-8")
rdr = csv.reader(f)
column = next(rdr) 

for line in rdr:
    dict1 = dict()    
    for idx, val in enumerate(line):
        dict1[column[idx]] = val

    coll.insert_one(dict1)
conn.close()