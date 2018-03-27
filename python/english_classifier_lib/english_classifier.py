import graphlab as gl

# Create SFrame from list of dictionaries https://forum.turi.com/discussion/1455/
def import_data(data_dict):
    sf =gl.SFrame(data_dict)
    return sf.unpack('X1',column_name_prefix="")

## This function is used for calculating short_desc column ##
# Create a short description for mobile app. Take first 5 sentences.  
def short_desc(row):
    desc_sentences = row['description'].split('.')[:5]
    return ''.join(desc_sentences)

## These functions are used for calculating tail_tf_idf column ##
# Converts a list into a dict (for finding top 15 lowest tf-idf's)
def convert_list(sorted_list):
    dct={}
    for k in sorted_list[:15]:
        dct[k[0]]=k[1]
    return dct

# Sorting tf-idf's in ascending order and outputing a dict of 15 most common words
import operator
def sort_dict(row):
    dct = row['short_tf_idf']
    sorted_list=sorted(dct.items(), key=operator.itemgetter(1))
    sorted_dict = convert_list(sorted_list)
    return sorted_dict

## These functions are used for calculating is_supported column ##
import unicodedata
def is_latin(char_count_dict):
    param=0
    chars=0
    for key, value in char_count_dict.iteritems():
        try:
            if unicodedata.category(key.decode('utf-8')) == 'Ll':
                chars += value
        except:
            chars -=value
    return 1 if chars>0 else 0

# English is the most common language between lating languages, this function predicts the right cluster_id for english.
def build_latin_apps_cluster(sf):
    cids = sf['cluster_id'].unique()
    cluster_list=[]
    for cid in cids:
        cluster_dict={}
        num_apps_latin = len(sf[(sf['cluster_id'] == cid) & (sf['is_latin'])])
        num_apps = len(sf[sf['cluster_id'] == cid])
        cluster_dict['cluster_id']= cid
        cluster_dict['num_apps'] = num_apps
        cluster_dict['num_apps_latin'] = num_apps_latin
        num_apps_latin = cluster_dict['num_apps_latin']
        cluster_list.append(cluster_dict)
    return cluster_list

def predict_english_cluster_id(latin_apps_cluster):
    maxPricedItem = max(latin_apps_cluster, key=lambda x:x['num_apps_latin'])
    return maxPricedItem['cluster_id']

def is_supported(row):
    result = True
    if row['cluster_id'] == 1:
        result = False
    return result

def iterate_kmean_model(sf):
    while True:
        kmean=gl.kmeans.create(sf, num_clusters=5,features=['tail_tf_idf'] ,max_iterations=15)
        if kmean.training_iterations > 6:
            return kmean 


# Create kmeans clustering model for detecting supported mobile apps
def create_english_classifier(source_data_dict):
    sf = import_data(source_data_dict)
    # Create required columns for calculating tail_tf_idf feature
    sf['short_desc'] = sf.apply(short_desc)
    sf['short_word_count']=gl.text_analytics.count_words(sf['short_desc'],to_lower=True)
    sf['short_tf_idf'] = gl.text_analytics.tf_idf(sf['short_word_count'])
    sf['tail_tf_idf'] = sf.apply(sort_dict)
    # Create kmeans clustering model to predict cluster_id (we still don't know which cluster id refers to english)
    kmean = iterate_kmean_model(sf)
    sf['cluster_id']=kmean.predict(sf)
    # Create required columns for calculating is_supported column
    sf['char_count'] = gl.text_analytics.count_ngrams(sf['short_desc'],n=1,to_lower=True,method="character")
    sf['is_latin']=sf['char_count'].apply(is_latin)
    latin_apps_cluster = build_latin_apps_cluster(sf)
    print latin_apps_cluster
    english_cluster_id = predict_english_cluster_id(latin_apps_cluster) 
    sf['is_english'] = sf.apply(lambda x: True if x['cluster_id'] == english_cluster_id else False) 
    # Create classification model for english language detection from cluster model 
    train_data,test_data=sf.random_split(.8,seed=0)
    english_classifier = gl.classifier.create(train_data,target='is_english',features=['tail_tf_idf'],validation_set=test_data)
    return english_classifier

def create_segment_classifier(source_data_dict):
    return segment_classifier