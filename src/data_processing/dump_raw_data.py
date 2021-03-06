"""Dump the raw XML data into a tabular format.

Usage:
    dump_raw_data.py csv <archive_path> <category_mapping_file> <output_file> [options]
    dump_raw_data.py postgresql <archive_path> <category_mapping_file> [options]

Arguments:
    <archive_path>  The path to the zip archive containing the raw data.
    <category_mapping_file>  Path to the category mapping, created by the 
                             build_legend script.
    <output_file>   Path to write the csv file to 

Options:
    --limit=LIMIT  Limit the dump to this number of rows
    --help         Display this help page
"""

from docopt import docopt
from lxml import etree
import resource
import csv
import psycopg2
import datetime
import re
import json

from src.constants import NAMESPACES, ZIP_DATA_PATH
from src.db import get_cursor, insert_dict
from src.common import get_input_from_zip

SERIES_TAG = "{%s}Series" % NAMESPACES["generic"]
VALUE_TAG = "{%s}Value" % NAMESPACES["generic"]
TIME_TAG = "{%s}Time" % NAMESPACES["generic"]
OBSVALUE_TAG = "{%s}ObsValue" % NAMESPACES["generic"]


def _set_cats(d, category_prefix, cat1, cat2, cat3, cat4):
    d["{0}_cat1".format(category_prefix)] = cat1 if cat1 else None 
    d["{0}_cat2".format(category_prefix)] = cat2 if cat2 else None
    d["{0}_cat3".format(category_prefix)] = cat3 if cat3 else None
    d["{0}_cat4".format(category_prefix)] = cat4 if cat4 else None
    return d


def _subcategorize_noc(row, category_key, category_mapping):
    i = str(category_mapping["NOC2011"][category_key]["category_id"])
    if len(i) == 1:
        row = _set_cats(row, "occupation", i[0], None, None, None)
    elif len(i) == 2:
        row = _set_cats(row, "occupation", i[0], i[:2], None, None)
    elif len(i) == 3:
        row = _set_cats(row, "occupation", i[0], i[:2], i[:3], None)
    elif len(i) == 4:
        row = _set_cats(row, "occupation", i[0], i[:2], i[:3], i[:4])
    else:
        row = _set_cats(row, "occupation", None, None, None, None)
    return row

def generate_raw_data(
        input_handle,  
        category_mapping=None,
        limit=None, 
        track_memory_usage=False
    ):

    starttime = datetime.datetime.utcnow()
    counter = 0
    read_counter = 0
    context = etree.iterparse(input_handle, events=("start",))
    for action, elem in context:

        row = {}

        if elem.tag == SERIES_TAG:

            # skip non - data entries
            children = elem.getchildren()
            if len(children) != 2:
                 continue

            # extract data
            for e in children[0]:
                if e.tag == VALUE_TAG:
                    row[e.get("concept")] = e.get("value")

            for e in children[1]:
                if e.tag == TIME_TAG:
                    row["time"] = e.text
                elif e.tag == OBSVALUE_TAG:
                    row["observation_value"] = e.get("value")

        else:
            continue
 
        # track memory usage
        if track_memory_usage:        
            print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # cleanup
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
 
        # check counter
        read_counter += 1
        if read_counter > 0 and read_counter % 100000 == 0:
            t = datetime.datetime.utcnow() - starttime
            print "read {0}, processed {1} rows in {2} seconds".format(
                read_counter, 
                counter,
                t.seconds
            )

        if limit and counter > limit:
            print("reached limit of {0} rows, stopping here".format(limit))
            raise StopIteration

        # we only look at aggregate data across all of Canada
        # skip province - specific rows
        if row["GEO"] != "01": 
            continue
        
        # skip rows that are not post-secondary or above
        if row["HCDD_14V"] not in ["4"]: 
            continue
        
        # aggregate across all age groups
        # skip specific age groups
        if row["AGE"] != "1": 
            continue

        # extract sub categories
        if category_mapping is not None:
            row = _subcategorize_noc(row, row["NOC2011"], category_mapping)
        
        counter += 1
        yield row


def get_fieldnames(input_file, category_mapping): 
    input_handle = get_input_from_zip(input_file, ZIP_DATA_PATH)
    g = generate_raw_data(
        input_handle, limit=1, category_mapping=category_mapping)
    k = g.next().keys()
    return k


def run_csv(input_file, category_file, output_file, limit=None):
    category_mapping = json.loads("".join(open(category_file, "r")))   
    
    input_handle = get_input_from_zip(input_file, ZIP_DATA_PATH) 
    
    fieldnames = get_fieldnames(input_file, category_mapping) 
    output_handle = open(output_file, "w")
    output_writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
    output_writer.writeheader()
 
    g = generate_raw_data(
        input_handle, limit=limit, category_mapping=category_mapping)
    for r in g:
        output_writer.writerow(r)
    
    input_handle.close()
    output_handle.close()


def run_postgresql(input_file, category_file, limit=None):
    category_mapping = json.loads("".join(open(category_file, "r")))   
    
    with get_input_from_zip(input_file, ZIP_DATA_PATH) as input_handle:
        cur = get_cursor()
        g = generate_raw_data(
            input_handle, limit=limit, category_mapping=category_mapping)
        for r in g:
            insert_dict(cur, r)
        cur.close()


if __name__ == "__main__":
    args = docopt(__doc__)

    limit = args["--limit"]
    limit = int(limit) if limit else None

    if args["csv"]:
        run_csv(
            args["<archive_path>"], 
            args["<category_mapping_file>"],
            args["<output_file>"], 
            limit=limit
        )
    elif args["postgresql"]:
        run_postgresql(
            args["<archive_path>"], 
            args["<category_mapping_file>"],
            limit=limit
        )

