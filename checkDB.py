import pytz
import datetime
import mysql.connector
from colorama import Fore, Back, Style

mydb = mysql.connector.connect(host='localhost', user='root', password='123456', database='accounts')
mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM transactions")

# print(Style.BRIGHT, "---------Date-Time-----------|---Name---|--Amount--", Style.RESET_ALL)
# for time, name, amount in mycursor:
#     if amount > 0:
#         print(f"{str(time)[0:23]:^30}|{name:^10}|" + Fore.GREEN + f"{f'+{amount:.2f}':^10}", Style.RESET_ALL)
#     else:
#         print(f"{str(time)[0:23]:^30}|{name:^10}|" + Fore.RED + f"{amount:^10.2f}", Style.RESET_ALL)
# ----------------------------------------------------------------------------------------------------------------------
# for utc_time, name, amount in mycursor:
#     local_time = pytz.utc.localize(utc_time).astimezone()
#     print(f"{utc_time}\t{local_time}\t{name}\t{amount}")
# ----------------------------------------------------------------------------------------------------------------------
# mycursor.execute("SELECT date_format(CONVERT_TZ(time, '+00:00', '+05:30'), '%d-%m-%Y %T') as local_time, "
#                  "account, amount FROM transactions")
# for local_time, name, amount in mycursor:
#     print(f"{local_time}\t{name:^10}\t{amount}")
# ----------------------------------------------------------------------------------------------------------------------
mycursor.execute("SELECT * FROM localhistory")
for local_time, name, amount in mycursor:
    print(f"{local_time}\t{name:^10}\t{amount}")

mydb.close()