from django.db import models

# Create your models here.

class pretty(models.Model):
    objects  = models.Manager() #vs code 오류 제거용

    id      = models.AutoField(primary_key=True)
    na      = models.CharField(max_length=200)
    ag      = models.CharField(max_length=200)
    pw      = models.CharField(max_length=200)
    # content = models.TextField() 
    # writer  = models.CharField(max_length=50)
    # hit     = models.IntegerField()
    # img     = models.BinaryField(null=True) #바이너리 필드
    # regdate = models.DateTimeField(auto_now_add=True)

# [DB 테이블 생성]
# $ python manage.py check
# $ python manage.py makemigrations board
# $ python manage.py migrate board