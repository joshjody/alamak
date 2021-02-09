import sys
import os
import datetime

from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy.dialects import postgresql
# from sqlalchemy.dialects import mysql
# from sqlalchemy.dialects import mssql
# from sqlalchemy.dialects.mssql import
# from sqlalchemy.dialects.mssql import BIGINT
# from sqlalchemy.dialects.mssql import DATETIME
# from sqlalchemy.dialects.mssql import DATE
# from sqlalchemy.dialects.mssql import VARCHAR
# from sqlalchemy.dialects.mssql import NUMERIC
# from sqlalchemy.dialects.mssql import INTEGER

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


from settings import *

db = SQLAlchemy(app)
db.init_app(app)

#### Model ####

class User(db.Model):
    __tablename__   = 'User'
    id                  = db.Column(db.Integer, primary_key=True)
    nama                = db.Column(db.String(30), nullable=False)
    username            = db.Column(db.String(30), nullable=False)
    email               = db.Column(db.String(30), nullable=False)
    password            = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User {self.nama},{self.username},{self.email},{self.password}>'

class Management(db.Model):
    __tablename__   = 'Management'
    id                  = db.Column(db.Integer, primary_key=True)
    gambar              = db.Column(db.String(300), unique=True, nullable=False)
    nama                = db.Column(db.String(60), nullable=False)
    jabatan             = db.Column(db.String(60), nullable=False)
    status              = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User {self.gambar},{self.nama},{self.jabatan},{self.status}>'
#### Schema ####

class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    id          = fields.Number(dump_only=True)
    name        = fields.String(required=True)
    username    = fields.String(required=True)
    email       = fields.String(required=True)
    password    = fields.String(required=True)

class ManagementSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Management
        sqla_session = db.session
    id          = fields.Number(dump_only=True)
    gambar      = fields.String(required=True)
    nama        = fields.String(required=True)
    jabatan     = fields.String(required=True)
    status      = fields.String(required=True)
