from django.db import models

class BaseField(models.Model):
    
    createtime = models.DateTimeField('创建日期',auto_now_add=True)
    modifytime = models.DateTimeField('修改日期',auto_now=True)
    remark = models.CharField("备注",max_length=255,null=True,blank=True)

    class Meta:
        abstract = True