import serial
import pymongo

link_To_db = pymongo.MongoClient("mongodb://admin:123456@203.64.128.65:27017/")

use_db = link_To_db['admin']
use_col= use_db['pulse_service']

try:
    ser = serial.Serial('/dev/ttyACM0',9600)  

    while True:
        try:
            read_serial = ser.readline()
            bpm = read_serial.decode('utf-8').strip()
            use_col.delete_one({})
            use_col.insert_one({"pulse":bpm})

            print(bpm)
        except KeyboardInterrupt:
            print("EXIting")
            break

except KeyboardInterrupt:
    print("error")
