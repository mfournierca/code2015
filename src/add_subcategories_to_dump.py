"""Add subcategories to the dump csv.

Usage:
    add_subcategories_to_dump.py <input_file> <output_file>

Arguments:
    <input_file>   input csv
    <output_file>  output csv
"""

from docopt import docopt
import csv


def set_cats(d, category_prefix, cat1, cat2, cat3):
    d["{0}_cat1".format(category_prefix)] = cat1
    d["{0}_cat2".format(category_prefix)] = cat2
    d["{0}_cat3".format(category_prefix)] = cat3
    return d


def subcategorize_column(d, column_name, category_prefix):
    cat = d[column_name]
    if len(cat) == 1:
        d = set_cats(d, category_prefix, cat, None, None)
    if len(cat) == 2:
        d = set_cats(d, category_prefix, cat[0], cat, None)
    if len(cat) == 3:
        d = set_cats(d, category_prefix, cat[0], cat[:2], cat)
    return d


def run(input_file, output_file):
    csvin = csv.DictReader(open(input_file, "r"))
    fieldnames = csvin.fieldnames + [
        "occupation_cat1", "occupation_cat2", "occupation_cat3",
        "field_of_study_cat1", "field_of_study_cat2", "field_of_study_cat3"]

    csvout = csv.DictWriter(open(output_file, "w"), fieldnames=fieldnames)
    csvout.writeheader()

    counter = 0
    for d in csvin:
        d = subcategorize_column(d, "NOC2011", "occupation")
        d = subcategorize_column(d, "CIP2011_4", "field_of_study")

        counter += 1
        if counter > 1 and counter % 500000 == 0:
            print("processed {0} lines".format(counter))

        csvout.writerow(d)


if __name__ == "__main__":
    args = docopt(__doc__)
    run(args["<input_file>"], args["<output_file>"])