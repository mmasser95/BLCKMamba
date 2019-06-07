from db import dbcon
from services import services
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


def main():
    conn=dbcon()
    serv=services(conn)
    print(conn.verTablas())
    print(conn.getGrupos())
    print(conn.getUsersGrupo('Admin'))
    print(conn.getUser(conn.login(('admin','admin'))))

if __name__ == "__main__":
    main()