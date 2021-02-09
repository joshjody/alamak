import json
import mysql.connector
import requests
import os
import time
import sys
import datetime
import re
import random
from datetime import datetime,date


from flask import render_template_string
from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import send_from_directory

sys.path.append("tgi_core")
sys.path.append("tgi_core/tgidb")
sys.path.append("tgi_core/models_mysql")
sys.path.append("tgi_core/settings")


from models_mysql     import *
from settings         import *
from tgi_core         import tgidb

class front_view:

    def __init__(self):
        pass

    def index(self):
        fnya =render_template('index.html')
        return fnya

    def company_in_brief(self):
        try:
            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM management where status='Directors'")
            Directors = mycursor.fetchall()

            mycursor.execute("SELECT * FROM management where status='Commisioners'")
            Commisioners = mycursor.fetchall()

            fnya =render_template('company-in-brief.html', Directors=Directors,Commisioners=Commisioners)
            return fnya
        except:
            fnya =render_template("company-in-brief.html")
            return fnya

    def company_in_briefview_send_mail(self):
        try:
            fname       = request.form['fname']
            lname       = request.form['lname']
            email       = request.form['email']
            purpose     = request.form['purpose']
            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO `mailbox`(`first_name`, `last_name`, `email`, `purpose`) VALUES ('"+fname+"','"+lname+"','"+email+"','"+purpose+"')")
            mydb.commit()
            fnya = "sending mail berhasil"
            return fnya
        except:
            fnya = "sending gagal"
            return fnya

    def operation_services(self):
        fnya =render_template('operation-services.html')
        return fnya

    def corporate_activity(self):
        fnya =render_template('corporate-activity.html')
        return fnya

    def investor_relations(self):
        try:
            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM annualreport")
            myresult = mycursor.fetchall()
            fnya =render_template('investor-relations.html', myresult=myresult)
            return fnya
        except:
            fnya =render_template('investor-relations.html')
            return fnya

    def become_our_customer(self):
        fnya =render_template('become-our-customer.html')
        return fnya

    def information(self):
        try:
            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM `news` ORDER BY `tgl` DESC")
            myresult = mycursor.fetchall()

            fnya =render_template('information.html', myresult=myresult)
            return fnya
        except:
            fnya =render_template('information.html')
            return fnya

    def news(self, params):
        try:
            id          = params["id"]
            mydb        = tgidb.connect()
            mycursor    = mydb.cursor()
            mycursor.execute("SELECT * FROM `news` WHERE id="+id)
            myresult    = mycursor.fetchone()
            print(myresult)

            fnya =render_template('newsread.html', myresult=myresult)
            return fnya
        except:
            fnya =render_template('newsread.html')
            return fnya

    def contact(self):
        fnya =render_template('contact.html')
        return fnya

    def legal_disclaimer(self):
        fnya =render_template('legal-disclaimer.html')
        return fnya

    def privacy_policy(self):
        fnya =render_template('privacy_policy.html')
        return fnya

    def copyright(self):
        fnya =render_template('copyright.html')
        return fnya
