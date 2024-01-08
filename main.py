# This is a sample Python script.

#
# Copyright (C) 2020-2024 Konrad Scham <konrad.scham@gmail.com>
# https://github.com/konrad1/tastyworks-guv-euro.git
#
# Generate data for a German tax income statement from Tastyworks tax gain and loss csv

import sys
import getopt
import pandas

def usage() -> None:
    print('tastyworks-guv-euro.py [-usd]' +
        '[--output-csv=test.csv][--output-excel=test.xlsx][--help]' +
        '[--verbose][--debug][--show] *.csv')

def main(argv) -> None:
    try:
        opts, args = getopt.getopt(argv, 'dhuv', ['assume-individual-stock',
            'download-eurusd',
            'help', 'summary=', 'output-csv=', 'output-excel=',
            'show', 'tax-output=', 'usd', 'verbose', 'debug'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--assume-individual-stock':
            global assume_stock
            assume_stock = True
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '--download-eurusd':
            filename = 'eurusd.csv'
            if not os.path.exists(filename):
                import urllib.request
                urllib.request.urlretrieve(eurusd_url, filename)
            sys.exit()
        elif opt == '--output-csv':
            output_csv = arg
        elif opt == '--output-excel':
            output_excel = arg
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
    #read_eurusd()
    args.reverse()
    all_wk = []
    for csv_file in args:
        all_wk.append(read_csv_tasty(csv_file))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
