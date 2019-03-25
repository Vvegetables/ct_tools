import pymysql
from functools import wraps

def check_error(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            k = func(*args,**kwargs)
        except Exception as e:
            print(e)
            return None
        return k
    return wrapper

class PyMysqlClient:
    
    def __init__(self,host:str,user:str,password:str,db:str,port=3306,dict_cursor:bool=True,**kwargs:dict) -> None:
        self.db = pymysql.connect(host,user,password,db,port,**kwargs)
        self.DICT_CURSOR_FLAG = dict_cursor
        self.dict_cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        self.sequence_cursor = self.db.cursor()
        
        self.cursor = self.dict_cursor if dict_cursor else self.sequence_cursor
        
        self.results = []
        self.sql = None
    
    #(select and insert) sql
    def _generate_sql(self,tablename:str,fields:list=None,
        values:list=None,_filter:str=None,order_by:list=None,distinct=None,
        limit:list=None,group_by=False) -> str:
        '''
            tablename : table name of db
            fields : the fields of table
            values : the values of fields
            _filter : the values of sql's where
            order_by : the segment of order by
            distinct : 
            group_by : include the select value of mysql func 
        '''
        sql = []
        if not fields:
            fields = "*"
        else:
            if not isinstance(fields,list):
                raise TypeError("fields 字段类型必须是list")
            else:
                fields = ",".join(map(lambda x:'`'+x+'`',fields))
        
        #choose select or insert dely on values
        if not values:
            sql.append("SELECT ")
        else:
            sql.append("INSERT INTO ")
        
        #check distinct is True or False
        if distinct:
            sql.append(' DISTINCT ')
        
        #choose select or insert dely on values
        if not values:
            sql.append(f' {fields} FROM {tablename}')
        else:
            values_ = ','.join(map(lambda x:"'" + str(x) + "'", values))
            sql.append(f' {tablename}({fields}) VALUES({values_}) ')
        
        if _filter:
            if isinstance(_filter,str):
                sql.append(f' WHERE {_filter} ')
            else:
                raise TypeError("_filter 字段必须是str")
        
        if order_by:
            if isinstance(order_by,list):
                order_by_data = ",".join(order_by)
                sql.append(f" ORDER BY {order_by_data}")
            else:
                raise TypeError("order_by 字段必须是list")
        
        if limit:
            if isinstance(limit,list):
                if len(limit) > 1:
                    sql.append(f" LIMIT {limit[0]},{limit[1]}")
                else:
                    sql.append(f" LIMIT {limit[0]}")
            else:
                raise TypeError("limit 字段必须是list")
        
        self.sql = "".join(sql)

        return self.sql
    
    #select query
    def query(self,tablename:str,fields:list=None,_filter:list=None,
        limit:list=None,order_by:list=None,distinct:bool=False,group_by:bool=False):
        
        sql = self._generate_sql(tablename, fields=fields, _filter=_filter, limit=limit, order_by=order_by, group_by=group_by, distinct=distinct)
        self.cursor.execute(sql)
        temp = self.cursor.fetchall() 
        self.results = []
        for t in temp:
            self.results.append(t)
    
    #insert
    def insert(self,tablename,values,fields=None):
        try:
            sql = self._generate_sql(tablename, fields=fields, values=values)
            self.cursor.execute(sql)
            self.db.commit()
            print('插入成功')
        except Exception as e:
            self.db.rollback()
            print('插入失败',e)
    
    #batch insert       
    def batch_insert(self,tablename,values,fields=None):
        if not values:
            return 0
        sql = self._generate_sql(tablename, fields=fields, values=values[0])
        front,params = sql.split('VALUES')
        param_nums = len(params.split(','))
        sql = front + ' VALUES(' + ','.join(['%s'] * param_nums) + ') '
        n = self.cursor.executemany(sql,values)
        self.db.commit()
        return n 

    #delete
    def delete(self,tablename,_filter):
        sql = 'DELETE FROM {}'.format(tablename)
        if _filter:
            sql += ' WHERE {}'.format(_filter)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
    
    #fetch first data
    @check_error
    def fetch_first(self):
        if self.results:
            return self.results[0]
        else:
            return None 
    
    #fetch range data    
    @check_error
    def fetch_some(self,start,end):
        length = len(self.results)
        if start > length:
            start = length
        return self.results[start:end]
    
    #fetch all data
    @check_error
    def fetch_all(self):
        return self.results
    
    #pymysql exec
    def raw_exec(self,sql):
        self.cursor.execute(sql)
        self.results = self.cursor.fetchall()
#         self.results = []
#         for t in temp:
#             self.results.append(t)

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        
        self.cursor.close()
        self.db.close()
        self.results = None


if __name__ == '__main__':
    
    _connect = PyMysqlClient('47.96.253.99','ct','IhadKD#4321','innerweb')
#     _connect.query('sp_configtable')
    _connect.query('sp_configtable',fields=['link'])
    print(_connect.fetch_some(0, 2))
#     print(_connect.results)
#     print(len(_connect.fetch_all()))
#     _connect.insert('educationnews', fields=('title','link'), values=('测试','www.baidu.com'))
#     k = _connect.batch_insert('sp_configtable', fields=['title','subtitle','link','type','visited','number'], values=[[]])
#     print(k)   