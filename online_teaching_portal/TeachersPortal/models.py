from django.utils import timezone
from django.db import models

# Create your models here.

class Teacherlogin(models.Model):
    Tid=models.AutoField(auto_created=True,primary_key=True)
    first_name = models.CharField(null=False,max_length=30)
    last_name = models.CharField(null=False,max_length=30)
    email = models.CharField(null=False,max_length=30)
    password = models.CharField(null=False,max_length=30)

class tcourse(models.Model):
    cid=models.AutoField(auto_created=True,primary_key=True)
    tid=models.IntegerField(null=False)
    cinfo=models.TextField(null=True)
    cname=models.TextField(null=False,default='no name')


class material(models.Model):
    mid =models.AutoField(auto_created=True,primary_key=True)
    tid=models.IntegerField(null=False)
    cid=models.IntegerField(null=True)
    mtitle=models.TextField(null=False)
    mdecription=models.TextField(null=False)
    mdocs=models.TextField(null=True)
    createdat=models.DateTimeField()
    updatedat=models.DateTimeField(default=timezone.now)

class attendance(models.Model):
    sid=models.IntegerField(default=-1)
    cid=models.IntegerField(null=False)
    tid=models.IntegerField(null=True)
    present=models.IntegerField(default=0)
    date=models.DateField()

 
class assignment(models.Model):
    Asid=models.AutoField(auto_created=True,primary_key=True)
    Atid=models.IntegerField()
    Atitle=models.TextField(null=False)
    Adec=models.TextField(null=False)
    Amarked=models.TextField(default=None)
    Atotalmark=models.TextField(default=None)
    Aduedate=models.TextField(default=None)
    Acreatedat=models.DateTimeField()
    Aupdatedat=models.DateTimeField(default=timezone.now)

class assignment_join(models.Model):
    cid=models.IntegerField(null=False)
    Aid=models.IntegerField(null=False)

class material_join(models.Model):
    cid=models.IntegerField(null=False)
    mid=models.IntegerField(null=False)
    