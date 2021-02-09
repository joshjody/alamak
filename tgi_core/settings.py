# from flask import Flask
# import jwt, datetime
#
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///databse.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'igUGIG73H(HD@(YS(Sh9hd20XHS)U@)#*)$&&DVB'

# app.run(debug=True, port=10000)

from flask import Flask, request
# import bcrypt, jwt, datetime, urllib
import jwt, datetime, urllib
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy.exc import IntegrityError
import pymysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mydata.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://.\SQLEXPRESS:""@localhost/flaskdb'
# app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://SQLEXPRESS/flaskdb?driver=SQL+Server?trusted_connection=yes"
# params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=.\SQLEXPRESS;DATABASE=localdb_pgn;Trusted_Connection=yes;')
# params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=103.10.223.172;UID={sa};PWD={Pgascom2018};DATABASE=collpertagas;')

# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tgidb2021'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'igUGIG73H(HD@(YS(Sh9hd20XHS)U@)#*)$&&DVB'
jwt = JWTManager(app)
