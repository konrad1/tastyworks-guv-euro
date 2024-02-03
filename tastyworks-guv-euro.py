# This is a sample Python script.

#
# Copyright (C) 2020-2024 Konrad Scham <konrad.scham@gmail.com>
# https://github.com/konrad1/tastyworks-guv-euro.git
#
# Generate data for a German tax income statement from Tastyworks tax gain and loss csv

import sys
import os
import datetime as pydatetime
from typing import List

import pandas
from pandas import DataFrame

eurkurs = None


# euro_ezb_url: str = 'https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBEX3.D.USD.EUR.BB.AC.000&its_csvFormat=en&its_fileFormat=csv&mode=its&its_from=2010'

# Setup 'eurkurs' as dict() to contain the EURUSD exchange rate on a given date
# based on official data from ezb.de.
# If the file 'eurusd.csv' does not exist, download the data from
# the bundesbank directly.
def read_eurusd(eurusd_csv: str) -> None:
    import csv
    global eurkurs

    if not os.path.exists(eurusd_csv):
        raise 'eurousd_csv does not exist'
    eurkurs = {}
    with open(eurusd_csv, encoding='UTF8') as csv_file:
        reader = csv.reader(csv_file)
        for _ in range(5):
            next(reader)
        for (date, usd, _) in reader:
            if date != '':
                if usd != '.':
                    eurkurs[date] = float(usd)
                else:
                    eurkurs[date] = None


def get_eurusd(date: str) -> float:
    while True:
        try:
            x = eurkurs[date]
        except KeyError:
            print(f'ERROR: No EURUSD conversion data available for {date},'
                  ' please download newer data into the file eurusd.csv.')
            sys.exit(1)
        if x is not None:
            return x
        date = str(pydatetime.date(*map(int, date.split('-'))) - pydatetime.timedelta(days=1))


# check if the first line of the csv line contains the correct header:
def check_csv(csv_file) -> None:
    with open(csv_file, encoding='UTF8') as f:
        content = f.readlines()
    if len(content) < 1 or content[
        0] != 'TAX_YEAR,SUBLOT_ID,SECNO,CUSIP,SYMBOL,SEC_DESCR,SEC_TYPE,SEC_SUBTYPE,SUBACCOUNT_TYPE,OPEN_TRAN_ID,CLOSE_TRAN_ID-SEQNO,OPEN_DATE,CLOSE_DATE,CLOSE_EVENT,DISPOSAL_METHOD,QUANTITY,LONG_SHORT_IND,NO_WS_COST,NO_WS_PROCEEDS,NO_WS_GAINLOSS,WS_COST_ADJ,WS_PROC_ADJ,WS_LOSS_ID-SEQNO,1099_ACQ_DATE,1099_DISP_DATE,1099_COST,1099_PROCEEDS,GROSS_NET_IND,TOTAL_GAINLOSS,ORDINARY_GAINLOSS,1099_DISALLOWED_LOSS,1099_MARKET_DISCOUNT,8949_GAINLOSS,8949_CODE,HOLDING_DATE,TERM,COVERED_IND,8949_BOX,1099_1256_CY_REALIZED,1099_1256_PY_UNREALIZED,1099_1256_CY_UNREALIZED,1099_1256_AGGREGATE\n':
        print('ERROR: Wrong first line in csv file. Please download trade history from the web page.')
        sys.exit(1)


def read_csv_tasty(csv_file: str) -> pandas.DataFrame:
    """

    :type csv_file: str
    """
    check_csv(csv_file)
    wk = pandas.read_csv(csv_file, parse_dates=['CLOSE_DATE'])
    return wk


def usage() -> None:
    print('tastyworks-guv-euro.py [-ouv]' +
          '[--output=test.csv][--eurusd=eurusd.csv][--help]' +
          '[--verbose][--debug][--show] *.csv')


def augmenteuramount(dataframe:pandas.DataFrame):
    for i in dataframe.index:
        if debug:
            print(dataframe.iloc[i].to_string())
        (datetime, tcode, tsubcode, symbol, buysell, openclose, quantity, expire, strike,
            callput, price, fees, amount, description, account_ref) = wk.iloc[i]


def main(argv) -> None:
    eurusd_csv: str = "https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBEX3.D.USD.EUR.BB.AC.000&its_csvFormat=en&its_fileFormat=csv&mode=its&its_from=2010"
    try:
        import getopt
        opts, args = getopt.getopt(argv, 'o:u:vhd', ['eurusd=',
                                                     'help', 'output=',
                                                     'verbose', 'debug'])

    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-u', '--eurusd'):
            eurusd_csv = arg
        elif opt == '--output':
            output_csv = arg
        elif opt in ('-u', '--usd'):
            global convert_currency
            convert_currency = False
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt == '--show':
            show = True
        elif opt == '--summary':
            output_summary = arg
        elif opt == '--tax-output':
            tax_output = arg
    if len(args) == 0:
        usage()
        sys.exit()
    read_eurusd(eurusd_csv)
    args.reverse()
    dataframe: DataFrame
    for csv_file in args:
        dataframe = read_csv_tasty(csv_file)
    augmenteuramount(dataframe)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
