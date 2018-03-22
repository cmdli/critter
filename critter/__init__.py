import os
from flask import Flask, session, redirect

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'critter.db'),
))
app.config.from_pyfile('secret.cfg', silent=True)
print('Config: ' + str(app.config))

@app.before_request
def session_length():
    session.permanent = True # Default to 31 days expiration

@app.errorhandler(401)
def unauthorized_response():
    return redirect('/')

import critter.database
import critter.users
import critter.views

if __name__ == "__main__":
    app.run()