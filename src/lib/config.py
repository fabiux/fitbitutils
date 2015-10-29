# -*- coding: utf-8 -*-
import ConfigParser


class Configuration:
    def __init__(self):
        try:
            self._cfg = ConfigParser.RawConfigParser()
            self._cfg.read(['config/defaults.conf'])
        except:
            self._cfg = None

    @property
    def ok(self):
        return self._cfg is not None

    @property
    def csvpath(self):
        return None if self._cfg is None else self._cfg.get('CSV', 'path')

    @property
    def header(self):
        return None if self._cfg is None else eval(self._cfg.get('CSV', 'header'))

    @property
    def decsep(self):
        return None if self._cfg is None else self._cfg.get('LANG', 'decimal_separator')

    @property
    def thsep(self):
        return None if self._cfg is None else self._cfg.get('LANG', 'thousands_separator')

    @property
    def dbname(self):
        return None if self._cfg is None else self._cfg.get('DB', 'name')
