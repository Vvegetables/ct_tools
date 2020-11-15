"""
动态设置db_table、app_label
"""

from django.db import models


class DynamicBase(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def setDB_table(cls, tableName, appLabel):
        class Meta:
            db_table = tableName
            app_label = appLabel

        attrs = {
            '__module__': cls.__module__,
            'Meta': Meta
        }
        return type(tableName, (cls, ), attrs)