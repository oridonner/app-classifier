import csv

class mobileApp(object):
    def __init__(self):
        self.appId = None
        self.package = None
        self.appName = None
        self.segment = None
        self.description = None

    # def importApps(self,file_path):
    #     pass

    def toDict(self):
        appDict={}
        appDict['appId'] = self.appId
        appDict['package'] = self.package 
        appDict['appName'] = self.appName 
        appDict['segment'] = self.segment
        appDict['description'] = self.description
        return appDict

def columns_dict(columns_row):
    columns_dict = {}
    for idx,column in enumerate(columns_row):
        columns_dict[column] = idx
    return columns_dict

def import_source_data(file_path):
    source_apps_data = mobileApp()
    apps_list = []
    columns = {}
    with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            i=1
            for idx,row in enumerate(reader):
                if idx == 0:
                    columns = columns_dict(row)
                else:
                    source_apps_data.appId = row[columns['appId']]
                    source_apps_data.package = row[columns['package']]
                    source_apps_data.appName = row[columns['appName']]
                    source_apps_data.segment = row[columns['segment']]
                    source_apps_data.description = row[columns['description']]
                    apps_list.append(source_apps_data.toDict())
    return apps_list 

def import_target_data(file_path):
    source_apps_data = mobileApp()
    apps_list = []
    columns = {}
    with open(file_path, mode='r') as infile:
            reader = csv.reader(infile)
            i=1
            for idx,row in enumerate(reader):
                if idx == 0:
                    columns = columns_dict(row)
                else:
                    source_apps_data.appId = row[columns['appId']]
                    source_apps_data.package = row[columns['package']]
                    source_apps_data.appName = row[columns['appName']]
                    source_apps_data.description = row[columns['description']]
                    apps_list.append(source_apps_data.toDict())
    return apps_list 


    