#! /usr/bin/python2

import time
import sys
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

#ex.py
EMULATE_HX711=False
referenceUnit = -69
#up.py--
GDriveJSON = 'key.json'
GSpreadSheet = 'Python_Android'
WaitSecond =2
count = 1
#--

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    #print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    #print("Bye!")
    sys.exit()

hx = HX711(5,6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()
#print("Tare done! Add weight now...")


while True:
    try:
        val = max(0,int(hx.get_weight(5)))
        #val = hx.get_weight(5)
        #print(val)  
        hx.power_down()
        hx.power_up()
        #time.sleep(0.1)
        #up.py----
        scope = ["https://spreadsheets.google.com/feeds"]
        key = SAC.from_json_keyfile_name(GDriveJSON,scope)
        gc = gspread.authorize(key)
        #worksheet = gc.open(GSpreadSheet).sheet1
        worksheet = gc.open_by_key("16tNGUftG-4GqH7POpbudnY49RxU14LC89mtgyN1kwXs").sheet1

        dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        #worksheet.append_row((dt,count))
        worksheet.update_acell('A2',dt)
        worksheet.update_acell('B2',val)
        print("new")
        time.sleep(WaitSecond)
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
    
    
#--------------------
#Upload.py



'''
while True:
    try:
        scope = ["https://spreadsheets.google.com/feeds"]
        key = SAC.from_json_keyfile_name(GDriveJSON,scope)
        gc = gspread.authorize(key)
        #worksheet = gc.open(GSpreadSheet).sheet1
        worksheet = gc.open_by_key("16tNGUftG-4GqH7POpbudnY49RxU14LC89mtgyN1kwXs").sheet1

        dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        #worksheet.append_row((dt,count))
        worksheet.update_acell('A2',dt)
        worksheet.update_acell('B2',val)
        
        print("new")
        time.sleep(WaitSecond)
    except Exception as ex:
        print("can not link google")
        sys.exit()

'''