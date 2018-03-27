#!/usr/bin/env python2.7
import os

from python.english_classifier_lib import english_classifier as eng_clsf
from python.segment_classifier_lib import segment_classifier as seg_clsf
from python.class_lib import mobileApps

def map_column(column_name,row):
    for idx,column in enumerate(row):
        if row[idx] == column_name:
            return idx

def main():
    source_data_file = 'data/input/Examples.csv'
    target_data_file = 'data/input/Classify.csv'
    output_data_path = 'data/output'

    source_data_dict = mobileApps.import_source_data(source_data_file)
    target_data_dict = mobileApps.import_target_data(target_data_file)

    sf = eng_clsf.create_model(source_data_dict)
    print sf.select_columns(['appName','description','is_english'])
        
if __name__ == "__main__":
    main()