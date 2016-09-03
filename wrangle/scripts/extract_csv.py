"""
Extracts data from spreadsheet and outputs plaintext CSV
- Does not attempt to clean messy dates
- Adds new column containing sheetname
"""

import argparse
import csv
from datetime import datetime
from loggy import loggy
from sys import stdout
import xlrd

LOGGY = loggy('loggy')
SHEETNAME_HEADER = 'sheetname'
DATE_CTYPE = 3


def float_to_datestring(cellfloat, datemode):
    dtuple = xlrd.xldate_as_tuple(cellfloat, datemode)
    return datetime(*dtuple).strftime('%Y-%m-%d')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("This does something")
    parser.add_argument('infile', type=argparse.FileType('r'), help='Spreadsheet to extract from')
    parser.add_argument('--sheetname', action='store_true', help="Print first sheetname and exit")

    args = parser.parse_args()
    xlsname = args.infile.name
    LOGGY.info('Opening spreadsheet: %s' % xlsname)

    book = xlrd.open_workbook(xlsname)

    if book.nsheets > 1:
        LOGGY.warn("Warning: %s sheets found (expecting just 1)" % book.nsheets)

    sheet = book.sheets()[0]
    if args.sheetname: # print to stdout and quit
        print(sheet.name)
    else:
        # otherwise, print metadata to stderr
        LOGGY.info("Sheet name: %s" % sheet.name)
        LOGGY.info("Row count: %s" % sheet.nrows)
        csvout = csv.writer(stdout)

        headers = sheet.row_values(0) + [SHEETNAME_HEADER]
        csvout.writerow(headers)
        for n in range(1, sheet.nrows):
            rowvals = [
                          float_to_datestring(cell.value, book.datemode) \
                          if cell.ctype == DATE_CTYPE else cell.value\
                          for cell in sheet.row(n)
                      ]
            csvout.writerow(rowvals)





"""
Example row
[text:'00613477',
 text:'00606168',
 text:'ALBRIGHT,CHARLES FREDRICK',
 text:'West Texas Hospital',
 text:'M',
 text:'W',
 xldate:12276.0,
 xldate:2958101.0,
 xldate:2958101.0,
 xldate:39179.0,
 text:'F-9104522-TJ',
 text:'Dallas',
 text:'09150000',
 text:'MURDER W/DEADLY WPN',
 xldate:33590.0,
 xldate:33316.0,
 text:'Life',
 text:'Denied on 09/03/2014',
 text:'08/2018',
 text:'NOT IN REVIEW PROCESS']
"""

