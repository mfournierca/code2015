"""Run the data processing pipeline. 

This script runs through the data processing pipeline from downloading the 
raw data, through preprocessing, cleaning, etc and ends with the data loaded
into a data base ready for use by an application. 

Usage: 

    pipeline.py --data-source-url=<url>

Options:
    
    --data-source-url=<url>  The source url for the data archive containing
                             the xml data file and the structure file. 
                             [default: http://open.canada.ca/data/en/dataset/64874af2-467c-41a6-8bda-efe99cfa3a61]
"""

from docopt import docopt

import dump_raw_data
import build_legend

def run(data_source_url):
    pass


if __name__ == "__main__":
    args = docopt(__doc__)
    run(args["--data-source-url"])

