import sqlite3 as sqlite


class DBConn:
    """
    Database connector.
    """
    def __init__(self, dbname, decsep, thsep):
        """
        Constructor.
        :param dbname: path to database file
        :param decsep: decimal separator char
        :param thsep: thousands separator char
        """
        self._decsep = decsep
        self._thsep = thsep
        self._db = None
        try:
            self._db = sqlite.connect(dbname)
            self._cur = self._db.cursor()
        except Exception, e:
            print 'Error opening database ' + dbname
            print str(e)

    def __del__(self):
        """
        Destructor.
        Commit and close connection.
        """
        self._db.commit()
        self._db.close()

    def _to_int(self, v):
        """
        Convert string representation of a value to integer form.
        :param v: value
        :return: converted value
        """
        return v.replace(self._thsep, '')

    def _to_float(self, v):
        """
        Convert string representation of a value to float form.
        :param v: value
        :return: converted value
        """
        return v.replace(self._thsep, '').replace(self._decsep, '.')

    def _delete_record(self, table, tstamp):
        """
        Delete a record from a table, given the key value (timestamp).
        :param table: table name
        :param tstamp: timestamp
        """
        try:
            self._cur.execute("DELETE FROM " + table + " WHERE date_time = ?", [tstamp])
        except Exception, e:
            print 'Error deleting key ' + tstamp + ' from table ' + table
            print str(e)

    def _save(self, table, data):
        """
        Save data into a table.
        :param table: table name
        :param data: data to save (tuple)
        """
        try:
            self._cur.execute("INSERT INTO " + table + " VALUES (" + ", ".join(['?'] * len(data)) + ")", data)
        except Exception, e:
            print 'Error saving record in table ' + table
            print str(e)

    def _save_body(self, data):
        """
        Save 'body' block data.
        :param data: 'body' block data
        """
        keys = sorted(data)
        for key in keys:
            self._delete_record('body', key)
            data[key][0] = self._to_int(data[key][0])
            data[key][1] = self._to_float(data[key][1])
            data[key][2] = self._to_float(data[key][2])
            self._save('body', [key] + data[key])

    def _save_activity(self, data):
        """
        Save 'activity' block data.
        :param data: 'activity' block data
        """
        keys = sorted(data)
        for key in keys:
            self._delete_record('activity', key)
            self._delete_record('activity_periods', key)
            data[key][0] = self._to_int(data[key][0])
            data[key][1] = self._to_int(data[key][1])
            data[key][2] = self._to_float(data[key][2])
            data[key][3] = self._to_int(data[key][3])
            data[key][4] = self._to_int(data[key][4])
            data[key][5] = self._to_int(data[key][5])
            data[key][6] = self._to_int(data[key][6])
            data[key][7] = self._to_int(data[key][7])
            data[key][8] = self._to_int(data[key][8])
            if int(data[key][8]) != 0:
                for i in range(4, 8):
                    self._save('activity_periods', [key, str(i - 4), data[key][i]])
                del(data[key][4])
                del(data[key][4])
                del(data[key][4])
                del(data[key][4])
                self._save('activity', [key] + data[key])

    def _save_sleep(self, data):
        """
        Save 'sleep' block data.
        Fields:
        0: sleeping_minutes
        1: waking_minutes
        2: awakenings
        3: resting_minutes = sleeping_minutes + waking_minutes (it seems redundant)
        :param data: 'sleep' block data
        """
        keys = sorted(data)
        for key in keys:
            if int(data[key][3]) > 0:  # sleep activity has been registered
                self._delete_record('sleep', key)
                self._save('sleep', [key] + data[key])

    def save(self, data):
        """
        Save data from fitbit into database.
        :param data: data from fitbit
        """
        self._save_body(data['body'])
        self._save_activity(data['activity'])
        self._save_sleep(data['sleep'])
