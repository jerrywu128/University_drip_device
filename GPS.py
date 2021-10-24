#!/usr/bin/python3.7
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time
import pymongo

import sys
import os
sys.path.append('/home/Desktop/github/University_topics/GPS.py')

#db_link--
link_To_db = pymongo.MongoClient("mongodb://admin:123456@203.64.128.65:27017/")

use_db = link_To_db['admin']
use_col= use_db['Gps_service']
#--

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0

def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
                        gps_info = rec_buff.decode()
                        if ',,,,,,' not in gps_info:
                            gps_info = gps_info.split(': ')
                            gps_info = gps_info[1].split(',')
                            use_col.delete_one({})
                            use_col.insert_one({"latitude":gps_info[0],"longitude":gps_info[2]})
                        print(gps_info)
                        return 1
	else:
		print('GPS is not ready')
		return 0

def get_gps_position():
	rec_null = True
	answer = 0
	print('Start GPS session...')
	rec_buff = ''
	send_at('AT+CGPS=1,1','OK',1)
	time.sleep(2)
	while rec_null:
		answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
		if 1 == answer:
			answer = 0
			if ',,,,,,' in rec_buff:
				print('GPS is not ready')
				rec_null = False
				time.sleep(1)
		else:
			print('error %d'%answer)
			rec_buff = ''
			send_at('AT+CGPS=0','OK',1)
			return False
		time.sleep(1.5)


def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')

try:
	power_on(power_key)
	get_gps_position()
	power_down(power_key)
except:
	if ser != None:
		ser.close()
	power_down(power_key)
	GPIO.cleanup()
if ser != None:
		ser.close()
		GPIO.cleanup()	
