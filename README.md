Fitbit
======
Data management utilities for <b>Fitbit Charge HR</b>.

Food data are ignored here.

Description
-----------
This script reads data from <b>Fitbit Charge HR</b> (exported on a <tt>CSV</tt> file) and store them into a <tt>SQLite3</tt> database.

Database
--------
From this folder, run the following command in order to create default empty database:

<code>
sqlite3 src/db/fitbit.db < sql/fitbit.sql
</code>