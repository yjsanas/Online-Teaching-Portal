from django.db import models

# Create your models here.

class Studentlogin(models.Model):
    Sid=models.AutoField(auto_created=True,primary_key=True)
    first_name = models.CharField(null=False,max_length=255)
    last_name = models.CharField(null=False,max_length=255)
    email = models.CharField(null=False,max_length=255)
    password = models.CharField(null=False,max_length=255)


class scourse(models.Model):
    sid=models.IntegerField(null=False)
    cid=models.IntegerField(null=False)

