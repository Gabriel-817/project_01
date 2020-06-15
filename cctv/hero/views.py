from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth.models import User
from base64 import b64encode
import pandas as pd
import matplotlib.pyplot as plt
import io # byte로 변환
import base64 # byte를 base64로 변경
from matplotlib import font_manager, rc #한글 폰트 적용
from matplotlib.pyplot import figure

cursor = connection.cursor()


@csrf_exempt
def main_vis(request):
    if request.method == 'GET' or request.method == 'POST':
        return render(request, 'hero/main_vis.html')
    
        
@csrf_exempt
def main_login(request):
    if request.method == 'GET':
        return render(request, 'hero/main_login.html')
    
    elif request.method =='POST':
        
        id = request.POST['id']
        pw = request.POST['pw']

        ar = [id,pw]
        
        print(ar)

        sql = """
            SELECT ID, NAME FROM TABLE_PR WHERE ID = %s AND PW = %s
            """
        cursor.execute(sql, ar)
        
        data = cursor.fetchone()

        if data:
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('/hero/menu_list')
            
        return redirect('/hero/main_login_wrong')

@csrf_exempt
def main_login_wrong(request):
    if request.method == 'GET':
        return render(request, 'hero/main_login_wrong.html')
    
    elif request.method =='POST':
        id = request.POST['id']
        pw = request.POST['pw']

        ar = [id,pw]
        print(ar)

        sql = """
            SELECT ID, NAME FROM TABLE_PR WHERE ID = %s AND PW = %s
            """
        cursor.execute(sql, ar)
        data = cursor.fetchone()

        if data:
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('hero/menu_list')
        
        return redirect('/hero/main_login_wrong') 


@csrf_exempt
def main_join(request):
    if request.method == 'GET':
        return render(request, 'hero/main_join.html')
       
    if request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']
        
        ar = [id, na, ag, pw]

        sql = """
        INSERT INTO TABLE_PR(ID,NAME,AGE,PW,JOINDATE) 
        VALUES (%s, %s, %s, %s, SYSDATE)
        """
        cursor.execute(sql,ar)

        print(ar)

        return redirect("/hero/main_join1")

@csrf_exempt
def main_join1(request):
    if request.method == 'GET':
        return render(request, 'hero/main_join1.html')
       
    if request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']
        
        ar = [id, na, ag, pw]

        sql = """
        INSERT INTO TABLE_PR(ID,NAME,AGE,PW,JOINDATE) 
        VALUES (%s, %s, %s, %s, SYSDATE)
        """
        cursor.execute(sql,ar)

        print(ar)

        return redirect("/hero/menu_list")

@csrf_exempt
def main_logout(request):
    if request.method == 'GET' or request.method == 'POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/hero/main_vis')


@csrf_exempt
def menu_list(request):
    if request.method == 'GET':
        return render(request, 'hero/menu_list.html')
    


@csrf_exempt
def gu_cctv(request):
    if request.method == 'GET':
        return render(request, 'hero/gu_cctv.html')
    


       

@csrf_exempt
def gu_cctv2(request):
    if request.method == 'GET':
        gu_name = request.GET.get('gu_name', "")
        type11 = request.GET.get('btn', "Search")
        
        if type11 == "Search":
            str = "%"+gu_name+"%"
            startyear="2011"
            endyear="2019"

            print(str)
            sql = """
                SELECT SUM(CAMERA_N), SUBSTR(INSTALL_DATE, 0, 4)
                FROM CCTV
                WHERE C_ADDRESS LIKE %s
                GROUP BY SUBSTR(INSTALL_DATE, 0, 4)
                HAVING SUBSTR(INSTALL_DATE, 0, 4) >= %s AND SUBSTR(INSTALL_DATE, 0, 4) < %s
                ORDER BY SUBSTR(INSTALL_DATE, 0, 4) ASC 
                """
            cursor.execute(sql, [str, startyear, endyear])
            data = cursor.fetchall()
            print(data)

            return render(request, 'hero/gu_cctv2.html', {'gu_list':data, 'gu_name': gu_name})
        elif type11 == "Chart":
            str = "%"+gu_name+"%"
            startyear="2011"
            endyear="2019"
            
            font_name = font_manager.FontProperties(fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
            rc('font', family=font_name) # 폰트적용
            plt.rcParams['figure.figsize']= (12, 4)

            sql = """
                SELECT SUM(CAMERA_N), SUBSTR(INSTALL_DATE, 0, 4)
                FROM CCTV
                WHERE C_ADDRESS LIKE %s
                GROUP BY SUBSTR(INSTALL_DATE, 0, 4)
                HAVING SUBSTR(INSTALL_DATE, 0, 4) >= %s AND SUBSTR(INSTALL_DATE, 0, 4) < %s
                ORDER BY SUBSTR(INSTALL_DATE, 0, 4) ASC 
                """
            cursor.execute(sql, [str, startyear, endyear])
            data = cursor.fetchall()
            x= []
            y=[]
            for i in data  : 
                y.append(i[0])
                x.append(i[1])
   
            chart_name = gu_name + "_Chart"
            plt.bar(x,y)
            plt.title(chart_name)
            plt.xlabel("Year")
            plt.ylabel("CCTV")


                #plt.show()  #표시
            plt.draw()  #안보이게 그림을 캡쳐
            img = io.BytesIO() # img에 byte배열로 보관
            plt.savefig(img, format="png") #png파일 포멧으로 저장
            img_url = base64.b64encode(img.getvalue()).decode()    
                
            plt.close()    #그래프 종료
            
            
            
            
            
            return render(request, 'hero/gu_chart_1.html',{"gu_chart_1":'data:;base64,{}'.format(img_url)})





@csrf_exempt
def gu_crime(request):
    if request.method == 'GET':
        return render(request, 'hero/gu_crime.html')




@csrf_exempt 
def gu_crime2(request):
    if request.method == 'GET':
        gu_name_c = request.GET.get('gu_name_c', "")
        type12 = request.GET.get('btn', "Search")
        
        if type12 == "Search":
            str = gu_name_c
            startyear="2011"
            endyear="2019"

            print(str)
            sql = """
                SELECT t4.YEAR, t4.sum1, t5.sum2 
                FROM
                    (SELECT t3.YEAR, SUM(t3.NUM) sum1   
                        FROM
                            (SELECT t1.NAME, t1.GU_NAME, t2.NUM, t2.YEAR 
                                FROM POLICE_GU t1 
                                INNER JOIN CRIME_ARREST14 t2
                                ON t1.NAME= t2.NAME) t3
                        WHERE t3.GU_NAME = %s
                        GROUP BY t3.YEAR
                        HAVING SUBSTR(YEAR, 0, 4) >= %s AND SUBSTR(YEAR, 0, 4) < %s
                        ORDER BY t3.YEAR ASC) t4
                INNER JOIN
                (SELECT t3.YEAR, SUM(t3.NUM) sum2  
                    FROM
                    (SELECT t1.NAME, t1.GU_NAME, t2.NUM, t2.YEAR 
                        FROM POLICE_GU t1 
                        INNER JOIN CRIME_OCCUR14 t2
                        ON t1.NAME= t2.NAME) t3
                    WHERE t3.GU_NAME = %s
                GROUP BY t3.YEAR
                HAVING SUBSTR(YEAR, 0, 4) >= %s AND SUBSTR(YEAR, 0, 4) < %s
                ORDER BY t3.YEAR ASC) t5
                ON t4.YEAR = t5.YEAR
                """

            cursor.execute(sql, [str, startyear, endyear, str, startyear, endyear])
            data_c = cursor.fetchall()
            print(data_c)

            return render(request, 'hero/gu_crime2.html', {'gu_list_c':data_c, 'gu_name_c': gu_name_c})
        
        elif type12 == "Chart":
            
            str = gu_name_c
            startyear="2011"
            endyear="2019"

            sql = """
                SELECT t4.YEAR, t4.sum1, t5.sum2 
                FROM
                    (SELECT t3.YEAR, SUM(t3.NUM) sum1   
                        FROM
                            (SELECT t1.NAME, t1.GU_NAME, t2.NUM, t2.YEAR 
                                FROM POLICE_GU t1 
                                INNER JOIN CRIME_ARREST14 t2
                                ON t1.NAME= t2.NAME) t3
                        WHERE t3.GU_NAME = %s
                        GROUP BY t3.YEAR
                        HAVING SUBSTR(YEAR, 0, 4) >= %s AND SUBSTR(YEAR, 0, 4) < %s
                        ORDER BY t3.YEAR ASC) t4
                INNER JOIN
                (SELECT t3.YEAR, SUM(t3.NUM) sum2  
                    FROM
                    (SELECT t1.NAME, t1.GU_NAME, t2.NUM, t2.YEAR 
                        FROM POLICE_GU t1 
                        INNER JOIN CRIME_OCCUR14 t2
                        ON t1.NAME= t2.NAME) t3
                    WHERE t3.GU_NAME = %s
                GROUP BY t3.YEAR
                HAVING SUBSTR(YEAR, 0, 4) >= %s AND SUBSTR(YEAR, 0, 4) < %s
                ORDER BY t3.YEAR ASC) t5
                ON t4.YEAR = t5.YEAR
                """
            cursor.execute(sql, [str, startyear, endyear, str, startyear, endyear])
            data1 = cursor.fetchall()
            data3 = []
            for tmp in data1:
                data3.append(tmp)

            print(data3)    

            figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

            font_name = font_manager.FontProperties(fname='C:/Windows/Fonts/gulim.ttc').get_name() # 폰트읽기
            rc('font', family=font_name) # 폰트적용
            plt.rcParams['figure.figsize']= (12, 4)

            df = pd.DataFrame(data3, columns =['year', 'arrest', 'occur'])
            df = df.set_index("year")

            print(df)

            df.plot(kind="bar", title=str, fontsize= 10) 
            plt.xticks(rotation = 0 )
            plt.draw()  #안보이게 그림을 캡쳐

            img = io.BytesIO() # img에 byte배열로 보관
            plt.savefig(img, format="png") #png파일 포멧으로 저장
            img_url = base64.b64encode(img.getvalue()).decode()    
            plt.close()    #그래프 종료
            
            return render(request, 'hero/gu_chart_2.html',{"gu_chart_2":'data:;base64,{}'.format(img_url)})
        
@csrf_exempt
def gu_comp(request):
    if request.method == 'GET':
        
        sql_cctv = """
                select row_number() over (order by sum(camera_n) desc), gu_name, sum(camera_n)
                from cctv
                group by gu_name
                order by sum(camera_n) desc
                """
        cursor.execute(sql_cctv)
        data_cctv = cursor.fetchmany(5)
        
        

        sql_rate = """
                select row_number() over (order by round(sum(crime_arrest14.num)/sum(crime_occur14.num),2)*100 desc), police_gu.gu_name,  round(sum(crime_arrest14.num)/sum(crime_occur14.num),2)*100 as rate
                from police_gu, crime_arrest14, crime_occur14
                where crime_occur14.name = police_gu.name and crime_arrest14.name = police_gu.name and crime_occur14.name = crime_arrest14.name 
                group by police_gu.gu_name
                order by rate desc
                """
        cursor.execute(sql_rate)
        data_rate = cursor.fetchmany(5)
        
        
        return render(request, 'hero/gu_comp.html',  {'data_cctv':data_cctv, 'data_rate': data_rate})

        # elif request.method == 'Chart':
            
            
            
            
            
            
            
        #     return render(request, 'hero/gu_chart_3.html',{"gu_chart_3":'data:;base64,{}'.fromat(img_url)})




    
@csrf_exempt
def gu_chart_1(request):
    if request.method == 'GET':
        return render(request, 'hero/gu_chart_1.html')


@csrf_exempt
def gu_chart_2(request):
    if request.method == 'GET':
        return render(request, 'hero/gu_chart_2.html')


@csrf_exempt
def gu_chart_3(request):
    if request.method == 'GET':
        return render(request, 'hero/gu_chart_3.html')



