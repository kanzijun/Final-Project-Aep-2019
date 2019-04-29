from flask import Flask, request, Response
import json

import pandas as pd

app = Flask(__name__)

columns = ['title', 'text', 'current_user', 'state']
df = pd.DataFrame(columns=columns)

@app.route('/story/start', methods=["POST"])
def start_story():
	if request.headers['Content-Type'] == 'application/json':
		arguments = request.get_json()
		title = arguments.get("title")
		text = arguments.get("text")
		current_user = arguments.get("current_user")
		state = arguments.get("state")

	df.loc[len(df)] = [title, text, current_user, state]
		
	resp = Response(json.dumps({ "title": title }), status=201, mimetype='application/json')
	return resp
	

@app.route('/story/list', methods=["GET"])
def list_stories_titles():
	resp = Response(df['title'].to_json(), status=200, mimetype='application/json')
	return resp

@app.route('/story/<title>')
def display_story(title):
	row = df.loc[df['title'] == title]
	resp = Response(row.to_json(), status=200, mimetype='application/json')
	return resp


@app.route('/story/<title>/edit', methods=["PUT"])
def edit_story(title):

	row = df.loc[df['title'] == title]

	if request.headers['Content-Type'] == 'application/json':
		arguments = request.get_json()
		title = arguments.get("title")
		new_text = arguments.get("new_text")
		current_user = arguments.get("current_user")
		state = arguments.get("state")

	old_text = row['text']

	text = old_text + new_text
	# row = [title, text, current_user, state]
	# df.replace({'text' : { old_text : text}}, {'current_user': {}})

	df.loc[df.title==title, ['text', 'current_user', 'state']] = [text, current_user, state] #this causes the object type series not json serializable problem

	# row = [text, current_user, state]
# 
	# df2 = pd.DataFrame({'title': title, 'text': text, 'current_user': current_user, 'state': state}, index=[0])
	# df.set_index('title', inplace=True)
	# df2.set_index('title', inplace=True)
	# df.update(df2)

	# new_row = df.loc[df['title']==title]

	row = df.loc[df['title'] == title]
	
	resp = Response(row.to_json(), status=201, mimetype='application/json')
	# resp = Response(row.to_json(), status=201, mimetype='application/json')
	return resp

@app.route('/story/<title>/end', methods=["PUT"])
def end_story(title):
	
	df.loc[df.title==title, ['state']] = 0
	row = df.loc[df['title'] == title]
	resp = Response(row.to_json(), status=201, mimetype='application/json')
	return resp

# @app.route('/story/<title>/leave')