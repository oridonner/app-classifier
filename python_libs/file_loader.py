import csv

class FileLoader(object):
    def __init__(self,file_path,file_type):
        self.appId = None
        self.package = None
        self.appName = None
        self.segment = None
        self.description = None
        self.dict = self._file_to_dict(file_path,file_type)

    def get_dict(self):
        return self.dict

    def _to_dict(self,file_type):
        app_dict={}
        app_dict['appId'] = self.appId
        app_dict['package'] = self.package 
        app_dict['appName'] = self.appName 
        if file_type == 'training':
            app_dict['segment'] = self.segment
        app_dict['description'] = self.description
        return app_dict

    def _columns_dict(self,columns_row):
        columns_dict = {}
        for idx,column in enumerate(columns_row):
            columns_dict[column] = idx
        return columns_dict

    def _file_to_dict(self,file_path,file_type):
        training_dict = []
        columns = {}
        with open(file_path, mode='r') as infile:
                reader = csv.reader(infile)
                i=1
                for idx,row in enumerate(reader):
                    if idx == 0:
                        columns = self._columns_dict(row)
                    else:
                        self.appId = row[columns['appId']]
                        self.package = row[columns['package']]
                        self.appName = row[columns['appName']]
                        if file_type == 'training':
                            self.segment = row[columns['segment']]
                        self.description = row[columns['description']]
                        training_dict.append(self._to_dict(file_type))
        return training_dict     