from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import os
import base64


def init_dbsession():
    config_dir = os.path.abspath('./configs/')
    cf = configparser.ConfigParser()
    a = config_dir + "/config.ini"
    if os.path.exists(config_dir + "/config.ini"):
        cf.read(config_dir + "/config.ini")
        secs = cf.sections()
        if "Mysql-Database" in secs:
            config_options = cf.options("Mysql-Database")
            if "host" in config_options:
                host = cf.get("Mysql-Database", "host")
                if host == '':
                    host = "localhost"
            else:
                host = "localhost"

            if "port" in config_options:
                port = cf.get("Mysql-Database", "port")
                if port == '':
                    port = "3306"
            else:
                port = "3306"

            if "user" in config_options:
                user = cf.get("Mysql-Database", "user")
                if user == '':
                    user = "root"
            else:
                user = "root"

            if "password" in config_options:
                password = cf.get("Mysql-Database", "password")
                if password == '':
                    password = "123456"
                else:
                    password = base64.b64decode(password).decode('UTF-8')
                    password = password[:-10]
            else:
                password = "123456"

            if "db_name" in config_options:
                db_name = cf.get("Mysql-Database", "db_name")
                if  db_name =='':
                    db_name = "123456"
            else:
                db_name = "competitionproject"

            DATABASE = "mysql+pymysql://" + user + ":" + password + "@" + host + ":" + port + "/" + db_name
        else:
            DATABASE = "mysql+pymysql://root:123456@localhost:3306/competitionproject"
    else:
        DATABASE = "mysql+pymysql://root:123456@localhost:3306/competitionproject"

    engine = create_engine(DATABASE, isolation_level='AUTOCOMMIT')
    DBSession = sessionmaker(bind=engine)
    return DBSession()


db_session = init_dbsession()
