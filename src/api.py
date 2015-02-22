from flask import Flask
from flask import request
import psycopg2
import copy

app = Flask(__name__)
# db_conn = psycopg2.connect(
#     database="code2015", user="app_user", password="app_user_password")
# cursor = db_conn.cursor()


DEFAULTS = {
    "geo": [1],
    "cip2011_4": [1],
    "age": [1],
    "noc2011": [1],
    "hcdd_14v": [2, 3, 4]
}

#    "geo": "location",
#    "cip2011_4": "field_of_study",
#    "age": "age",
#    "noc2011": "occupation",
#    "hcdd_14v": "education_level"



def build_query(args):
    d = copy.copy(DEFAULTS)
    d.update(args)
    q = "SELECT SUM(observation_value) FROM data WHERE "
    q += "AND ".join(
        [k + " IN (" + ",".join([str(j) for j in d[k]]) + ") " for k in d]
    )
    return q


@app.route('/api/v1/status')
def status():
    return 'Hello World!'


@app.route('/api/v1/totals')
def totals():
    cip_2011_4 = request.args.get("cip_2011_4")
    if cip_2011_4:
        q = build_query({"cip_2011_4": cip_2011_4})
    else:
        raise ValueError("invalid value for cip_2011_4: {0}".format(cip_2011_4))
    return q

    # get query params
    # need field of study



@app.route('/api/v1/ratios')
def ratios():
    pass
    # get query params
    # query db
    # get totals
    # get denominators
    # build json
    # return


# occupation categories
# field of study categories
# location
# age

# value
# totals
# ratios


# given a field of study
    # return the top 10 industries by total, ratio

# denominators can be found by walking up the category tree.

# note that you have to limit some variables:

# code2015=# SELECT SUM(observation_value) FROM data WHERE GEO=1 AND NOC2011=1 AND CIP2011_4=1 AND AGE=1 AND (HCDD_14V=2 OR HCDD_14V=3 OR HCDD_14V=4);


if __name__ == '__main__':
    app.debug = True
    app.run()