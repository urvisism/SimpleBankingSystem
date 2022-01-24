import mysql.connector
import pytz
import datetime

mydb = mysql.connector.connect(host='localhost', user='root', password='123456', database='accounts')
mycursor = mydb.cursor()

# mycursor.execute("TRUNCATE TABLE accounts")
# mycursor.execute("TRUNCATE TABLE transactions")

mycursor.execute("CREATE TABLE IF NOT EXISTS accounts (datetime_utc TIMESTAMP(6) NOT NULL, "
                 "name VARCHAR(255) primary key NOT NULL, balance float NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS transactions (datetime_utc TIMESTAMP(6) NOT NULL, "
                 "account VARCHAR(255) NOT NULL, "
                 "amount float NOT NULL, PRIMARY KEY(datetime_utc, account))")
mycursor.execute("CREATE or REPLACE VIEW localhistory as "
                 "SELECT date_format(CONVERT_TZ(datetime_utc, '+00:00', '+05:30'), '%d-%m-%Y %T') as local_time, "
                 "account, amount FROM transactions")


class Account:

    @staticmethod
    def _current_time():
        return pytz.utc.localize(datetime.datetime.utcnow())

    def __init__(self, name: str, opening_balance: float = 0.0):
        mycursor.execute("SELECT * FROM accounts WHERE name = %s", (name, ))
        acc_exists = mycursor.fetchone()

        if acc_exists:
            utc_datetime, self.name, current_balance = acc_exists
            self._balance = current_balance * 100
            local_time = str(pytz.utc.localize(utc_datetime).astimezone())[0:19]
            print(f"Account of {self.name} already exists & created on {local_time}.", end=' ')
        else:
            self.name = name
            self._balance = opening_balance * 100
            acct_generation_time_utc = Account._current_time()
            mycursor.execute("INSERT INTO accounts VALUES (%s, %s, %s)",
                             (acct_generation_time_utc, self.name, self._balance / 100))
            mydb.commit()
            print(f"Account created for {self.name}.", end=' ')
        self.show_balance()

    def _save_amount(self, amount):
        new_balance = self._balance + (amount * 100)
        utc_datetime = Account._current_time()
        try:
            mycursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_balance / 100, self.name))
            mycursor.execute("INSERT INTO transactions VALUES (%s, %s, %s)",
                             (utc_datetime, self.name, amount))
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError):
            mydb.rollback()
        else:
            mydb.commit()
            self._balance = new_balance

    def deposit(self, amount: float) -> float:
        if amount > 0.0:
            self._save_amount(amount)
            print(f"{amount:.2f} deposited from the acct. of {self.name}.")
        return self._balance / 100

    def withdraw(self, amount: float) -> float:
        if 0 < amount < self._balance:
            self._save_amount(-amount)
            print(f"{amount:.2f} withdrawn from the acct. of {self.name}.")
        else:
            print("The amount must be greater than zero & no less than your account balance")
            return 0.0

    def show_balance(self):
        print(f"Balance on account of {self.name} is {self._balance / 100:.2f}")


if __name__ == "__main__":
    urvis = Account("Urvis")
    urvis.deposit(10.10)
    urvis.deposit(0.10)
    urvis.deposit(0.20)
    urvis.deposit(0)
    urvis.withdraw(0.33)
    urvis.show_balance()

    Neel = Account('Neel', 15)
    Pratik = Account('Pratik', 9000)
    Sahil = Account('Sahil', 6500)
    Monika = Account('Monika', 10_000)

    mydb.close()