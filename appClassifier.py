#!/usr/bin/env python2.7
import os

from python_libs import app_classifier as ac
from python_libs import file_loader as fl


def main():
    training_file = 'data/input/Examples.csv'
    classify_file = 'data/input/Classify.csv'
    output_data_file = 'data/output/Predict.csv'

    training_file_loader = fl.FileLoader(training_file,'training')
    training_dict = training_file_loader.get_dict()
    
    classify_file_loader = fl.FileLoader(classify_file,'classify')
    classify_dict = classify_file_loader.get_dict()
    
    app_classifier = ac.AppClassifier(training_dict)

    print app_classifier.get_sframe_data('training')
    app_classifier.predict_segment(classify_dict,output_data_file)
    print app_classifier.get_sframe_data('classify')




if __name__ == "__main__":
    main()