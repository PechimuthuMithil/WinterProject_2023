'''
This script will handle jod of finding the right users to notify once an item is found.
Written by Mithil Pechimuthu.
'''

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from concurrent.futures import ThreadPoolExecutor
import psycopg2
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to fetch ItemID and Description from found_items table
def fetch_items_from_database():
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            database="winterproject"
        )

        cursor = conn.cursor()
        query = '''
            SELECT ides, uemail FROM lost;
        '''
        cursor.execute(query)
        
        items = [{'Description': row[0], 'Email': row[1]} for row in cursor.fetchall()]

        return items

    except (Exception, psycopg2.Error) as error:
        print("Error fetching items from database:", error)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

def findID(desc):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            database="winterproject"
        )

        cursor = conn.cursor()
        query = '''
            SELECT iid FROM itmes WHERE ides = %s;
        '''
        cursor.execute(query,(desc,))
        id = int(cursor.fetchall())
        return id

    except (Exception, psycopg2.Error) as error:
        print("Error fetching items from database:", error)
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()   
# Usage example

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
      result.append({'Email':item['Email'], 'Description':item['Description'], 'Score':float(similarity_score)})
  return result

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0 

def send_notification_email(receiver_email, found_item_url):
    # Email content
    subject = "Found an item you lost"
    body = f"We found an item similar to your description! Please click <a href='{found_item_url}'>here</a> to see the details of the found item and to claim it."
    sender_email = "lostnfound.noreply@gmail.com"
    sender_pass = "MailNotification"
    # Setup the email message
    message = MIMEMultipart()
    message["From"] = sender_email  # Your email address
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach HTML content
    message.attach(MIMEText(body, "html"))
    context = ssl.create_default_context()
    # Establish a connection to the SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        #server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_pass)
        server.send_message(message)

#### Cleaning and initialising the Database of found items. Also adding the vector embeddings ###
### Will be later replaced by calls to an actual database ###

database = fetch_items_from_database()
# print(database)
### USING ANALYTICAL METHODS ###
### Taking User Query and Pre-processing it ###
user_query = input()
id = findID(user_query)
query_words = word_tokenize(user_query)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
filtered_words = [lemmatizer.lemmatize(word.lower()) for word in query_words if word.lower() not in stop_words]
filtered_query = ' '.join(filtered_words)

#### Creating a Ranking (MULTI-THREADED) ###
minThresh = 0.1
num_threads = 2

result = []
sub_database_size = max(len(database)%num_threads,len(database)//num_threads)
sub_databases = [database[i:i + sub_database_size] for i in range(0, len(database), sub_database_size)]

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    sub_results = executor.map(similarity_search_jaccard, sub_databases)
    for sub_result in sub_results:
        result.extend(sub_result)

if (len(result) != 0):
    for email, des, score in result:
        send_notification_email(email, f"http://lostnfound.iitgn.ac.in:5000/details/{id}")
    # for item_id, description, similarity_score in result :
    #     print(f"Item ID: {item_id}, Description: {description}, Jaccard Similarity Score: {similarity_score}\n")
    print(0)
else:
    #print("No matching items found. Please try again later.")
   print(-1)