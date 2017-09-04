import MySQLdb


class Database:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host','localhost')
        self.port = kwargs.get('port',3306)
        self.user = kwargs.get('user')
        self.passwd = kwargs.get('passwd')
        self.db = kwargs.get('db')
        self.charset = kwargs.get('charset','utf8')
        self.conn = MySQLdb.connect(
                            host=self.host,
                            port=self.port,
                            user=self.user,
                            passwd=self.passwd,
                            db=self.db,
                            charset=self.charset
                        )
        self.cursor = self.conn.cursor()
        self.insert_sql = 'INSERT INTO %(table)s(%(column)s) VALUES (%(values)s)'
        self.select_sql = 'SELECT %(column)s FROM %(table)s ORDER BY id LIMIT %(_from)s,%(limit)s'

    def insert(self,**kwargs):
        sql = self.insert_sql % kwargs
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def select(self,**kwargs):
        sql = self.select_sql % kwargs
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()