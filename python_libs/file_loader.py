import csv

class mobile_app(object):
    def __init__(self):
        self.appId = None
        self.package = None
        self.appName = None
        self.segment = None
        self.description = None

    def to_dict(self):
        app_dict={}
        app_dict['appId'] = self.appId
        app_dict['package'] = self.package 
        app_dict['appName'] = self.appName 
        app_dict['segment'] = self.segment
        app_dict['description'] = self.description
        return app_dict

def columns_dict(columns_row):
    columns_dict = {}
    for idx,column in enumerate(columns_row):
        columns_dict[column] = idx
    return columns_dict

def training_file_to_dict(file_path):
    app = mobile_app()
    training_dict = []
    columns = {}
    with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            i=1
            for idx,row in enumerate(reader):
                if idx == 0:
                    columns = columns_dict(row)
                else:
                    app.appId = row[columns['appId']]
                    app.package = row[columns['package']]
                    app.appName = row[columns['appName']]
                    app.segment = row[columns['segment']]
                    app.description = row[columns['description']]
                    training_dict.append(app.to_dict())
    return training_dict 

def classify_file_to_dict(file_path):
    app = mobile_app()
    classify_dict = []
    columns = {}
    with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            i=1
            for idx,row in enumerate(reader):
                if idx == 0:
                    columns = columns_dict(row)
                else:
                    app.appId = row[columns['appId']]
                    app.package = row[columns['package']]
                    app.appName = row[columns['appName']]
                    app.description = row[columns['description']]
                    classify_dict.append(app.to_dict())
    return classify_dict 


    