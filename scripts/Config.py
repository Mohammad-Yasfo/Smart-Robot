#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Mohammad-AlYasfo

global BOARD, PI, STEP, DC_FREQ, SR_FREQ,RESPONSE_TIME, MIDEAN_WINDOW, INITIAL_RESPONCE_TIME
BOARD = {

      'MOTOR_A_IN1':   31,
      'MOTOR_A_IN2':   33,
      'MOTOR_B_IN1':   37,
      'MOTOR_B_IN2':   35,
      'MOTOR_A_ENA':   29,
      'MOTOR_B_ENB':   32,

      'MOTOR_C_IN1':   13,
      'MOTOR_C_IN2':   15,
      'MOTOR_D_IN1':   18,
      'MOTOR_D_IN2':   16,

      'MOTOR_C_ENC':   11,
      'MOTOR_D_END':   12,

      'ENCODER_R'  :   36,
      'ENCODER_L'  :   38,

      'INFRA'      :   40,

      'SERVO_H'    :   22,
      'SERVO_V'    :   24,

     }

MAX_RESPONSE_TIME=0.5
INITIAL_RESPONCE_TIME=10;
PI      = 3.14752
STEP    = 0.1
DC_FREQ = 100
SR_FREQ = 1000
MIDEAN_WINDOW = 15
ACCELERATION_STEP=20
MIN_SPEED_CHANGE=5
