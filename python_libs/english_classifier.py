import graphlab as gl
import unicodedata
import operator

class EnglishClassifier(object):
    # Import data into graphlab's SFrame dataframe object when instantiating an object
    def __init__(self,source_data_dict):    
        self.english_classifier = None
        self.sf = self._load_data(source_data_dict)
        self.tf = None
        
        self._add_helper_columns(self.sf)
        self._build_cluster_model()
        self._is_supported()
        self._build_english_classifier()
        self._delete_helper_columns(self.sf)
        self._build_segment_classifier()

    # Get SFrame dataframe object
    def get_sframe_data(self,data_type):
        if data_type == 'training':
            return self.sf
        if data_type == 'classify':
            return self.tf

    # Get english classifier model
    def get_english_classifier(self):
        return self.english_classifier

    # Predict if app is supported (if it's description language is english), using the english classifier model
    def predict_is_supported(self,target_data_dict):
        self.tf = self._load_data(target_data_dict)
        self._add_helper_columns(self.tf)
        self.tf['is_supported_predict'] = self.english_classifier.predict(self.tf)
        self._delete_helper_columns(self.tf)




    # Import data as dict to SFrame dataframe object
    def _load_data(self,data_dict):
        sframe = gl.SFrame(data_dict)
        return sframe.unpack('X1',column_name_prefix="")

    # Add helper columns to SFrame dataframe object
    def _add_helper_columns(self,sframe):
        sframe['short_desc'] = sframe.apply(_short_desc)
        sframe['short_word_count']=gl.text_analytics.count_words(sframe['short_desc'],to_lower=True)
        sframe['short_tf_idf'] = gl.text_analytics.tf_idf(sframe['short_word_count'])
        sframe['tail_tf_idf'] = sframe.apply(_sort_dict)

    # Removes helper columns from SFrame dataframe object
    def _delete_helper_columns(self,sframe):
        sframe.remove_column('short_word_count')
        sframe.remove_column('short_desc')
        sframe.remove_column('short_tf_idf')
        sframe.remove_column('tail_tf_idf')

    # Build kmean clustering model for predicting cluster id
    def _build_cluster_model(self):
        while True:
            kmean=gl.kmeans.create(self.sf, num_clusters=5,features=['tail_tf_idf'] ,max_iterations=15)
            if kmean.training_iterations > 6:
                self.sf['cluster_id']=kmean.predict(self.sf)
                self.kmean_model = kmean
                break 

    # English is the most common language between lating languages, this function predicts the right cluster_id for english.
    def _build_latin_apps_cluster(self):
        cluster_ids = self.sf['cluster_id'].unique()
        cluster_list=[]
        for cluster_id in cluster_ids:
            cluster_dict={}
            cluster_dict['cluster_id']= cluster_id
            cluster_dict['num_apps'] = len(self.sf[self.sf['cluster_id'] == cluster_id])
            cluster_dict['num_apps_latin'] = len(self.sf[(self.sf['cluster_id'] == cluster_id) & (self.sf['is_latin'])])
            num_apps_latin = cluster_dict['num_apps_latin']
            cluster_list.append(cluster_dict)
        return cluster_list

    # Clusters created by build_cluster are not tagged, this function predicts the proper english tag for cluster_id. Only english apps are supported.
    def _is_supported(self):
        self.sf['char_count'] = gl.text_analytics.count_ngrams(self.sf['short_desc'],n=1,to_lower=True,method="character")
        self.sf['is_latin']=self.sf['char_count'].apply(_is_latin)
        latin_apps_cluster = self._build_latin_apps_cluster()
        print latin_apps_cluster
        english_cluster_id = _predict_english_cluster_id(latin_apps_cluster) 
        self.sf['is_supported'] = self.sf.apply(lambda x: True if x['cluster_id'] == english_cluster_id else False) 
        # Clean SFrame 
        self.sf.remove_column('cluster_id')
        self.sf.remove_column('char_count')
        self.sf.remove_column('is_latin')

    # Create classification model for english language detection from cluster model 
    def _build_english_classifier(self):
        train_data,test_data = self.sf.random_split(.8,seed=0)
        english_classifier = gl.classifier.create(train_data,target='is_supported',features=['tail_tf_idf'],validation_set=test_data)
        self.english_classifier = english_classifier
        
    def _build_segment_classifier(self):
        pass


## This function is used for calculating short_desc column ##
# Create a short description for mobile app. Take first 5 sentences.  
def _short_desc(row):
    desc_sentences = row['description'].split('.')[:5]
    return ''.join(desc_sentences)

## These functions are used for calculating tail_tf_idf column ##
# Converts a list into a dict (for finding top 15 lowest tf-idf's)
def _convert_list(sorted_list):
    dct={}
    for k in sorted_list[:15]:
        dct[k[0]]=k[1]
    return dct

# Sorting tf-idf's in ascending order and outputing a dict of 15 most common words
def _sort_dict(row):
    dct = row['short_tf_idf']
    sorted_list=sorted(dct.items(), key=operator.itemgetter(1))
    sorted_dict = _convert_list(sorted_list)
    return sorted_dict

## These functions are used for calculating is_supported column ##
def _is_latin(char_count_dict):
    param=0
    chars=0
    for key, value in char_count_dict.iteritems():
        try:
            if unicodedata.category(key.decode('utf-8')) == 'Ll':
                chars += value
        except:
            chars -=value
    return 1 if chars>0 else 0

def _predict_english_cluster_id(latin_apps_cluster):
    maxPricedItem = max(latin_apps_cluster, key=lambda x:x['num_apps_latin'])
    return maxPricedItem['cluster_id']


    

