"""Build a legend from the source data structure document.

The legend is mapping between the different id values found in the data set and
their plain-text equivalent.

Usage:
    python build_legend.py <structure_file> <output_file>
"""

from lxml import etree
from docopt import docopt

from common import NAMESPACES


def _parse_codelist(document, codelist_id):
    legend = {}
    entries = document.xpath(
        "//structure:CodeList[@id='{0}']/structure:Code".format(codelist_id),
        namespaces=NAMESPACES)

    for e in entries:
        name = e.xpath("./structure:Description/text()",
                       namespaces=NAMESPACES)[0]
        i = e.get("value")
        legend[i] = name
    return legend


def parse_geo(document):
    return _parse_codelist(document, "CL_GEO")


def parse_field_of_study(document):
    return _parse_codelist(document, "CL_CIP2011_4")


def parse_age(d):
    return _parse_codelist(d, "CL_AGE")


def parse_occupation(d):
    return _parse_codelist(d, "CL_NOC2011")


def parse_education_level(d):
    return _parse_codelist(d, "CL_HCDD_14V")


def parse_document(d):
    legend = {
        "location": parse_geo(d),
        "field_of_study": parse_field_of_study(d),
        "age_group": parse_age(d),
        "occupation": parse_occupation(d),
        "education_level": parse_education_level(d)
    }
    return legend


def run(input_file, output_file):
    doc = etree.parse(input_file)
    legend = parse_document(doc)
    with open(output_file) as f:
        f.write(str(legend))


if __name__ == "__main__":
    args = docopt(__doc__)
    run(
        args["<structure_file>"],
        args["<output_file>"]
    )
