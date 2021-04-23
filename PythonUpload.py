import sys
import time
from datetime import datetime
import gspread

from oauth2client.service_account import ServiceAccountCredentials as SAC
GDriveJSON = 'key.json'
GSpreadSheet = 'Python_Android'
WaitSecond =2
count = 1

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
        worksheet.update_acell('B2',count)
        count = count + 1
        print("new")
        time.sleep(WaitSecond)
    except Exception as ex:
        print("can not link google")
        sys.exit()
