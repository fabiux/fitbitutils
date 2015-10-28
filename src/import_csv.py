# -*- coding: utf-8 -*-
import ConfigParser
from lib.db import DBConn
from os import listdir
from os.path import isfile, join
from csv import reader


def filelist(path):
    """
    Return list ov CSV files in a given folder.
    :param path: CSV folder
    :return: list of CSV files
    """
    return [f for f in listdir(path) if isfile(join(path, f)) and (f[0] != '.') and ('.csv' == f[-4:].lower())]


def convert_tstamp(timestamp):
    """
    Convert timestamp according to locale settings.
    :param timestamp: timestamp
    :return: converted timestamp (YYYY-MM-DD)
    """
    return timestamp[6:10] + '-' + timestamp[3:5] + '-' + timestamp[:2]

if __name__ == '__main__':
    # global configuration
    try:
        config = ConfigParser.RawConfigParser()
        config.read(['config/defaults.conf'])
        csvpath = config.get('CSV', 'path')
        header = eval(config.get('CSV', 'header'))  # converted to dict - only contains interesting data block names
        decsep = config.get('LANG', 'decimal_separator')
        thsep = config.get('LANG', 'thousands_separator')
        dbname = config.get('DB', 'name')
    except Exception, e:
        print 'Error reading config file!'
        print str(e)
        exit(1)

    db = DBConn(dbname, decsep, thsep)
    flist = sorted(filelist(csvpath))  # older files before
    for csvfile in flist:
        # save data blocks in a dict using header as key
        datablocks = dict()
        dblock = []  # this data block is a list of lists
        hdr = ''  # new data block's header - if not empty, we're currently reading data
        with open(csvpath + '/' + csvfile, 'rb') as f:
            print 'processing file ' + csvfile
            csv = reader(f)
            for row in csv:
                if hdr == '':  # this is the data block's header
                    hdr = row[0]
                else:
                    if row == []:  # end of data block
                        if hdr in header.keys():  # skip ignored data blocks
                            del(dblock[0])  # first element contains data field names: removed
                            d = dict()
                            for datarow in dblock:
                                d[convert_tstamp(datarow[0])] = datarow[1:len(datarow)]
                            datablocks[header[hdr]] = d  # now a single data block is a dict of lists
                        hdr = ''
                        dblock = []
                    else:
                        dblock.append(row)
        db.save(datablocks)
