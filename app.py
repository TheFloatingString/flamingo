from flask import Flask, request, render_template,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from priv.create_database import User, StressEntry
from src.api_functions import *

app = Flask(__name__)

engine = create_engine("postgres://dmguzjxxsmloic:5948608b6a121bda4af1489059dcca556334daf592af381eaf6f40add0606d5e@ec2-174-129-229-106.compute-1.amazonaws.com:5432/d49b6n4290m484", echo = True)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route("/")
def home():
	return render_template("data_entry.html")

@app.route("/create_user/<first_name>/<last_name>/<email>/<password>",
 methods=["GET", "POST"])
def create_user(first_name, last_name, email, password):
	user = User(first_name=first_name, last_name=last_name, email=email, password=password)
	session.add(user)
	session.commit()
	return 200

@app.route("/query_users", methods=["GET"])
def query_users():
	return_string = ''
	for instance in session.query(User).order_by(User.id):
		return_string += str(instance.first_name) + ' ' + str(instance.last_name) + ' ' + str(instance.email) + ' ' + str(instance.password)
		return_string += "<br>"
	return return_string

@app.route("/stress_entry", methods=["POST"])
def stress_entry():
	return render_template("data_entry.html")

@app.route("/api/add_stress_entry", methods=["POST"])
def add_stress_entry():
	print("add_stress_entry")
	json = request.get_json()

	user_id = 0
	datetime_start_str = json["start"]
	datetime_end_str = json["end"]
	stress_level = json["stress_level"]

	datetime_obj_start = datetime.strptime(datetime_start_str, '%Y-%m-%dT%H:%M:%SZ')
	datetime_obj_end = datetime.strptime(datetime_end_str, '%Y-%m-%dT%H:%M:%SZ')
	stress_entry = StressEntry(user_id=user_id, datetime_start=datetime_obj_start, datetime_end=datetime_obj_end, stress_level=stress_level)
	session.add(stress_entry)
	session.commit()
	
	return "200"

@app.route("/query_user_response")
def query_user_response():
	
	print(request.args)

	user_id = request.args.get("user_id", None)
	method = request.args.get("method", "return_all_user")

	if method=="return_all_user":
		return_json = []
		for instance in session.query(StressEntry).order_by(StressEntry.id):
			if str(user_id) == str(instance.user_id):
				return_json.append({"user_id": instance.user_id, 
					"datetime_start": instance.datetime_start, 
					"datetime_end": instance.datetime_end, 
					"stress_level": instance.stress_level})
		print(method)
		return str(return_json)	

	elif method=="total_hours":
		return_json = dict()
		total_hours = 0.0
		for instance in session.query(StressEntry).order_by(StressEntry.id):
			if str(user_id) == str(instance.user_id):
				start = datetime.strptime(instance.datetime_start, '%Y-%m-%d %H:%M:%S')
				end = datetime.strptime(instance.datetime_end, '%Y-%m-%d %H:%M:%S')

				print(type(start))

				elpased_time = end - start
				total_hours += elpased_time.total_seconds()/3600
		return_json["total_hours"] = total_hours
		return return_json

	elif method=="plot_data":
		time_counter = TimeCounter()
		return_json = dict()
		first_row = True
		for instance in session.query(StressEntry).order_by(StressEntry.datetime_start):
			if str(user_id) == str(instance.user_id):
				start = datetime.strptime(instance.datetime_start, '%Y-%m-%d %H:%M:%S')
				end = datetime.strptime(instance.datetime_end, '%Y-%m-%d %H:%M:%S')

				if first_row:
					time_counter.set_initial_day(start)
					first_row = False
				time_counter.add_row(start, end, int(instance.stress_level))

		data, pointBackgroundColor = time_counter.return_data()
		print(data)
		print(pointBackgroundColor)
		return render_template("view_data.html", data=data, pointBackgroundColor=pointBackgroundColor)


@app.route("/view_data", methods=["GET"])
def view_data():
	return render_template("view_data.html")

if __name__ == '__main__':
	app.run(debug=True)