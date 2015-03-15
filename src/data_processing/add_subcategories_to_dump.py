"""Add subcategories to the dump csv.

Usage:
    add_subcategories_to_dump.py <input_file> <output_file>

Arguments:
    <input_file>   input csv
    <output_file>  output csv
"""

from docopt import docopt
import csv

from dump_raw_data import *

def run(input_file, output_file):
    csvin = csv.DictReader(open(input_file, "r"))
    fieldnames = csvin.fieldnames + SUBCATS_FIELDNAMES

    csvout = csv.DictWriter(open(output_file, "w"), fieldnames=fieldnames)
    csvout.writeheader()

    counter = 0
    for d in csvin:
        d = _subcategorize_column(d, "NOC2011", "occupation")
        d = _subcategorize_column(d, "CIP2011_4", "field_of_study")

        counter += 1
        if counter > 1 and counter % 500000 == 0:
            print("processed {0} lines".format(counter))

        csvout.writerow(d)


if __name__ == "__main__":
    args = docopt(__doc__)
    run(args["<input_file>"], args["<output_file>"])
