import firebase_admin
import os
from firebase_admin import auth
from flask import session

from critter import app
import critter.database as database

FIREBASE_CRED = app.config.get('FIREBASE_CRED',None)
if FIREBASE_CRED:
    cred = firebase_admin.credentials.Certificate(os.path.join(app.root_path,FIREBASE_CRED))
    firebase_admin.initialize_app(cred)
else:
    print('Error: Could not load Firebase Credentials')

def decode_login_token(token):
    try:
        decoded = auth.verify_id_token(token)
        print(decoded)
        return decoded
    except ValueError as err:
        print('Could not validate user: ' + str(err))
    return None

def create_user_if_necessary(userinfo):
    db = database.get_db()
    cursor = db.cursor()
    user = cursor.execute('select * from users where firebase_id=?',[userinfo['uid']]).fetchone()
    if user:
        return user
    cursor.execute('insert into users (firebase_id,name) values (?,?)',[userinfo['uid'],userinfo['name']])
    db.commit()
    return cursor.execute('select * from users where firebase_id=?'[userinfo['uid']]).fetchone()

def is_logged_in():
    return session.get('userid', None) is not None

def current_user_id():
    return session.get('userid')

def current_user_info():
    return get_user_info(current_user_id())

def get_user_info(userid):
    db = database.get_db()
    return db.execute('select * from users where id=?', [userid]).fetchone()

def login(token):
    userinfo = decode_login_token(token)
    if not userinfo:
        return False
    user = create_user_if_necessary(userinfo)
    session['userid'] = user['id']
    return True

def logout():
    session.pop('userid')