# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 13:43:47 2020

@author: Tejas
"""


from flask import Flask, Response, render_template,flash,request,url_for,redirect
from camera import VideoCamera
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

import cv2


app = Flask(__name__)

app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root''@localhost/sih'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

class Demo1(db.Model):
    sr_no = db.Column(db.Integer, primary_key = True)
    vehicle = db.Column(db.String(100))
    #color = db.Column(db.String(100))
    location = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))

    def __init__(self,sr_no,vehicle,location,date,time):
        self.sr_no = sr_no
        self.vehicle = vehicle
        #self.color = color
        #self.number_plate = number_plate
        self.location = location
        self.date = date
        self.time = time

@app.route('/')
def Home():
    return render_template('home.html')



@app.route('/data')
def index():
    all_data = Demo1.query.all()
    return render_template('homehey.html', databases = all_data)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed_display')
def video_feed_display():
    return render_template('video_cam_error.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/search', methods=['GET','POST'])
# def Search():
#     if request.methods == "POST":
#         form = request.form
#         searchTerm = form['searchBox']
#         search = "%{}%".format(searchTerm)
#         searchResult = Demo1.query.filter(Demo1.)

#
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sih"

        )
#
#
#         # new method
#
#         result1 = request.form
#         result2 = request.form
#         result3 = request.form
#         result4 = request.form
#         name = result1['vehicle']
#         location = result2['location']
#         date = result3['date']
#         time = result4['time']
#         mycursor = db.cursor()
#         mycursor.execute(
#             "select * from demo1 where vehicle LIKE '%" + name + "%' OR location LIKE '%" + location + "%' OR date LIKE '%" + date + "%' OR time  LIKE '%" + time + "%'")
#         myresult = mycursor.fetchall()
#         db.commit()
#         mycursor.close()
#         return render_template("search1.html", r=myresult)



        # old method

        mycursor=db.cursor()
        result=request.form
        name=result['search']

        mycursor.execute("select * from demo1 where vehicle LIKE '%"+name+"%'OR location LIKE '%" + name + "%' OR date LIKE '%" + name +"%' OR time  LIKE '%" + name + "%'")
        myresult = mycursor.fetchall()
        db.commit()
        mycursor.close()
        return render_template("search.html", r=myresult)

        #c.executemany('''select * from demo1 where vehicle LIKE %varibalename%' '', request.form['search'])
        #return render_template("search.html", records=c.fetchall())

       # c.execute("SELECT vehicle FROM demo1")

       # myresult = c.fetchall()

        #for x in myresult:
        #    print(x)
    #return render_template('search.html', myresult= )


@app.route('/search1', methods=['GET', 'POST'])
def search1():

  if request.method == "GET":

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sih"

        )
 #
 #
 #        # new method
 #
        value = request.form
        vehicle = value["vehicle"]
        location = value["location"]
        date = value["date"]
        time = value["time"]
        dbcursor = db.cursor()
        dbcursor.execute("select * from demo1 where vehicle LIKE '%" + vehicle + "%' OR location LIKE '%" + location + "%' OR date LIKE '%" + date + "%' OR time  LIKE '%" + time + "%'")
        myvalue = dbcursor.fetchall()
        db.commit()
        dbcursor.close()
        return render_template("search1.html", a=myvalue)

  #else:

     # return render_template("search1.html")



if __name__ == '__main__':
    app.run(host='localhost', debug=True)
