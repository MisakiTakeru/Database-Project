import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'DIKUDatabase.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('DIKUDATABASE_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')





#add a user
@app.route('/add', methods=['POST'])
def add_user():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute("""'insert into users (name) values (?)', 
	[request.form['name]]""")
	db.commit()
	flash('New user created')

#add a course
@app.route('/add', methods=['POST'])
def add_course():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute("""'insert into course (name, total_hours) values (?,?)', 
	[request.form['name], request.form['total_hours]]""")
	db.commit()
	flash('New course created')	

#add user to course
@app.route('/add', methods=['POST'])
def teach():
#also needs supervisor log in here through or statement
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute("""'insert into teaches (hours,Uid,Cid) values (?,?,?)',
	[request.form['hours'], request.form['Uid'], request.form['Cid']]""")
	db.commit()
	flash('user successfully added to course')

@app.route('/add', methods=['POST'])
def add_role():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute("""'insert into roles (roles,hours,Uid) values (?,?,?)',
	[request.form['roles'], request.form['hours'], request.form['Uid']]""")
	db.commit()
	flash('role successfully added to User')

# show courses
@app.route('/')
def show_courses():
	db = get_db()
	show = db.execute('select name, text from courses order by id desc')
	courses = show.fetchall()
	return render_template('show_courses.html', entries=entries)
