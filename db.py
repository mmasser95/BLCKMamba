import sqlite3
import hashlib


class dbcon():
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.curs = self.conn.cursor()
        if not self.testDB():
            print('Instalación completa')
        else:
            print('DB cargada')

    def verTablas(self):
        sql = "SELECT name FROM sqlite_master WHERE type = 'table';"
        self.curs.execute(sql)
        return self.curs.fetchall()

    def crearDB(self):
        sql = ["""
            CREATE TABLE grupos(
                name TEXT NOT_NULL,
                UNIQUE(name)
            );
        """, """
            CREATE TABLE permissions(
                verUsers INT NOT_NULL,
                verGrupos INT NOT_NULL,
                grupoId INT NOT_NULL,
                FOREIGN KEY(grupoId) REFERENCES grupos(rowid)
            );
        """, """
            CREATE TABLE users(
                username TEXT NOT_NULL,
                email TEXT NOT_NULL,
                pass TEXT NOT_NULL,
                grupoId INT NOT_NULL,
                UNIQUE(email),
                FOREIGN KEY(grupoId) REFERENCES grupos(rowid)
            );
        """,
               "INSERT INTO grupos VALUES ('Admin');",
               "INSERT INTO permissions VALUES (1,1,1);",
               "INSERT INTO users VALUES ('admin','admin','" +
               self.myMD5('admin')+"', 1);"]
        for cmd in sql:
            self.curs.execute(cmd)
        return self.conn.commit()

    def droptall(self):
        for i in self.verTablas():
            self.curs.execute("DROP TABLE "+i+";")
        return self.conn.commit()

    def testDB(self):
        l = len(self.verTablas())
        if l == 0:
            self.crearDB()
            return False
        if l != 3:
            self.droptall()
            self.crearDB()
            return False
        return True

    def getGrupos(self):
        sql = "SELECT rowid,* FROM grupos;"
        self.curs.execute(sql)
        return self.curs.fetchall()

    def getPermissions(self):
        sql = "SELECT rowid,* FROM permissions;"
        self.curs.execute(sql)
        return self.curs.fetchall()

    def getUsers(self):
        sql = "SELECT rowid,* FROM users;"
        self.curs.execute(sql)
        return self.curs.fetchall()

    def getUsersGrupo(self, nombre):
        sql="SELECT u.rowid,u.* FROM users u JOIN grupos g ON(u.grupoId=g.rowid) WHERE g.name='"+nombre+"';"
        self.curs.execute(sql)
        return self.curs.fetchall()

    def getUser(self, idd):
        sql="SELECT * FROM users WHERE rowid="+str(idd)+";"
        self.curs.execute(sql)
        return self.curs.fetchone()
    
    def login(self,data):
        sql="SELECT pass,rowid FROM users WHERE email='"+data[0]+"';"
        self.curs.execute(sql)
        rees=self.curs.fetchone()
        if self.myMD5(data[1])==rees[0]:
            return rees[1]
        return False

    @staticmethod
    def myMD5(s):
        return hashlib.md5(s.encode()).hexdigest()
