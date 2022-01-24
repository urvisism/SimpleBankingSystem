import datetime
import pytz

# balance = "{:.2f}".format(float(input("Enter a number: ")))
# print(balance)
tz = pytz.timezone('Asia/Kolkata')
utc_time = pytz.utc.localize(datetime.datetime.utcnow())
local_time = pytz.utc.localize(utc_time).astimezone(tz=tz)
# local_time = ''

print(utc_time, local_time)