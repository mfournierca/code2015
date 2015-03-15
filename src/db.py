import psycopg2

DB_NAME="code2015"
DB_USER="postgres"
DB_TABLE="data"


def get_conn():
    conn = psycopg2.connect("dbname={0} user={1}".format(DB_NAME, DB_USER))
    conn.autocommit = True
    return conn


def get_cursor():
    return get_conn().cursor()


def insert_dict(cur, d, table=None):
    # I shouldn't need to write this function, I expected something better
    # to already exist. I couldn't find it in the docs though
    if table is None:
        table = DB_TABLE
    keys = d.keys()

    statement = "INSERT INTO {0} ({1}) VALUES ({2});".format(
        table,
        ", ".join(keys), 
        ", ".join(["%s" for k in keys])
    ) 
    cur.execute(statement, [d[k] if d[k] else None for k in keys])
