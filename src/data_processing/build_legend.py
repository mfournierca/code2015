"""Build a legend from the data structure document.

The legend is a dictionary. The dictionary maps between the different id values 
found in the data set and their plain-text equivalent.

Usage:
    build_legend.py <structure_file> <output_file> [options]

Arguments:
    <structure_file>  structure file that came with the dataset
    <output_file>     output file for the legend
    --help            show this help page
"""

from lxml import etree
from docopt import docopt
from collections import defaultdict

import json

from src.constants import NAMESPACES
from src.common import extract_category_name_id


TAG_MAPPING = {
    "geo": "location",
    "cip2011_4": "field_of_study",
    "age": "age",
    "noc2011": "occupation",
    "hcdd_14v": "education_level"
}


def _parse_codelist(document, codelist_id):
    legend = []
    entries = document.xpath(
        "//structure:CodeList[@id='{0}']/structure:Code".format(codelist_id),
        namespaces=NAMESPACES)

    for e in entries:
        category_key = e.get("value")  
        name = e.xpath(
            "./structure:Description/text()",
            namespaces=NAMESPACES
        )[0] 
        category_id, category_name = extract_category_name_id(name)
       
        legend.append({
            "category_id": category_id, 
            "category_name": category_name, 
            "category_key": category_key,
            "subcategories": []
        })

    return _gather_codelist(legend)

    
def _gather_codelist(codelist):
      
    l = {"category_id": None, "subcategories": []}

    for c in codelist:

        keys = []
        if c.get("category_id", "").find(".") == -1:
            for i in range(len(c["category_id"]) + 1):
                keys.append(c["category_id"][:i])
        else:
            p = c.get("category_id", "")
            if p.endswith("."):   
                keys = [p]
            else:
                keys = [p.split(".")[0] + ".", p]


        nl = l 
        for i, k in enumerate(keys):
            kl = [t for t in nl["subcategories"] if t["category_id"] == k]
            if len(kl) == 0:
                ll = {"category_id": k, "subcategories": []}
                nl["subcategories"].append(ll) 
                nl = ll
            elif len(kl) > 1:
                print("category id not unique! {0}".format(kl))
                raise ValueError
            else:
                nl = kl[0]

        nl["category_name"] = c.get("category_name")
        nl["category_key"] = c.get("category_key")
        nl["subcategories"].sort()
    
    return l

    
def parse_legend_document(d):
    legend = {
        "GEO": _parse_codelist(d, "CL_GEO"),
        "CIP2011_4": _parse_codelist(d, "CL_CIP2011_4"),
        "AGE": _parse_codelist(d, "CL_AGE"),
        "NOC2011": _parse_codelist(d, "CL_NOC2011"),
        "HCDD_14V": _parse_codelist(d, "CL_HCDD_14V")
    }
    return legend


def parse_legend_file(f):
    doc = etree.parse(f)
    legend = parse_legend_document(doc)
    return legend


def run(input_file, output_file):
    legend = parse_legend_file(input_file)
    with open(output_file, "w") as f:
        f.write(json.dumps(legend, indent=2))


if __name__ == "__main__":
    args = docopt(__doc__)
    run(
        args["<structure_file>"],
        args["<output_file>"]
    )
