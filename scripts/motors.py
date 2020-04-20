#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Mohammad-AlYasfo

import RPi.GPIO as GPIO
import math, time
from Config import *

class DCMotors():

    def __init__(self, IN1, IN2, IN3, IN4, DC1, DC2, IN5, IN6, IN7, IN8, DC3, DC4, enc_R, enc_L, IR):
        GPIO.setup(IR, GPIO.IN) # pull_up_down=GPIO.PUD_DOWN
        GPIO.setup(enc_L, GPIO.IN) # pull_up_down=GPIO.PUD_DOWN
        GPIO.setup(enc_R, GPIO.IN) # pull_up_down=GPIO.PUD_DOWN
        GPIO.add_event_detect(IR,GPIO.RISING, callback=self.Infra_distance)
        self.safe_moving = True
        self.edges = {'right':[],'left':[]}
        GPIO.add_event_detect(enc_R,GPIO.RISING, callback=self.right_encoder)
        GPIO.add_event_detect(enc_L,GPIO.RISING, callback=self.left_encoder)
        self.last_right_edge = 0
        self.last_left_edge = 0
        self.MotorA={'IN1':IN1,'IN2':IN2,'DC':DC1}
        self.MotorB={'IN3':IN3,'IN4':IN4,'DC':DC2}
        self.MotorC={'IN5':IN5,'IN6':IN6,'DC':DC3}
        self.MotorD={'IN7':IN7,'IN8':IN8,'DC':DC4}
        self.currentSpeed=0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.MotorA["IN1"], GPIO.OUT)
        GPIO.setup(self.MotorA["IN2"], GPIO.OUT)
        GPIO.setup(self.MotorA["DC"], GPIO.OUT)
        GPIO.setup(self.MotorB["IN3"], GPIO.OUT)
        GPIO.setup(self.MotorB["IN4"], GPIO.OUT)
        GPIO.setup(self.MotorB["DC"], GPIO.OUT)
        GPIO.setup(self.MotorC["IN5"], GPIO.OUT)
        GPIO.setup(self.MotorC["IN6"], GPIO.OUT)
        GPIO.setup(self.MotorC["DC"], GPIO.OUT)
        GPIO.setup(self.MotorD["IN7"], GPIO.OUT)
        GPIO.setup(self.MotorD["IN8"], GPIO.OUT)
        GPIO.setup(self.MotorD["DC"], GPIO.OUT)

        self.SpeedA = GPIO.PWM(self.MotorA["DC"],DC_FREQ)
        self.SpeedB = GPIO.PWM(self.MotorB["DC"],DC_FREQ)
        self.SpeedC = GPIO.PWM(self.MotorC["DC"],DC_FREQ)
        self.SpeedD = GPIO.PWM(self.MotorD["DC"],DC_FREQ)
        self.SpeedA.start(self.currentSpeed)
        self.SpeedB.start(self.currentSpeed)
        self.SpeedC.start(self.currentSpeed)
        self.SpeedD.start(self.currentSpeed)
        self.data={}

    def Infra_distance(self,channel):
        self.safe_moving = not self.safe_moving
        if not self.safe_moving:
            self.stop()
        pass

    def left_encoder(self,channel):
        duration = min(time.time() - self.last_left_edge,0)
        self.edge_append('left',duration)
        pass

    def right_encoder(self,channel):
        now = time.time()
        duration = min(now - self.last_right_edge,0)
        self.edge_append('right',duration)
        self.last_right_edge = now
        pass

    def edge_append(self,direction,value):
        if len(self.edges['left']) > MAX_EDGES_LEN or len(self.edges['right']) > MAX_EDGES_LEN:
            self.edges['left'] = []
            self.edges['right'] = []
        else:
            self.edges[direction].append(value)
        pass

    def get_velocity(self):
        # get the median to avoid outliers of values in both lists
        median_left = sorted(self.edges['left'])[int(len(self.edges['left'])/2)-1]
        median_right = sorted(self.edges['right'])[int(len(self.edges['right'])/2)-1]
        # velocity = step_length * time difference
        velocity = STEP_ENGTH * (median_left - median_right)/2
        return velocity
        pass

    def stop(self):
        data={'IN1':0,'IN2':0,'IN3':0,'IN4':0,'IN5':0,'IN6':0,'IN7':0,'IN8':0}
        self.motors.setData(data)

    def setData(self, data):

        if(self.data!=data):
            GPIO.output(self.MotorA["IN1"], data["IN1"])
            GPIO.output(self.MotorA["IN2"], data["IN2"])
            GPIO.output(self.MotorB["IN3"], data["IN3"])
            GPIO.output(self.MotorB["IN4"], data["IN4"])
            GPIO.output(self.MotorC["IN5"], data["IN5"])
            GPIO.output(self.MotorC["IN6"], data["IN6"])
            GPIO.output(self.MotorD["IN7"], data["IN7"])
            GPIO.output(self.MotorD["IN8"], data["IN8"])
            self.data=data

    def setVelocity(self,speed):
        if(math.fabs((self.currentSpeed-speed))>MIN_SPEED_CHANGE):
            self.SpeedA.ChangeDutyCycle(speed)
            self.SpeedB.ChangeDutyCycle(speed)
            self.SpeedC.ChangeDutyCycle(speed)
            self.SpeedD.ChangeDutyCycle(speed)
