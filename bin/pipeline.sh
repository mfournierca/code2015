#!/usr/bin/env sh

#
# the data processing pipeline
#

DATA_SOURCE_URL="http://www12.statcan.gc.ca/open-gc-ouvert/?CTLG=99-012-X2011056"
DATA_DIR="../data/"
DATA_ARCHIVE=$DATA_DIR"data.zip"

# download source data
wget --continue -O $DATA_ARCHIVE $DATA_SOURCE_URL

# build category mapping, legend
python ../src/data_processing/build_legend.py 


# parse raw data

# copy into shiny dir

# build and upload docker app

