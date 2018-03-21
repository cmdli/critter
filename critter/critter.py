
from flask import Flask, g, session, request, redirect, url_for, render_template, abort
import sqlite3
import os
import random

## App Setup

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'critter.db'),
))
app.config.from_pyfile('secret.cfg', silent=True)
print('Config: ' + str(app.config))

import database
import users

@app.before_request
def session_length():
    session.permanent = True # Default to 31 days expiration

@app.errorhandler(401)
def unauthorized_response():
    return redirect('/')

## Endpoints

@app.route('/')
def main():
    db = database.get_db()
    if users.is_logged_in():
        print(users.current_user_id())
        tweets = db.execute('select poster_id,poster_name,text from tweets ' +
                         'inner join (select * from follows where follower=?) on followed=poster_id',
                         [users.current_user_id()]).fetchall()
        return render_template('feed.html', tweets=tweets)
    else:
        cur = db.execute('select poster_id,poster_name,text from tweets')
        tweets = cur.fetchall()
        return render_template('feed.html', tweets=tweets)

@app.route('/p/<userid>')
def profile(userid):
    user = users.get_user_info(userid)
    db = database.get_db()
    tweets = db.execute('select poster_name,text from tweets where poster_id=?',[userid]).fetchall()
    followed = False
    if users.is_logged_in():
        followed = db.execute('select * from follows where follower=? and followed=?',
                            [users.current_user_id(),userid]).fetchone() is not None
    return render_template('profile.html', user=user, tweets=tweets, followed=followed)

@app.route('/login', methods=['GET','POST'])
def login():
    if users.is_logged_in():
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    else: # POST
        token = request.form['token']
        if not token:
            return redirect('/login')
        if not users.login(token):
            return redirect('/login')
        else:
            return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    users.logout()
    return redirect('/')

@app.route("/add", methods=["POST"])
def add():
    if not users.is_logged_in():
        print('Could not add because user is not logged in')
        abort(401)
    user = users.current_user_info()
    db = database.get_db()
    db.cursor().execute('insert into tweets (poster_id,poster_name,text) values (?,?,?)',
                        [user['id'],user['name'],request.form['text']])
    db.commit()
    return redirect('/')

@app.route("/follow", methods=["POST"])
def follow():
    follower = users.current_user_id()
    followed = request.form.get('id')
    if follower and followed:
        db = database.get_db()
        follow = db.cursor().execute("select * from follows where follower=? and followed=?",
                                    [follower,followed]).fetchone()
        if not follow:
            db.cursor().execute('insert into follows (follower,followed) values (?,?)',
                                [follower,followed])
            db.commit()
    if followed:
        return redirect('/p/' + followed)
    else:
        return redirect('/')

@app.route('/unfollow', methods=['POST'])
def unfollow():
    follower = users.current_user_id()
    followed = request.form.get('id')
    if follower and followed:
        db = database.get_db()
        db.execute('delete from follows where follower=? and followed=?',[follower,followed])
        db.commit()
    if followed:
        return redirect('/p/' + followed)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run()
