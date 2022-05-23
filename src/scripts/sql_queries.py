import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS events_staging;"
staging_songs_table_drop = "DROP TABLE IF EXISTS songs_staging;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users cascade;"
song_table_drop = "DROP TABLE IF EXISTS songs cascade;"
artist_table_drop = "DROP TABLE IF EXISTS artists cascade;"
time_table_drop = "DROP TABLE IF EXISTS time cascade;"

# CREATE TABLES

staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS events_staging (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender CHAR(1),
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location TEXT,
        method VARCHAR,
        page VARCHAR,
        registration VARCHAR,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        userAgent TEXT,
        userId INT
    );""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs_staging (
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_location TEXT,
        artist_longitude FLOAT,
        artist_name VARCHAR,
        duration FLOAT,
        num_songs INT,
        song_id VARCHAR,
        title VARCHAR,
        year INT
    );""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT IDENTITY(0,1) SORTKEY DISTKEY, 
        start_time TIMESTAMP, 
        user_id INT, 
        level VARCHAR, 
        song_id VARCHAR,  
        artist_id VARCHAR,
        session_id INT,
        location VARCHAR,
        user_agent VARCHAR
    );""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT SORTKEY, 
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR
    );""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR SORTKEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR,
        year INT,
        duration REAL
    );""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR SORTKEY,
        name VARCHAR,
        location VARCHAR,
        latitude REAL,
        longitude REAL
    );""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP SORTKEY,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        weekday INT NOT NULL
    );""")

# STAGING TABLES

staging_events_copy = (f"""
    copy events_staging
    from {LOG_DATA}
    iam_role {IAM_ROLE}
    json {LOG_JSONPATH};
""")

staging_songs_copy = (f"""
    copy songs_staging
    from {SONG_DATA}
    iam_role {IAM_ROLE}
    json 'auto';
""")

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
)
(
    SELECT
        TIMESTAMP 'epoch' + ev.ts/1000 * INTERVAL '1 second' as start_time,
        CAST(ev.userId AS INT),
        ev.level,
        so.song_id,
        so.artist_id,
        CAST(ev.sessionId AS INT),
        ev.location,
        ev.userAgent
    FROM
        events_staging ev
    LEFT OUTER JOIN songs_staging so
        ON (ev.song = so.title AND ev.artist = so.artist_name)
    WHERE ev.page = 'NextSong'
)
""")

user_table_insert = ("""
    INSERT INTO users(user_id, first_name, last_name, gender, level)
    SELECT DISTINCT CAST(userId as INT), firstName, lastName, gender,level
    FROM events_staging WHERE userId IS NOT NULL
""")

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration)
    (SELECT DISTINCT song_id, title, artist_id, year, duration FROM songs_staging)
""")

artist_table_insert = ("""
    INSERT INTO artists(artist_id, name, location, latitude, longitude)
    (SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM songs_staging)
""")

time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT ts.start_time as start_time,
        EXTRACT (HOUR FROM ts.start_time) as hour,
        EXTRACT (DAY FROM ts.start_time) as day,
        EXTRACT (WEEK FROM ts.start_time) as week,
        EXTRACT (MONTH FROM ts.start_time) as month,
        EXTRACT (YEAR FROM ts.start_time) as year,
        EXTRACT (WEEKDAY FROM ts.start_time) as weekday
    FROM (
        SELECT TIMESTAMP 'epoch' + ev.ts/1000 * INTERVAL '1 second' as start_time
        FROM events_staging ev
        ) ts
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create,
                        song_table_create, artist_table_create, time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
