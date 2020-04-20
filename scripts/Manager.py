#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Mohammad-AlYasfo

from Config import *
from motors import DCMotors
from wierd_queue import WierdQueue
from math import *
from time import sleep
import RPi.GPIO as GPIO
import threading

class manager():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.motors=DCMotors(BOARD['MOTOR_A_IN1'],
                             BOARD['MOTOR_A_IN2'],
                             BOARD['MOTOR_B_IN1'],
                             BOARD['MOTOR_B_IN2'],
                             BOARD['MOTOR_A_ENA'],
                             BOARD['MOTOR_B_ENB'],
                             BOARD['MOTOR_C_IN1'],
                             BOARD['MOTOR_C_IN2'],
                             BOARD['MOTOR_D_IN1'],
                             BOARD['MOTOR_D_IN2'],
                             BOARD['MOTOR_C_ENC'],
                             BOARD['MOTOR_D_END'],
                             BOARD['ENCODER_R'],
                             BOARD['ENCODER_L'],
                             BOARD['INFRA'],
                             )
        self.acceleration = WierdQueue();
        self.velocity = 0
        self.speedMode = 'manual' # By default
        self.change_speed(35)
        self.stop(True)
        print "Manger object created"


    def get_speed(self,):
        return
        pass

    def changeSpeedMode(self, mode):
        self.speedMode=mode

        if mode == 'manual':
            self.acceleration.len=0
        else:
            self.acceleration.top='F'
            self.acceleration.len=floor(self.velocity/ACCELERATION_STEP)


    def change_speed(self,velocity):
        if self.speedMode == 'auto':
            velocity=min(100,ACCELERATION_STEP*velocity)
        self.motors.setVelocity(velocity)
        self.velocity=velocity

    def move(self,direction):
        if self.speedMode == 'auto':
            self.change_speed(self.acceleration.len)

        if direction == 'B':
            data={'IN1':1,'IN2':0,'IN3':1,'IN4':0,'IN5':1,'IN6':0,'IN7':1,'IN8':0}
            self.acceleration.enqueue(direction)
        elif direction == 'F':
            data={'IN1':0,'IN2':1,'IN3':0,'IN4':1,'IN5':0,'IN6':1,'IN7':0,'IN8':1}
            self.acceleration.enqueue(direction)
        elif direction == 'R':
            data={'IN1':0,'IN2':1,'IN3':0,'IN4':1,'IN5':1,'IN6':0,'IN7':1,'IN8':0}
        elif direction == 'L':
            data={'IN1':1,'IN2':0,'IN3':1,'IN4':0,'IN5':0,'IN6':1,'IN7':0,'IN8':1}
        self.motors.setData(data)

	# print "Dir: %s" %  direction

    def stop(self,check): # add check to have the same function template with move()
        data={'IN1':0,'IN2':0,'IN3':0,'IN4':0,'IN5':0,'IN6':0,'IN7':0,'IN8':0}
        self.motors.setData(data)

    @staticmethod
    def main():
        m=manager()
        m.move('F')
        m.change_speed(40)
        print 'me ', m.velocity
        m.changeSpeedMode(False)
        t=['F','F','F','F','F']
        for el in t:
            m.move(el)
            sleep(0.3)
            print m.velocity
        m.stop()

if __name__ == '__main__':
    manager.main()
