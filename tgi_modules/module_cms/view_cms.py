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

    def tgi_cms_login(self):
        if session.get('username_user'):
            fnya = redirect('/tgi_cms/management')
            return fnya
        ctt = request.args.get('error')
        if ctt is None:
            cttn = " "
        else:
            cttn = ctt
        fnya =render_template('logincms.html', cttn=cttn)
        return fnya

    def login_proc(self):
        try:
            username  = request.form['Username']
            password  = request.form['Password']
            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM user where username ='"+username+"'AND password ='"+password+"'")
            myresult = mycursor.fetchone()
            if myresult:

                id       = myresult[0]
                username = myresult[1]
                fullname = myresult[2]
                email    = myresult[3]
                session['username_user']    = username
                fnya = redirect('/tgi_cms/management')
                return fnya
            else:
                f    = 'Error. Username / Password Salah'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya
        except:
            f    = 'Error. Username / Password Salah'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_logout(self):
        try:
            session.pop('loggedin', None)
            session.pop('id_user', None)
            session.pop('username_user', None)
            session.pop('email_user', None)
            session.pop('fullname', None)
            fnya = redirect('/tgi_cms/login')
            return fnya
        except:
            fnya = redirect('/tgi_cms/login')
            return fnya

    # def tgi_cms_index(self):
    #     if session.get('username_user'):
    #         username_user   = session.get('username_user')
    #         fullname        = session.get('fullname')
    #         id_user         = session.get('id_user')
    #         email_user      = session.get('email_user')
    #         fnya =render_template('indexcms.html', username_user=username_user)
    #         return fnya
    #     else:
    #         f    = 'Silahkan Login Dahulu'
    #         fnya = redirect('/tgi_cms/login?error='+f)
    #         return fnya

    def tgi_cms_management(self):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            fullname        = session.get('fullname')
            try:

                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM management")
                myresult = mycursor.fetchall()

                fnya =render_template('management.html', myresult=myresult)
                return fnya
            except:
                fnya =render_template('management.html')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_management_create(self):
        if session.get('username_user'):
            fnya =render_template('managementcreate.html')
            return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_management_create_proc(self, params):
        if session.get('username_user'):

            admin       = session['username_user']
            tanggal     = str(datetime.datetime.now())
            filename    = params["fn"]
            Gambar      ='/static/'+filename
            nama        = request.form['Nama']
            jabatan     = request.form['Jabatan']
            status      = request.form['Management']


            mydb        = tgidb.connect()
            mycursor    = mydb.cursor()
            mycursor.execute("INSERT INTO `management`(`gambar`, `nama`, `jabatan`, `status`) VALUES ('"+Gambar+"','"+nama+"','"+jabatan+"','"+status+"')")
            mydb.commit()


            mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menambahkan data management')")
            mydb.commit()
            fnya = redirect('/tgi_cms/management')
            return fnya

        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_management_edit(self, params):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            fullname        = session.get('fullname')
            id_user         = session.get('id_user')
            email_user      = session.get('email_user')
            try:
                id=params["id"]
                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM management where id ="+id)
                myresult = mycursor.fetchone()

                id = myresult[0]
                Gambar = myresult[1]
                Nama = myresult[2]
                Jabatan = myresult[3]
                Management = myresult[4]
                fnya =render_template('managementedit.html', id=id,Gambar=Gambar,Nama=Nama,Jabatan=Jabatan,Management=Management)
                return fnya
            except:
                fnya =render_template('managementedit.html')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_management_edit_proc(self, params):
        if session.get('username_user'):

            admin       = session['username_user']
            tanggal     = str(datetime.datetime.now())

            filename    =params["fn"]
            Gambar      ='/static/'+filename

            id          = request.form['id']
            Management  = request.form['Management']
            Nama        = request.form['Nama']
            Jabatan     = request.form['Jabatan']

            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE management SET Nama = '"+ Nama +"', status='"+Management+"', jabatan = '"+Jabatan+"', Gambar='"+Gambar+"' WHERE id = '"+id+"'")
            mydb.commit()
            mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','mengupdate data management')")
            mydb.commit()
            fnya = redirect('/tgi_cms/management')
            return fnya

        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_management_delete(self, params):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            try:
                admin       = session['username_user']
                tanggal     = str(datetime.datetime.now())
                id    = params["id"]
                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM `management` WHERE id="+id)
                mydb.commit()
                mycursor.execute("ALTER TABLE `management` AUTO_INCREMENT = 1")
                mydb.commit()
                mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menghapus data management')")
                mydb.commit()
                fnya = redirect('/tgi_cms/management')
                return fnya
            except:
                fnya = redirect('/tgi_cms/management')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news(self):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            try:

                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM news")
                myresult = mycursor.fetchall()
                # print(myresult)
                fnya =render_template('news.html', myresult=myresult)
                return fnya
            except:
                fnya =render_template('news.html')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news_create(self):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            fnya =render_template('newscreate.html', username_user=username_user)
            return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news_create_proc(self, params):
        if session.get('username_user'):

            admin       = session['username_user']
            tanggal     = str(datetime.datetime.now())
            filename    = params["fn"]
            Gambar      ='/static/'+filename
            Judul       = request.form['Judul']
            Isi         = request.form['Isi']
            Tanggal     = request.form['Tanggal']

            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO `news`(`gambar`, `judul`, `isi`, `tgl`) VALUES ('"+Gambar+"','"+Judul+"','"+Isi+"','"+Tanggal+"')")
            mydb.commit()
            mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menambahkan data news')")
            mydb.commit()
            fnya = redirect('/tgi_cms/news')
            return fnya

        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news_edit(self, params):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            try:
                id=params["id"]
                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM news where id ="+id)
                myresult = mycursor.fetchone()
                # print(myresult)

                id = myresult[0]
                Gambar = myresult[1]
                Judul = myresult[2]
                Isi = myresult[3]
                # print(Isi)
                Tanggal = myresult[4]
                fnya =render_template('newsedit.html', id=id,Gambar=Gambar,Judul=Judul,Isi=Isi,Tanggal=Tanggal)
                return fnya
            except:
                fnya =render_template('newstedit.html')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news_edit_proc(self, params):
        if session.get('username_user'):

            admin       = session['username_user']
            tanggal     = str(datetime.datetime.now())
            filename    = params["fn"]
            Gambar      ='/static/'+filename
            Id          = request.form['id']
            Judul       = request.form['Judul']
            Isi         = request.form['Isi']
            Tanggal     = request.form['Tanggal']

            mydb = tgidb.connect()
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE news SET judul = '"+ Judul +"', isi='"+Isi+"', gambar = '"+Gambar+"', tgl='"+Tanggal+"' WHERE id = '"+Id+"'")
            mydb.commit()
            mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','mengupdate data news')")
            mydb.commit()

            fnya = redirect('/tgi_cms/news')
            return fnya

        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_news_delete(self, params):
        if session.get('username_user'):
            username_user   = session.get('username_user')
            try:
                admin       = session['username_user']
                tanggal     = str(datetime.datetime.now())
                id    = params["id"]
                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM `news` WHERE id="+id)
                mydb.commit()
                mycursor.execute("ALTER TABLE news AUTO_INCREMENT = 1")
                mydb.commit()
                mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menghapus data news')")
                mydb.commit()
                fnya = redirect('/tgi_cms/news')
                return fnya
            except:
                fnya = redirect('/tgi_cms/news')
                return fnya
        else:
            f    = 'Silahkan Login Dahulu'
            fnya = redirect('/tgi_cms/login?error='+f)
            return fnya

    def tgi_cms_annualreport(self):
            if session.get('username_user'):
                username_user   = session.get('username_user')
                try:

                    mydb = tgidb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM annualreport")
                    myresult = mycursor.fetchall()
                    print(myresult)
                    fnya =render_template('annualreport.html', myresult=myresult)
                    return fnya
                except:
                    fnya =render_template('annualreport.html')
                    return fnya
            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_annualreport_create(self):
            if session.get('username_user'):
                username_user   = session.get('username_user')
                fnya =render_template('annualreportcreate.html', username_user=username_user)
                return fnya
            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_annualreport_create_proc(self, params):
            if session.get('username_user'):

                admin       = session['username_user']
                tanggal     = str(datetime.datetime.now())
                filename    = params["fn"]
                Gambar      ='/static/'+filename
                pdfname     = params["pdf"]
                pdf         ='/static/'+pdfname
                Judul       = request.form['Judul']

                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO `annualreport`(`gambar`, `judul`, `datapdf`) VALUES ('"+Gambar+"','"+Judul+"','"+pdf+"')")
                mydb.commit()
                mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menambahkan data annual report')")
                mydb.commit()
                fnya = redirect('/tgi_cms/annualreport')
                return fnya

            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_annualreport_edit(self, params):
            if session.get('username_user'):
                username_user   = session.get('username_user')
                try:
                    id=params["id"]
                    mydb = tgidb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM annualreport where id ="+id)
                    myresult = mycursor.fetchone()
                    print(myresult)

                    id = myresult[0]
                    Judul = myresult[1]
                    gambar = myresult[2]
                    data = myresult[3]
                    print(id)
                    print(Judul)

                    fnya =render_template('annualreportedit.html', id=id,Judul=Judul)
                    return fnya
                except:
                    fnya =render_template('annualreportedit.html')
                    return fnya
            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_annualreport_edit_proc(self, params):
            if session.get('username_user'):

                admin       = session['username_user']
                tanggal     = str(datetime.datetime.now())
                Id          = request.form['id']
                filename    = params["fn"]
                Gambar      ='/static/'+filename
                pdfname     = params["pdf"]
                pdf         ='/static/'+pdfname
                Judul       = request.form['Judul']

                mydb = tgidb.connect()
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE annualreport SET judul = '"+ Judul +"', datapdf='"+pdf+"', gambar = '"+Gambar+"' WHERE id = '"+Id+"'")
                mydb.commit()
                mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','mengupdate data annual report')")
                mydb.commit()
                fnya = redirect('/tgi_cms/annualreport')
                return fnya

            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_annualreport_delete(self, params):
            if session.get('username_user'):
                username_user   = session.get('username_user')
                try:
                    admin       = session['username_user']
                    tanggal     = str(datetime.datetime.now())
                    id    = params["id"]
                    mydb = tgidb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute("DELETE FROM `annualreport` WHERE id="+id)
                    mydb.commit()
                    mycursor.execute("ALTER TABLE annualreport AUTO_INCREMENT = 1")
                    mydb.commit()
                    mycursor.execute("INSERT INTO `log`(`username`, `tanggal`, `aktivitas`) VALUES ('"+admin+"','"+tanggal+"','menghapus data annual report')")
                    mydb.commit()
                    fnya = redirect('/tgi_cms/annualreport')
                    return fnya
                except:
                    fnya = redirect('/tgi_cms/annualreport')
                    return fnya
            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya

    def tgi_cms_message(self):
            if session.get('username_user'):
                username_user   = session.get('username_user')
                try:

                    mydb = tgidb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM mailbox")
                    myresult = mycursor.fetchall()
                    # print(myresult)
                    fnya =render_template('message.html', myresult=myresult)
                    return fnya
                except:
                    fnya =render_template('message.html')
                    return fnya
            else:
                f    = 'Silahkan Login Dahulu'
                fnya = redirect('/tgi_cms/login?error='+f)
                return fnya
