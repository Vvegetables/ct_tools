from django.core.management.base import BaseCommand
from django.db import connections
from openpyxl.workbook.workbook import Workbook

class Command(BaseCommand):
    help = " download data to a file via sql statement or script"
    
    def add_arguments(self, parser):
        parser.add_argument("-s", "--script", dest="script", metavar="select * from table")
        parser.add_argument("-t", "--ext", dest="file_ext", choices=["xlsx"], default="xlsx")
        parser.add_argument("-n", "--name", dest="file_name", default="data")
        parser.add_argument("-d", "--db", dest="db_name", default="default")
        
    def handle(self, *args, **options):
        script_: str = options.get("script")
        file_ext: str = options.get("file_ext")
        file_name: str = options.get("file_name")
        db_name: str = options.get("db_name")
        
        connection_ = connections[db_name]
        with connection_.cursor() as cur:
            cur.execute(script_)
            result = self._dict_fetch_all(cur)
            if file_ext == 'xlsx':
                self._xlsx_save(result, file_name)
            
    def _dict_fetch_all(self, cursor):
        """return all rows from a cursor as a dict"""
        desc: list = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]
    
    def _xlsx_save(self, result: [dict], file_name: str):
        """data is saved in excel format"""
        wb = Workbook()
        sheet = wb.active
        for i, ldict in enumerate(result, 1):
            if i == 1:
                title_list: list = list(ldict.keys())
                sheet.append(title_list)
            sheet.append(list(ldict.values()))
        wb.save(fr"{file_name}.xlsx")