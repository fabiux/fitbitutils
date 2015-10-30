DROP TABLE IF EXISTS body;
CREATE TABLE body (
    date_time DATETIME,
    weight INTEGER,
    bmi REAL,       -- body mass index
    fatmass REAL,   -- probably INTEGER
    PRIMARY KEY (date_time)
);

DROP TABLE IF EXISTS activity;
CREATE TABLE activity (
    date_time DATETIME,
    calories_burned INTEGER,
    steps INTEGER,
    distance REAL,
    floors INTEGER,
    calories_in_activity INTEGER,
    PRIMARY KEY (date_time)
);

DROP TABLE IF EXISTS activity_periods;
CREATE TABLE activity_periods (
    date_time DATETIME,
    intensity INTEGER,  -- 0 = sedentary, 1 = light, 2 = moderate, 3 = heavy activity
    minutes INTEGER,
    PRIMARY KEY (date_time, intensity)
);

DROP TABLE IF EXISTS sleep;
CREATE TABLE sleep (
    date_time DATETIME,
    sleeping_minutes INTEGER,
    waking_minutes INTEGER,
    awakenings INTEGER,
    resting_minutes INTEGER,  -- redudant, it should be sleeping_minutes + waking_minutes
    PRIMARY KEY (date_time)
);

DROP TABLE IF EXISTS resting_heartrate;
CREATE TABLE resting_heartrate (
    date_time DATETIME,
    heartrate REAL,
    PRIMARY KEY (date_time)
);

