# This is a sample Python script.

#
# Copyright (C) 2020-2024 Konrad Scham <konrad.scham@gmail.com>
# https://github.com/konrad1/tastyworks-guv-euro.git
#
# Generate data for a German tax income statement from Tastyworks tax gain and loss csv

import sys
import os
import datetime as pydatetime
import pandas


eurkurs = None
eurusd_csv
#euro_ezb_url: str = 'https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBEX3.D.USD.EUR.BB.AC.000&its_csvFormat=en&its_fileFormat=csv&mode=its&its_from=2010'

# Setup 'eurkurs' as dict() to contain the EURUSD exchange rate on a given date
# based on official data from ezb.de.
# If the file 'eurusd.csv' does not exist, download the data from
# the bundesbank directly.
def read_eurusd() -> None:
    import csv
    global eurkurs,eurusd_csv

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

def usage() -> None:
    print('tastyworks-guv-euro.py [-ouv]' +
        '[--output=test.csv][--eurusd=eurusd.csv][--help]' +
        '[--verbose][--debug][--show] *.csv')

def main(argv) -> None:
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
    all_wk = []
    for csv_file in args:
        all_wk.append(read_csv_tasty(csv_file))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
