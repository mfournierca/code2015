import re

def extract_category_name_id(name):
    if not name:
        return None, None
    i = re.search(r"^\s*([\d\.]*)\s*(.*)", name)
    if not i:
        return None, None
    return i.group(1), i.group(2)
