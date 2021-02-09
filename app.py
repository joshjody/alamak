import json
import time
import sys
import os
import datetime
#baru
# import bcrypt
import urllib
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import jsonify, abort, send_from_directory

# from flask_mail import Mail
# from flask_mail import Message

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from marshmallow_sqlalchemy import ModelSchema
from marshmallow            import fields

from werkzeug.utils import secure_filename

sys.path.append("tgi_core")
sys.path.append("tgi_modules")
sys.path.append("tgi_modules/module_view")
sys.path.append("tgi_modules/module_cms")

from tgi_core                       import tgidb
from module_view                    import view_index
from module_cms                     import view_cms


app = Flask(__name__)

app.config['SECRET_KEY']    = 'iasdasd3ewq8hsi)U@)#*)$&&DVB'

ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg','pdf'])
app.config['UPLOAD_FOLDER']    = 'static'

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'dummy@dummy.com'#'bagiberkah17@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dummy'#'pH9xknnS#2v$#U8'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

##############halaman depan ###################

@app.route('/', methods=['GET'])
def indexview():
    reg = view_index.front_view().index()
    return reg

@app.route('/company-in-brief', methods=['GET'])
def company_in_briefview():
    reg = view_index.front_view().company_in_brief()
    return reg

@app.route('/company-in-brief-send-mail', methods=['GET','POST'])
def company_in_briefview_send_mail():
    # target ='dummy1@dummy.com'
    # msg = Message('Hello', sender=('no-reply', 'noreply@gmail.com'), recipients = [target])
    # msg.body = ""
    # msg.html = '<b>Anda mempunyai 1 notifikasi mailbox pada web tgi</b>'
    # mail.send(msg)
    reg = view_index.front_view().company_in_briefview_send_mail()
    return reg

@app.route('/operation-services', methods=['GET'])
def operation_servicesview():
    reg = view_index.front_view().operation_services()
    return reg

@app.route('/corporate-activity', methods=['GET'])
def corporate_activityview():
    reg = view_index.front_view().corporate_activity()
    return reg

@app.route('/investor-relations', methods=['GET'])
def investor_relationsview():
    reg = view_index.front_view().investor_relations()
    return reg

@app.route('/become-our-customer', methods=['GET'])
def become_our_customerview():
    reg = view_index.front_view().become_our_customer()
    return reg

@app.route('/information', methods=['GET'])
def informationview():
    reg = view_index.front_view().information()
    return reg

@app.route('/news/<id>', methods=['GET'])
def newsreadview(id):
    params = {"id" : id}
    reg = view_index.front_view().news(params)
    return reg

@app.route('/contact', methods=['GET'])
def contactview():
    reg = view_index.front_view().contact()
    return reg

@app.route('/legal-disclaimer', methods=['GET'])
def legal_disclaimer():
    reg = view_index.front_view().legal_disclaimer()
    return reg

@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    reg = view_index.front_view().privacy_policy()
    return reg

@app.route('/copyright', methods=['GET'])
def copyright():
    reg = view_index.front_view().copyright()
    return reg

################ cms ########################

@app.route('/tgi_cms/login', methods=['GET'])
def tgi_cmsview():
    log = view_cms.front_view().tgi_cms_login()
    return log

@app.route('/tgi_cms/login_proc', methods=['GET','POST'])
def login_proc():
    log = view_cms.front_view().login_proc()
    return log

@app.route('/tgi_cms/index', methods=['GET'])
def tgi_cms_indexview():
    reg = view_cms.front_view().tgi_cms_index()
    return reg

@app.route('/tgi_cms/management', methods=['GET','POST'])
def tgi_cms_managementview():
    reg = view_cms.front_view().tgi_cms_management()
    return reg

@app.route('/tgi_cms/management/edit/<id>', methods=['GET'])
def tgi_cms_managementeditview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_management_edit(params)
    return reg

@app.route('/tgi_cms/management/create', methods=['GET'])
def tgi_cms_managementcreateview():
    reg = view_cms.front_view().tgi_cms_management_create()
    return reg

@app.route('/tgi_cms/management/create_proc', methods=['GET','POST'])
def tgi_cms_managementcreateprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename}
    reg = view_cms.front_view().tgi_cms_management_create_proc(params)
    return reg

@app.route('/tgi_cms/management/edit_proc', methods=['GET','POST'])
def tgi_cms_managementeditprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename}
    reg = view_cms.front_view().tgi_cms_management_edit_proc(params)
    return reg

@app.route('/tgi_cms/management/delete/<id>', methods=['GET','POST'])
def tgi_cms_managementdeleteview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_management_delete(params)
    return reg

@app.route('/tgi_cms/news', methods=['GET','POST'])
def tgi_cms_newsview():
    reg = view_cms.front_view().tgi_cms_news()
    return reg

@app.route('/tgi_cms/news/create', methods=['GET'])
def tgi_cms_newscreateview():
    reg = view_cms.front_view().tgi_cms_news_create()
    return reg

@app.route('/tgi_cms/news/create_proc', methods=['GET','POST'])
def tgi_cms_newscreateprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename}
    reg = view_cms.front_view().tgi_cms_news_create_proc(params)
    return reg

@app.route('/tgi_cms/news/edit/<id>', methods=['GET'])
def tgi_cms_newseditview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_news_edit(params)
    return reg

@app.route('/tgi_cms/news/edit_proc', methods=['GET','POST'])
def tgi_cms_newseditprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename}
    reg = view_cms.front_view().tgi_cms_news_edit_proc(params)
    return reg

@app.route('/tgi_cms/news/delete/<id>', methods=['GET','POST'])
def tgi_cms_newsdeleteview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_news_delete(params)
    return reg

@app.route('/tgi_cms/annualreport', methods=['GET','POST'])
def tgi_cms_annualreportview():
    reg = view_cms.front_view().tgi_cms_annualreport()
    return reg

@app.route('/tgi_cms/annualreport/create', methods=['GET'])
def tgi_cms_annualreportcreateview():
    reg = view_cms.front_view().tgi_cms_annualreport_create()
    return reg

@app.route('/tgi_cms/annualreport/create_proc', methods=['GET','POST'])
def tgi_cms_annualreportcreateprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
                pdf = request.files['pdf']
                if pdf and allowed_file(pdf.filename):
                    pdfname = secure_filename(pdf.filename)
                    pdf.save(os.path.join(app.config['UPLOAD_FOLDER'],  pdfname))
        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename,"pdf":pdfname}
    reg = view_cms.front_view().tgi_cms_annualreport_create_proc(params)
    return reg

@app.route('/tgi_cms/annualreport/edit/<id>', methods=['GET'])
def tgi_cms_annualreporteditview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_annualreport_edit(params)
    return reg

@app.route('/tgi_cms/annualreport/edit_proc', methods=['GET','POST'])
def tgi_cms_annualreporteditprocview():
    if session.get('username_user'):
        username_user   = session.get('username_user')
        try:
             if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))

                pdf = request.files['pdf']
                print(pdf)
                if pdf and allowed_file(pdf.filename):
                    pdfname = secure_filename(pdf.filename)
                    pdf.save(os.path.join(app.config['UPLOAD_FOLDER'],  pdfname))

        except:
            fnya = 'upload gagal'
            return fnya
    else:
        f    = 'Silahkan Login Dahulu'
        fnya = redirect('/tgi_cms/login?error='+f)
        return fnya
    params = {"fn" : filename,"pdf":pdfname}
    reg = view_cms.front_view().tgi_cms_annualreport_edit_proc(params)
    return reg

@app.route('/tgi_cms/annualreport/delete/<id>', methods=['GET','POST'])
def tgi_cms_annualreportdeleteview(id):
    params = {"id" : id}
    reg = view_cms.front_view().tgi_cms_annualreport_delete(params)
    return reg


@app.route('/tgi_cms/message', methods=['GET','POST'])
def tgi_cms_messageview():
    reg = view_cms.front_view().tgi_cms_message()
    return reg

@app.route('/tgi_cms/logout', methods=['GET','POST'])
def tgi_cms_logout():
    reg = view_cms.front_view().tgi_cms_logout()
    return reg

app.run(debug=True, port=10000)
