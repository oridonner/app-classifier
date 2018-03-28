#!/usr/bin/env python2.7
import os

from python_libs import english_classifier as ec
from python_libs import file_loader as fl


def main():
    training_file = 'data/input/Examples.csv'
    classify_file = 'data/input/Classify.csv'
    output_data_path = 'data/output'

    training_file_loader = fl.FileLoader(training_file,'training')
    training_dict = training_file_loader.get_dict()
    
    classify_file_loader = fl.FileLoader(classify_file,'classify')
    classify_dict = classify_file_loader.get_dict()
    
    english_classifier = ec.EnglishClassifier(training_dict)

    print english_classifier.get_sframe_data('training')
    english_classifier.predict_is_supported(classify_dict)
    print english_classifier.get_sframe_data('classify')



if __name__ == "__main__":
    main()