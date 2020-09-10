from flask import Flask
from flask import Flask, render_template, redirect, url_for, request
import RPi.GPIO as GPIO
import time


app = Flask(__name__)

SERVOPIN = 13
FWD_LEFT=12
BCK_LEFT=16
FWD_RIGHT=7
BCK_RIGHT=8
MOTOR_LEFT=20
MOTOR_RIGHT=25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SERVOPIN, GPIO.OUT)
GPIO.setup(FWD_LEFT, GPIO.OUT)
GPIO.setup(BCK_LEFT, GPIO.OUT)
GPIO.setup(FWD_RIGHT, GPIO.OUT)
GPIO.setup(BCK_RIGHT, GPIO.OUT)
GPIO.setup(MOTOR_LEFT, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT,GPIO.OUT)

GPIO.output(FWD_LEFT , 0)
GPIO.output(BCK_LEFT , 0)
GPIO.output(FWD_RIGHT, 0)
GPIO.output(BCK_RIGHT, 0)

SERVO = GPIO.PWM(SERVOPIN, 50) # GPIO 17 for PWM with 50Hz
SERVO.start(0)

LEFT_SPEED = GPIO.PWM(MOTOR_LEFT,100)
LEFT_SPEED.start(0)

RIGHT_SPEED = GPIO.PWM(MOTOR_RIGHT,100)
RIGHT_SPEED.start(0)



@app.route("/")
def index():
    return render_template('robot.html')

@app.route('/forward',methods = ['POST'])
def forward():
    up_side()
    
    motorLeft = request.form['leftSpeed']
    motorRight = request.form['rightSpeed']
    
    speed(motorLeft,motorRight)
    return 'true'
    
@app.route('/backward', methods = ['POST'])
def backward():
    down_side()
    
    motorLeft = request.form['leftSpeed']
    motorRight = request.form['rightSpeed']
    
    speed(motorLeft,motorRight)
    return 'true'
    
def up_side():
   GPIO.output(FWD_LEFT , 1)
   GPIO.output(BCK_LEFT , 0)
   GPIO.output(FWD_RIGHT , 1)
   GPIO.output(BCK_RIGHT , 0)
   return 'true'

def down_side():

   GPIO.output(FWD_LEFT , 0)
   GPIO.output(BCK_LEFT , 1)
   GPIO.output(FWD_RIGHT , 0)
   GPIO.output(BCK_RIGHT , 1)
   return 'true'

@app.route('/stop' , methods = ['POST'])
def stop():
   GPIO.output(FWD_LEFT , 0)
   GPIO.output(BCK_LEFT , 0)
   GPIO.output(FWD_RIGHT , 0)
   GPIO.output(BCK_RIGHT , 0)
   speed(0,0)
   return  'true'

@app.route('/servoposition', methods =['POST'])
def servoposition():
    slider1 = request.form['slider1']
    servoAngle(slider1)
    return 'true'

def servoAngle(angle):
    SERVO.ChangeDutyCycle(float(angle))
    time.sleep(0.03)
    SERVO.ChangeDutyCycle(0)
    return
            
    
   
def speed(left,right):
    sLeft = float(left)
    sRight = float(right)
    LEFT_SPEED.ChangeDutyCycle(sLeft)
    RIGHT_SPEED.ChangeDutyCycle(sRight)
    
if __name__ == "__main__":
 print "Start"
 app.run(host='adelene.local',port=5010)


