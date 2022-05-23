import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Load staging data from S3.
    Args:
        cur (cursor): psycopg cursor 
        conn (connetion): Encapsulation of PostgreSQL database session
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Load table data from staging tables.
    Args:
        cur (cursor): psycopg cursor 
        conn (connetion): Encapsulation of PostgreSQL database session
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Establishes a connection with the data warehouse in the Redshift cluster, 
    get's the cursor to it and extracts, transforms and loads the song and log data into the staging tables before
    copying this data into the final tables. Finally, closing the connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()