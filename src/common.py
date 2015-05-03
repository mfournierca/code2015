import re

def extract_category_name_id(name):
    if not name:
        return None, None
    i = re.search(r"^\s*([\d\.]*)\s*(.*)", name)
    if not i:
        return None, None
    return i.group(1), i.group(2)


def get_input_from_zip(archive_path, zip_path):
    z = zipfile.ZipFile(data_zip, "r")
    return z.open(zip_path)
