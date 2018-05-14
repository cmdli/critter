
import sqlite3
import os
import random
import time
from flask import Flask, g, session, request, redirect, url_for, render_template, abort

from critter import app
import critter.users as users
import critter.database as database

@app.route('/')
def main():
    db = database.get_db()
    cur = db.execute('select poster_id,poster_name,time,text from tweets order by time')
    tweets = cur.fetchall()
    return render_template('feed.html', tweets=tweets)

@app.route('/feed')
def feed():
    if not users.is_logged_in():
        return redirect('/')
    db = database.get_db()
    print(users.current_user_id())
    tweets = db.execute('select poster_id,poster_name,time,text from tweets ' +
                        'inner join (select * from follows where follower=?) on followed=poster_id order by time',
                        [users.current_user_id()]).fetchall()
    return render_template('feed.html', tweets=tweets)

@app.route('/p/<userid>')
def profile(userid):
    user = users.get_user_info(userid)
    db = database.get_db()
    tweets = db.execute('select poster_name,time,time,text from tweets where poster_id=? order by time',[userid]).fetchall()
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
        if not token or not users.login(token):
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
    current_time = int(time.time())
    db.cursor().execute('insert into tweets (poster_id,poster_name,time,text) values (?,?,?,?)',
                        [user['id'],user['name'],current_time,request.form['text']])
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
