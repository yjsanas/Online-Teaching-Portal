from django.db import models

# Create your models here.
class courseinfo(models.Model):
    cid=models.IntegerField(primary_key=True)
    cname=models.IntegerField(null=False)
    cinfo=models.TextField(null=False)

