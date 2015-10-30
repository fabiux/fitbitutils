# -*- coding: utf-8 -*-
"""
Import Fitbit Charge HR data from CVS to sqlite database.
"""
from lib.config import Configuration
from lib.db import DBConn
from lib.utils import filelist, convert_tstamp
from csv import reader

if __name__ == '__main__':
    # global configuration
    config = Configuration()
    if config.ok:
        csvpath = config.csvpath
        header = config.header  # dict - only contains interesting data block names
    else:
        print 'Error reading config file!'
        exit(1)

    db = DBConn(config.dbname, config.decsep, config.thsep)
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
