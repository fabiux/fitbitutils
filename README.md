Fitbit
======
Data management utilities for <b>Fitbit Charge HR</b>.

<b><i>Food</i></b> data are ignored here.

Description
-----------
These scripts collect data from <b>Fitbit Charge HR</b> into a <tt>SQLite3</tt> database.

Database
--------
From this folder, run the following command in order to create default empty database:

<code>
sqlite3 src/db/fitbit.db < sql/fitbit.sql
</code>

<tt>import_csv.py</tt>
----------------------
This script reads data (about <b><i>body</i></b>, <b><i>activity</i></b> and <b><i>sleep</i></b>) from an exported <tt>CSV</tt> file and store them into the database.

Before launching this script, save all your <tt>fitbit_export_YYYYMMDD.csv</tt> files in <tt>src/csv/</tt> folder or set your favourite one in <tt>src/config/defaults.conf</tt>.

<tt>scrap_heart_data.py</tt>
----------------------------
This script scraps data about <b><i>resting heart rate</i></b> from <b>Fitbit</b> <tt>HTML</tt> web panel into the database.

Before launching this script, save <tt>HTML</tt> source file as <tt>src/html/fitbit.html</tt> or set your favourite file path in <tt>src/config/defaults.conf</tt>.
