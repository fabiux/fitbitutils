# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join


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
