"""Dump the raw XML data into a tabular format.

Usage:
    python dump_raw_data.py csv <input_file> <output_file> [options]

Options:
    --limit=LIMIT  Limit the dump to this number of rows
"""

from docopt import docopt
from lxml import etree
import resource
import csv

from common import NAMESPACES


SERIES_TAG = "{%s}Series" % NAMESPACES["generic"]
VALUE_TAG = "{%s}Value" % NAMESPACES["generic"]
TIME_TAG = "{%s}Time" % NAMESPACES["generic"]
OBSVALUE_TAG = "{%s}ObsValue" % NAMESPACES["generic"]


def _set_cats, category_prefix, cat1, cat2, cat3):
    d["{0}_cat1".format(category_prefix)] = cat1
    d["{0}_cat2".format(category_prefix)] = cat2
    d["{0}_cat3".format(category_prefix)] = cat3
    return d


def _subcategorize_column(d, column_name, category_prefix):
    cat = d[column_name]
    if len(cat) == 1:
        d = _set_cats(d, category_prefix, cat, None, None)
    if len(cat) == 2:
        d = _set_cats(d, category_prefix, cat[0], cat, None)
    if len(cat) == 3:
        d = _set_cats(d, category_prefix, cat[0], cat[:2], cat)
    return d


def generate_raw_data(input_handle, limit=None, track_memory_usage=False):

    counter = 0
    context = etree.iterparse(input_handle, events=("start",))
    for action, elem in context:

        if counter > 1000 and counter % 1000 == 0:
            print "processed {0} rows".format(counter)

        if limit and counter >= limit:
            print("reached limit {0}, stopping here".format(limit))
            break

        row = {}

        if elem.tag == SERIES_TAG:

            children = elem.getchildren()
            if len(children) != 2:
                continue

            for e in children[0]:
                if e.tag == VALUE_TAG:
                    row[e.get("concept")] = e.get("value")

            for e in children[1]:
                if e.tag == TIME_TAG:
                    row["time"] = e.text
                elif e.tag == OBSVALUE_TAG:
                    row["observation_value"] = e.get("value")

            row = _subcategorize_column(row, "NOC2011", "occupation")
            row = _subcategorize_column(row, "CIP2011_4", "field_of_study")

        else:
            continue

        # track memory usage
        if track_memory_usage:        
            print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # cleanup
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        counter += 1

        yield row


def get_fieldnames(input_handle):
    g = generate_raw_data(input_handle, limit=1)
    k = g.next().keys()
    input_handle.seek(0)
    return k


def dump_data(input_handle, output_writer, limit=None):
    g = generate_raw_data(input_handle, limit=limit)
    for r in g:
        output_writer.writerow(r)


def run(input_file, output_file, limit=None):

    input_handle = open(input_file, "r")
    
    fieldnames = get_fieldnames(input_handle) 
    output_handle = open(output_file, "w")
    output_writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
    writer.writeheader()
    
    try:
        dump_data(input_handle, output_writer, limit=limit)
    except:
        pass

    input_handle.close()
    output_handle.close()


if __name__ == "__main__":
    args = docopt(__doc__)
    run(args["<input_file>"], args["<output_file>"], args["--limit"])
