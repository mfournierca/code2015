#!/usr/bin/env sh

#
# the data processing pipeline
#

DATA_SOURCE_URL="http://www12.statcan.gc.ca/open-gc-ouvert/?CTLG=99-012-X2011056"
DATA_DIR="../data/"
DATA_ARCHIVE=$DATA_DIR"data.zip"

CATEGORY_MAP_JSON_PATH=$DATA_DIR"category_mapping.json"
CIP_MAP_CSV_PATH=$DATA_DIR"cip_mapping.csv"
NOC_MAP_CSV_PATH=$DATA_DIR"noc_mapping.csv"
PROCESSED_DATA_PATH=$DATA_DIR"dump.csv"
mkdir $DATA_DIR

# download source data
wget --continue -O $DATA_ARCHIVE $DATA_SOURCE_URL

# build category mapping, legend
echo building category and CIP mapping
PYTHONPATH=.. python ../src/data_processing/build_legend.py $DATA_ARCHIVE $CATEGORY_MAP_JSON_PATH $CIP_MAP_CSV_PATH $NOC_MAP_CSV_PATH

# parse raw data
echo preparing data
PYTHONPATH=.. python ../src/data_process/dump_raw_data.py $DATA_ARCHIVE $CATEGORY_MAP_JSON_PATH $PROCESSED_DATA_PATH

# copy into shiny dir


# build and upload docker app

