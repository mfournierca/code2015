"""Build a legend from the data structure document.

The legend is a dictionary. The dictionary maps between the different id values 
found in the data set and their plain-text equivalent.

Usage:
    build_legend.py <data_zip> <category_map_json> <cip_map_csv> <noc_map_csv> [options]

Arguments:
    <data_zip>           The data set zip file
    <category_map_json>  Output file for the category mapping, a dictionary
                         mapping category keys to ids
    <cip_map_csv>        Output file for the CIP category mapping, a csv 
                         containing the category name and id of each field
                         of education
    <noc_map_csv>        Output file for the NOC category mapping, a csv
                         containing the category name and id of each
                         occupation
    --help               Show this help page
"""

from lxml import etree
from docopt import docopt
from collections import defaultdict

import csv
import json

from src.constants import NAMESPACES, ZIP_STRUCTURE_PATH
from src.common import extract_category_name_id, get_input_from_zip


TAG_MAPPING = {
    "geo": "location",
    "cip2011_4": "field_of_study",
    "age": "age",
    "noc2011": "occupation",
    "hcdd_14v": "education_level"
}


def _get_next_unique_nocat_id():
    start = 0
    while True:
        start += 1
        yield "nocategory.{0}".format(start)


def _parse_codelist(
        document, 
        codelist_id, 
        extract_category_id=False
    ):
    legend = {}
    entries = document.xpath(
        "//structure:CodeList[@id='{0}']/structure:Code".format(codelist_id),
        namespaces=NAMESPACES)
    
    no_category_id_generator = _get_next_unique_nocat_id()

    for e in entries:
        category_key = e.get("value")  
        name = e.xpath(
            "./structure:Description/text()",
            namespaces=NAMESPACES
        )[0] 
        
        if extract_category_id:
            category_id, category_name = extract_category_name_id(name)
        else:
            name = name.strip()
            category_id, category_name = None, name

        if not category_id:
            category_id = no_category_id_generator.next()
 
        legend[category_key] = {
            "category_id": category_id, 
            "category_name": category_name, 
            "subcategories": []
        }

    return legend


def _sort_subcategories(l): 
    subcats = l.get("subcategories", [])
    subcats.sort(key=lambda x: x["category_id"])
    l["subcategories"] = subcats

    for i, s in enumerate(l["subcategories"]):
        l["subcategories"][i] = _sort_subcategories(s)
    
    return l

    
def _gather_codelist(codelist):
      
    l = {"category_id": None, "subcategories": []}

    for category_key, c in codelist.iteritems():

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
            kl = [
                t for t in nl["subcategories"] if t["category_id"] == k
            ]
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
        nl["category_key"] = category_key
   
    return l


def _parse_legend(document, codelist_id, extract_category_id=False):
    legend = _parse_codelist(
        document, codelist_id, extract_category_id=extract_category_id)
    legend = _gather_codelist(legend)   
    legend = _sort_subcategories(legend) 
    return legend

 
def parse_full_legend(d):
    legend = {
        "GEO": _parse_legend(d, "CL_GEO"),
        "CIP2011_4": _parse_legend(
            d, "CL_CIP2011_4", extract_category_id=True
        ),
        "AGE": _parse_legend(d, "CL_AGE"),
        "NOC2011": _parse_legend(d, "CL_NOC2011", extract_category_id=True),
        "HCDD_14V": _parse_legend(d, "CL_HCDD_14V")
    }
    return legend


def _parse_category_mapping(document, codelist_id, extract_category_id=False):
    legend = _parse_codelist(
        document, codelist_id, extract_category_id=extract_category_id)
    return legend


def parse_full_category_mapping(d):
    category_mapping = {
        "CIP2011_4": _parse_category_mapping(
            d, "CL_CIP2011_4"
        ),
        "NOC2011": _parse_category_mapping(
            d, "CL_NOC2011", extract_category_id=True
        )
    }
    return category_mapping


def _write_mapping(mapping, output_csv):
    fieldnames = ["category_key", "category_id", "category_name"]
    with open(output_csv, "w") as c: 
        f = csv.DictWriter(c, fieldnames)
        f.writeheader() 
        for n, d in mapping.iteritems():            
            d = {
                k: v.encode("utf-8") for k, v in d.items() if k != "subcategories"
            }
            d["category_key"] = n
            f.writerow(d)
    

def run_document(
        document, 
        category_mapping_json, 
        cip_mapping_csv, 
        noc_mapping_csv
    ):
    
    category_mapping = parse_full_category_mapping(document)
    with open(category_mapping_json, "w") as f:
        f.write(json.dumps(category_mapping, indent=2))
   
    cip_mapping = category_mapping["CIP2011_4"]
    _write_mapping(cip_mapping, cip_mapping_csv)

    noc_mapping = category_mapping["NOC2011"]
    _write_mapping(noc_mapping, noc_mapping_csv)


def run(zip_path, category_mapping_json, cip_mapping_csv, noc_mapping_csv): 
    input_file = get_input_from_zip(zip_path, ZIP_STRUCTURE_PATH)
    doc = etree.parse(input_file) 
    run_document(doc, category_mapping_json, cip_mapping_csv, noc_mapping_csv)


if __name__ == "__main__":
    args = docopt(__doc__)
    run(
        args["<data_zip>"],
        args["<category_map_json>"], 
        args["<cip_map_csv>"], 
        args["<noc_map_csv>"]
    )
