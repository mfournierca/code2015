import re
import zipfile 

def extract_category_name_id(name):
    if not name:
        return None, None
    i = re.search(r"^\s*([\d\.]*)\s*(.*)", name)
    if not i:
        return None, None
    return i.group(1), i.group(2)


def get_input_from_zip(archive_path, zip_path):
    z = zipfile.ZipFile(archive_path, "r")
    return z.open(zip_path)
