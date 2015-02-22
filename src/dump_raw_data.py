"""Dump the raw XML data into a tabular format.

Usage:
    python dump_raw_data.py csv <input_file> <output_file>
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


def parse(input_handle, output_handle):

        writer = None
        counter = 0

        context = etree.iterparse(input_handle, events=("start",))
        for action, elem in context:

            if counter > 1000 and counter % 1000 == 0:
                print "processed {0} rows".format(counter)

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

            else:
                continue

            if writer is None:
                writer = csv.DictWriter(output_handle, fieldnames=row.keys())
                writer.writeheader()
            writer.writerow(row)

            #memory usage
            # print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            # cleanup
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

            counter += 1


def run(input_file, output_file):

    input_handle = open(input_file, "r")
    output_handle = open(output_file, "w")

    try:
        parse(input_handle, output_handle)
    except:
        input_handle.close()
        output_handle.close()


if __name__ == "__main__":
    args = docopt(__doc__)
    run(args["<input_file>"], args["<output_file>"])
