"""Build a legend from the source data structure document.

The legend is mapping between the different id values found in the data set and
their plain-text equivalent.

Usage:
    build_legend.py <structure_file> <output_file>

Arguments:
    <structure_file>  structure file that came with the dataset
    <output_file>     output file for the legend
"""

from lxml import etree
from docopt import docopt

from common import NAMESPACES


TAG_MAPPING = {
    "GEO": "location",
    "CIP2011_4": "field_of_study",
    "AGE": "age",
    "NOC2011": "occupation",
    "HCDD_14V": "education_level"
}


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


def parse_document(d):
    legend = {
        "GEO": _parse_codelist(d, "CL_GEO"),
        "CIP2011_4": _parse_codelist(d, "CL_CIP2011_4"),
        "AGE": _parse_codelist(d, "CL_AGE"),
        "NOC2011": _parse_codelist(d, "CL_NOC2011"),
        "HCDD_14V": _parse_codelist(d, "CL_HCDD_14V")
    }
    return legend


def parse_file(f):
    doc = etree.parse(f)
    legend = parse_document(doc)
    return legend


def run(input_file, output_file):
    legend = parse_file(input_file)
    with open(output_file) as f:
        f.write(str(legend))


if __name__ == "__main__":
    args = docopt(__doc__)
    run(
        args["<structure_file>"],
        args["<output_file>"]
    )
