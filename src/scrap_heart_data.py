# -*- coding: utf-8 -*-
"""
Scrap resting heartrate data from Fitbit web panel to sqlite database.
"""
from lib.config import Configuration
from lib.db import DBConn
from lib.tilesdata import TilesData

if __name__ == '__main__':
    config = Configuration()
    if not config.ok:
        print 'Error reading config file!'
        exit(1)

    db = DBConn(config.dbname, config.decsep, config.thsep)
    td = TilesData(config.htmlfile)
    d = dict()
    d['heartrate'] = td.data['getRestingHeartRateData']['data']['dataPoints']  # resting heartrate data to import
    db.save(d)
