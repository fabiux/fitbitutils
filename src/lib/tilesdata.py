# -*- coding: utf-8 -*-
from os.path import isfile


class TilesData:
    """
    Fetch data from Fitbit HTML+JS web panel.
    """
    def __init__(self, htmlfile):
        """
        Constructor.
        Do initial scan of file.
        :param htmlfile: HTML source file name
        """
        self._tdata = dict()
        if isfile(htmlfile):
            try:
                with open(htmlfile, 'r') as f:
                    self._html = f.readlines()
            except:
                return
        if self._seek('</footer>'):
            more_blocks = True
            while more_blocks:
                more_blocks = self._get_data_block()

    def _seek(self, s):
        """
        Search for a delimiter in our list of HTML rows.
        Truncate list if delimiter found.
        :param s: delimiter
        :return: True if delimiter found
        """
        pos = 0
        found = False
        for row in self._html:
            pos += 1
            found = (s == row.strip())
            if found:
                self._html = self._html[pos:]
                break
        return found

    def _get_row(self):
        """
        Get first row in our list of HTML rows and move pointer ahead.
        :return: stripped HTML row
        """
        row = self._html[0].strip()
        self._html = self._html[1:]
        return row

    def _get_label(self):
        """
        Get a label for current data block (name of ajax function).
        :return: label or '' if not found
        """
        row = self._get_row()
        if row[:13] == 'ajax.preload(':
            return row.split('"')[1]
        else:
            return ''

    def _get_data_type(self):
        """
        Get data type for current data block.
        :return: data type label or '' if not found
        """
        row = self._get_row()
        return row.split('"')[1]

    def _get_data_desc(self):
        """
        Get data description for current data block.
        :return: data description (dict)
        """
        row = self._get_row()
        return eval(row[:-1])

    def _get_data(self):
        """
        Return current data block.
        :return: data block (dict)
        """
        row = self._get_row().replace(':true', ':True').replace(':false', ':False').replace(':null', ':None')
        return eval(row[:-5])[0]

    def _get_data_block(self):
        """
        Get a single data block from HTML.
        :return: True if new data block found
        """
        found = False
        if self._seek('<script>'):
            if self._seek('require(["galileo/ajax/ajax"], function(ajax) {'):
                label = self._get_label()
                if label != '':
                    datatype = self._get_data_type()
                    datadesc = self._get_data_desc()
                    data = self._get_data()
                    self._tdata[label] = dict(datatype=datatype, datadesc=datadesc, data=data)
                    found = True
        return found

    @property
    def data(self):
        return self._tdata
