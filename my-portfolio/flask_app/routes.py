# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context, send_from_directory
from flask import jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()



#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x = random.choice(['I have two middle names and they start with W and E so my initials spell my name: O.W.E.N.','I taught myself how to play the piano','My aunt is a Full Stack Developer'])
	return render_template('home.html', fun_fact = x)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    name = request.form['name']
    email = request.form['email']
    comment = request.form['comment']
    db.insertRows('feedback', ['name', 'email', 'comment'], [[name, email, comment]])
    all_feedback=db.query("SELECT * FROM feedback")
    return render_template('processfeedback.html', feedback=all_feedback)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
