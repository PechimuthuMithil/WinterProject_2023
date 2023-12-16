''' 
This is a trila script wirtten by Mithil Pechimuthu
It tries to rank the entries in a database based on a query. 
I will use thos to compare Doc2Vec and BERT embeddings. 
This is also multi threaded. 
'''
#### FINAL SENTENCE-BERT BASET RANKER ####
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from concurrent.futures import ThreadPoolExecutor

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def similarity_search_jaccard(database):
  ''' Function for the threads to use while searching '''
  result = []
  for item in database:
    description = item['Description']
    words = word_tokenize(description)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]
    similarity_score = jaccard_similarity(set(filtered_query.split()), set(filtered_words))
    if (similarity_score >= minThresh):
      result.append({'ItemID':item['ItemID'], 'Description':item['Description'], 'Score':float(similarity_score)})
  return result

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0 

#### Cleaning and initialising the Database of found items. Also adding the vector embeddings ###
### Will be later replaced by calls to an actual database ###

database = [
    {'ItemID': 1, 'Description': "Found a red wallet in the hostel area"},
    {'ItemID': 2, 'Description': "Found black phone near the park"},
    {'ItemID': 3, 'Description': "Found keys in the hostel area"},
    {'ItemID': 4, 'Description': "One Red & Blue Colour Pendrive (SANDISK) found in AB-03"},
    {'ItemID': 5, 'Description': "Ten Rupees foind in AB-03"},
    {'ItemID': 6, 'Description': "One Blue & Black Colour Plastic Water Bottle (Stryder H2o) found in Kyzeel Hostel"},
    {'ItemID': 7, 'Description': "Found a maruti suzuki car key near Amul Store"},
    {'ItemID': 8, 'Description': "Found a black wallet next to Amul Store. It has some cash and some cards."},
    {'ItemID': 9, 'Description': "(seven) keys were found from Sports Complex Cricket Ground near Mango tree"},
    {'ItemID': 10, 'Description': "(10) Keys were found behind AB-1 Two degree cafe"},
    {'ItemID': 11, 'Description': "Found one Black Colour Steel Water Bottle (IIT LOGO) in AB-03"},
    {'ItemID': 12, 'Description': "Found One Grey Colour Measuring Tape 30m (Freemans) in AB-07"},
    {'ItemID': 13, 'Description': "One Black & Gold Colour Chain in Aibaan hostel"},
    {'ItemID': 14, 'Description': "One Black & Red Colour Earphone (Costar) found in hiqom"},
    {'ItemID': 15, 'Description': "One Silver Colour Steel Water Bottle (From 29 Seater Bus) at Gate 1"},
    {'ItemID': 16, 'Description': "One Grey Colour USB-C Fusion Max-6 (ALOGIC) found in AB-05"},
    {'ItemID': 17, 'Description': "Found one Black Colour Cycle Number Lock at gate 1"},
    {'ItemID': 18, 'Description': "One Silver Colour Chain With Krishna Locket in Aibaan hostel."}
]

### USING ANALYTICAL METHODS ###

### Taking User Query and Pre-processing it ###
user_query = input()
query_words = word_tokenize(user_query)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
filtered_words = [lemmatizer.lemmatize(word.lower()) for word in query_words if word.lower() not in stop_words]
filtered_query = ' '.join(filtered_words)

#### Creating a Ranking (MULTI-THREADED) ###
minThresh = 0.1
num_threads = 2

result = []
sub_database_size = len(database)//num_threads
sub_databases = [database[i:i + sub_database_size] for i in range(0, len(database), sub_database_size)]

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    sub_results = executor.map(similarity_search_jaccard, sub_databases)
    for sub_result in sub_results:
        result.extend(sub_result)

result.sort(key=lambda x: x['Score'], reverse=True)
if (len(result) != 0):
   print(result)
    # for item_id, description, similarity_score in result :
    #     print(f"Item ID: {item_id}, Description: {description}, Jaccard Similarity Score: {similarity_score}\n")
else:
    print("No matching items found. Please try again later.")