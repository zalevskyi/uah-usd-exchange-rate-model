import requests
import sqlite3
import csv
from datetime import date, timedelta

DATE_START = date(2016, 1, 1)
TODAY = date.today()
ONE_DAY = timedelta(days=1)
CURRENCY_CODES = ['USD', 'EUR', 'RUB', 'PLN']
DB_FIELDS = {'USD': 'uah_usd', 'EUR': 'uah_eur',
             'RUB': 'uah_rub', 'PLN': 'uah_pln'}
DB_FILE = 'uah-usd-data.db'
API_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'
BRENT_FILE = 'brent.csv'
WHEAT_FILE = 'wheat.csv'
STEAL_FILE = 'steal.csv'
MVEMSD_FILE = 'mvemsd.txt'


def main():
    db_populate_dates_till_today()
    db_update_exchange_rates_till_today()
    db_update_brent_till_today()
    db_update_wheat_till_today()
    db_update_steal_till_today()
    db_update_mvemsd_till_today()


def db_populate_dates_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(quote_date) FROM data')
    db_date_last = cursor.fetchone()[0]
    if db_date_last:
        date_last = date.fromisoformat(db_date_last)
    else:
        date_last = DATE_START - ONE_DAY
    while date_last < TODAY:
        date_last += ONE_DAY
        cursor.execute(f'INSERT INTO data (quote_date) VALUES("{date_last}")')
    connection.commit()
    connection.close()


def db_update_exchange_rates_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT MAX(quote_date) FROM data WHERE uah_usd IS NOT NULL AND uah_eur IS NOT NULL AND uah_rub IS NOT NULL AND uah_pln IS NOT NULL')
    db_date_last = cursor.fetchone()[0]
    if db_date_last:
        date_last = date.fromisoformat(db_date_last)
    else:
        date_last = DATE_START - ONE_DAY
    print('---- Updating currency rates ----')
    print(f'Currency rate request for: {date_last}', end='\r')
    while date_last < TODAY:
        date_last += ONE_DAY
        print(f'Currency rate request for: {date_last}', end='\r')
        response = requests.get(f'{API_URL}?json&date={date_last:%Y%m%d}')
        if response.status_code != 200:
            # This means something went wrong.
            print(
                f'Fail to retrieve currency data for date: {date_last}. Aborted. Status code: {response.status_code}')
            break
        fields = []
        rates = []
        for item in response.json():
            if item['cc'] in CURRENCY_CODES:
                fields.append(DB_FIELDS[item['cc']])
                rates.append(str(item['rate']))
        cursor.execute(
            f'UPDATE data SET ({",".join(fields)}) = ({",".join(rates)}) WHERE quote_date="{date_last}"')
    connection.commit()
    connection.close()
    print()


def db_update_brent_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    print('---- Updating brent prices ----')
    print('Brent price update for:', end='\r')
    with open(BRENT_FILE) as datafile:
        datareader = csv.reader(datafile)
        for row in datareader:
            if len(row) == 2:
                if len(row[0]) == 10:
                    try:
                        quote_date = date.fromisoformat(row[0])
                        price = float(row[1])
                        if quote_date >= DATE_START and quote_date <= TODAY:
                            print(
                                f'Brent price update for: {quote_date}', end='\r')
                            cursor.execute(
                                f'UPDATE data SET (brent) = ({price}) WHERE quote_date="{quote_date}"')
                    except ValueError:
                        pass
    connection.commit()
    connection.close()
    print()


def db_update_wheat_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    print('---- Updating wheat prices ----')
    print('Wheat price update for:', end='\r')
    with open(WHEAT_FILE) as datafile:
        datareader = csv.reader(datafile)
        for row in datareader:
            if len(row) == 2:
                if len(row[0]) == 10:
                    try:
                        quote_date = date.fromisoformat(row[0])
                        price = float(row[1])
                        if quote_date >= DATE_START and quote_date <= TODAY:
                            print(
                                f'Wheat price update for: {quote_date}', end='\r')
                            cursor.execute(
                                f'UPDATE data SET (wheat) = ({price}) WHERE quote_date="{quote_date}"')
                    except ValueError:
                        pass
    connection.commit()
    connection.close()
    print()


def db_update_mvemsd_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    print('---- Updating MVEMSD bond index ----')
    print('MVEMSD index update for:', end='\r')
    dialect_mv = 'mvemsd'
    csv.register_dialect(dialect_mv, delimiter=';')
    with open(MVEMSD_FILE) as datafile:
        datareader = csv.DictReader(datafile, dialect=dialect_mv)
        for row in datareader:
            quote_date = date.fromisoformat(
                f'{row["date"][0:4]}-{row["date"][4:6]}-{row["date"][6:8]}')
            index = float(row['MVEMSD'])
            if quote_date >= DATE_START and quote_date <= TODAY:
                print(
                    f'MVEMSD index update for: {quote_date}', end='\r')
                cursor.execute(
                    f'UPDATE data SET (mvemsd) = ({index}) WHERE quote_date="{quote_date}"')
    connection.commit()
    connection.close()
    print()
    csv.unregister_dialect(dialect_mv)


def db_update_steal_till_today():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    print('---- Updating Steal prices ----')
    print('Steal price update for:', end='\r')
    with open(STEAL_FILE) as datafile:
        datareader = csv.DictReader(datafile)
        for row in datareader:
            quote_date = date.fromisoformat(
                f'{row["USD/mt"][6:10]}-{row["USD/mt"][3:5]}-{row["USD/mt"][0:2]}')
            price = float(row['M1'])
            if quote_date >= DATE_START and quote_date <= TODAY:
                print(
                    f'Steal price update for: {quote_date}', end='\r')
                cursor.execute(
                    f'UPDATE data SET (steal) = ({price}) WHERE quote_date="{quote_date}"')
    connection.commit()
    connection.close()
    print()


if __name__ == '__main__':
    main()
