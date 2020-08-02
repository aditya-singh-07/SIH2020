import cv2
#from model import Vehicle_recog_model
from keras.models import model_from_json, load_model
from keras.preprocessing import image
import numpy as np
import os
import datetime
import tensorflow as tf
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sih"

)



config = tf.compat.v1.ConfigProto(gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model= model_from_json(open('model_bw.json').read())
model.load_weights('my_model_weights.h5')
Cam_Name = "Cam-01"
vehile_List = {0 : 'Bajaj Pulsar NS200', 1 : 'Hero Glamour', 2 : 'Hero Passion Pro 110', 3 : 'Hero Splendor', 4 : 'Honda Activa 6G', 5 : 'Honda City', 6 : 'Honda Shine', 7 : 'Hyundai Creta', 8 : 'KTM 200 Duke', 9 : 'KTM RC 200', 10 : 'MG Hector',  11 : 'Mahindra Centuro',  12 : 'Mahindra Scorpio',  13 : 'Mahindra XUV300',  14 : 'Maruti Suzuki Baleno', 15 : 'Maruti Suzuki Celerio', 16 : 'Maruti Suzuki Ciaz', 17 : 'Maruti Suzuki Ertiga', 18 : 'Maruti Suzuki Swift', 19 : 'Maruti Suzuki Vitara Brezza',  20 : 'Maruti Suzuki Wagon R',  21 : 'Renault Duster',  22 : 'Renault Kwid', 23 : 'Royal Enfield Classic 350',  24 : 'Royal Enfield Continental GT 650',  25 : 'Royal Enfield Himalayan', 26 : 'Royal Enfield Interceptor 650', 27 : 'Royal Enfield Thunderbird 350X', 28 : 'Suzuki Access 125', 29 : 'Suzuki Burgman Street 125', 30 : 'Suzuki Gixxer', 31 : 'Suzuki Gixxer SF', 32 : 'Suzuki Intruder 150' , 33 : 'TVS Apache RR310', 34  : 'TVS Apache RTR 160 4V', 35 : 'TVS Apache RTR 200 4V', 36 : 'TVS Jupiter', 37 : 'TVS Ntorq 125', 38 : 'Tata Harrier', 39 : 'Tata Nexon', 40 : 'Toyota Fortuner', 41 : 'Toyota Innova Crysta', 42 : 'Toyota Innova Crysta', 43 : 'Yamaha FZ S V3', 44 : 'Yamaha MT 15', 45 : 'Yamaha YZF R15 V3'}

vehicle_detect = cv2.CascadeClassifier('cars.xml')
plate_cascade = cv2.CascadeClassifier('indian_license_plate.xml')
datet = datetime.datetime.now()
#model = Vehicle_recog_model("model_bw.json", "my_model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        try:
            _, fr = self.video.read()
            #gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            VD = vehicle_detect.detectMultiScale(fr, 1.17, 5)
            plate_rect = plate_cascade.detectMultiScale(fr, scaleFactor = 1.17, minNeighbors = 7)

            datet= datetime.datetime.now()

            for (x, y, w, h) in VD:
                cv2.rectangle(fr,(x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_color = fr[y:y+w, x:x+h]
                roi_color = cv2.resize(roi_color,(150, 150))
                #roi_color = image.img_to_array(roi_color)
                roi_color = np.expand_dims(roi_color, axis=0)
                roi_color =roi_color*1./255.0
                #print(roi_color)
                predictions = model.predict(roi_color)
                prediction_class = []
                for class_name,index in vehile_List.items():
                    prediction_class.append(class_name)
                max_index = np.argmax(predictions[0])
                vehicle_detected = vehile_List[max_index]
                for (lx,ly,lw,lh) in plate_rect:
                    cv2.rectangle(fr, (lx,ly), (lx+lw, ly+lh), (0, 255, 255), 2)
                    plate = fr[ly:ly+lh, lx:lx+lw]
                    plate = cv2.resize(plate,(150,150))
                    plate = image.img_to_array(plate)
                    plate = np.expand_dims(plate, axis=0)
                    plate = plate*1./255.0
                    print(plate)

                cv2.putText(fr, vehicle_detected, (int(x),int(y)), font,1, (0, 255, 255),2, cv2.LINE_AA )

                print("Date:"+datet.strftime("%x")+
                      "Time:"+datet.strftime("%X")+
                      "Place:"+Cam_Name+
                      "Vehicle Name:"+ vehicle_detected)




                mycursor = mydb.cursor()
                        #primt(tyrp)
                sql = "INSERT INTO demo1 (vehicle,location,date,time) VALUES (%(vehicle)s,%(location)s,%(date)s,%(time)s)"
                val= {'vehicle':vehicle_detected,
                      #'license_plate': license_plate,
                      #'colour': colour,
                      'location': Cam_Name,
                      'date': datet.strftime("%x"),
                      'time': datet.strftime("%X")

                      }



                mycursor.execute(sql, val)

                mydb.commit()

                print(mycursor.rowcount, "record inserted.")

            cv2.putText(fr, Cam_Name, (150,50), font, 2, (0, 255, 255),2, cv2.LINE_AA )
            cv2.putText(fr, datet.strftime("%Y/%m/%d-%H:%M:%S"), (0,390), font, 1, (0, 255, 255),2, cv2.LINE_AA )
            #cv2.putText(fr, datet.strftime("%X"), (390,390), font1, 1, (0, 255, 255),2, cv2.LINE_AA )


            _, jpeg = cv2.imencode('.jpg', fr)
            return jpeg.tobytes()
        except cv2.error as e:
            print("you have an exception",e)



