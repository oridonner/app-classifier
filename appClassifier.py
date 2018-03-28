#!/usr/bin/env python2.7
import os

from python_libs import app_classifier as ac
from python_libs import english_classifier as ec
def map_column(column_name,row):
    for idx,column in enumerate(row):
        if row[idx] == column_name:
            return idx

def main():
    training_file = 'data/input/Examples.csv'
    classify_file = 'data/input/Classify.csv'
    output_data_path = 'data/output'

    app_classifier = ac.AppClassifier()
    app_classifier.load_training_file(training_file)
    app_classifier.load_classify_file(classify_file)
    training_dict = app_classifier.get_training_dict()
    classify_dict = app_classifier.get_classify_dict()
    english_classifier = ec.EnglishClassifier(training_dict)
    #english_classifier.build_features()
    #english_classifier.build_cluster()
    #english_classifier.is_supported()
    #english_classifier.build_english_classifier()
    print english_classifier.get_data()
    model = english_classifier.get_english_classifier()
    # app_classifier.build_english_classifier_model(training_dict)
    
    #source_data_dict = mobileApps.import_source_data(source_data_file)
    #target_data_dict = mobileApps.import_target_data(target_data_file)

    #sf = eng_clsf.init(source_data_dict)
    
    
    #print sf.select_columns(['appName','description','is_english'])
    


if __name__ == "__main__":
    main()