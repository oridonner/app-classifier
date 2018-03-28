from python_libs import file_loader as fl
from python_libs import english_classifier as ec

class AppClassifier(object):
    #def __init__(self):
    
    def load_training_file(self,training_file):
        self.training_dict = fl.classify_file_to_dict(training_file)

    def get_training_dict(self):
        return self.training_dict

    def load_classify_file(self,classify_file):
        self.classify_dict = fl.classify_file_to_dict(classify_file)
    
    def get_classify_dict(self):
        return self.classify_dict
    # Use training dict to build english classification model, use this model to predict if application is in english
    # def predict_is_english(self,training_dict,classify_dict):
    #     self.english_classifier = ec.create_english_classifier(training_dict)