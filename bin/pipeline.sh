#!/usr/bin/env sh

#
# the data processing pipeline
#

BIN_DIR=`dirname $0`"/"

DATA_SOURCE_URL="http://www12.statcan.gc.ca/open-gc-ouvert/?CTLG=99-012-X2011056"
DATA_DIR=$BIN_DIR"../data/"
DATA_ARCHIVE=$DATA_DIR"/source/data.zip"

CATEGORY_MAP_JSON_PATH=$DATA_DIR"category_mapping.json"
CIP_MAP_CSV_PATH=$DATA_DIR"cip_mapping.csv"
NOC_MAP_CSV_PATH=$DATA_DIR"noc_mapping.csv"
PROCESSED_DATA_PATH=$DATA_DIR"dump.csv"

SRC_DIR=$BIN_DIR"../src/"

mkdir -p `dirname $DATA_ARCHIVE`

# download source data
wget --continue -O $DATA_ARCHIVE $DATA_SOURCE_URL

# build category mapping, legend
echo building category and CIP mapping
PYTHONPATH=.. python $SRC_DIR"data_processing/build_legend.py" $DATA_ARCHIVE $CATEGORY_MAP_JSON_PATH $CIP_MAP_CSV_PATH $NOC_MAP_CSV_PATH

# parse raw data
echo preparing data
#PYTHONPATH=.. python $SRC_DIR"data_processing/dump_raw_data.py" csv $DATA_ARCHIVE $CATEGORY_MAP_JSON_PATH $PROCESSED_DATA_PATH

# build and upload docker app
docker build -t mfournierca/code2015 $BIN_DIR"../"
docker push mfournierca/code2015
