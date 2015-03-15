import psycopg2

DB_NAME="code2015"
DB_USER="postgres"
DB_TABLE="data"


def get_conn():
    return psycopg2.connect("dbname={0} user={1}".format(DB_NAME, DB_USER))

def get_cursor():
    get_conn().cursor()

def insert_dict(cur, d, table=None):
    # I shouldn't need to write this function, I expected something better
    # to already exist. I couldn't find it in the docs though
    if table is None:
        table = DB_TABLE
    keys = d.keys()

    
    return "INSERT INTO {0} {1} VALUES {2}".format(
        table,
        keys, 
        [d[k] for k in keys]
    )
