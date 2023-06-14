import requests
import pprint
import json
import time
from pymongo import MongoClient
import logging

log = logging.basicConfig(filename="twitter.log", level=logging.DEBUG, force=True)
logger = logging.getLogger('twitter')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info("Process is Started........")


pp = pprint.PrettyPrinter(indent=4,sort_dicts=True)

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMW%2FiQEAAAAAwRGhaVxGHRRjYVly%2FqLd4%2FAkKWY%3DCbX51APYnQrx1jGt45yQilDkF69OYTuZ1k6VcSTIndDD1JMGWt"

# query_params = {
#                 'tweet.fields': 'author_id,text,geo,created_at,lang',
#                 'user.fields': 'id,name,username,created_at,public_metrics,conversation_id'
#                 }

query_params = {
                'expansions': 'author_id,entities.mentions.username',
                'tweet.fields': 'id,text,author_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets',
                'user.fields': 'username'
                }

client = MongoClient()
client = MongoClient("mongodb://127.0.0.1:27017/")
for db in client.list_database_names():
    if db == "tweeterdb":
        pass
    else:
        mydb = client['tweeterdb']
        mycol_count = mydb['storeCount']
        mycol_data = mydb["tweeterData"]

#https://api.twitter.com/2/tweets/search/stream sample stream of data 1%

def create_url():
    
    sample_api = "https://api.twitter.com/2/tweets/sample/stream"
    return sample_api


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r

def insert_count_in_db(total_count,matched_count,time_date):
    logging.info("INSIDE FUNCTION")
    total_tweets = total_count
    matched_tweets = matched_count
    logging.info("Total Tweets: " +total_tweets)
    logging.info("Matched Tweets: "+matched_tweets)
    logging.info("Matched data at : " +str(time.strftime("%c", time_date)))
    insert_data = {
        "timestamp" : str(time.strftime("%c", time_date)),
        "total_tweets" : total_tweets,
        "matched_tweets" : matched_tweets
        }
    mydb.storeCount.insert_one(insert_data)    
    #connect to database and store value of total_tweets and matched_tweets in db with date and time stamp
    
def connect_to_endpoint(url):
    
    total_count = 0 
    matched_count = 0
    response = requests.request("GET", url, auth=bearer_oauth, stream=True, params = query_params)
    logging.info(response.status_code)
    t = time.localtime()
    logging.info("Start time " + str(time.strftime("%c", t)))
    logging.info("AFTER RESET DATE total responses : " + str(total_count))
    logging.info("AFTER RESET DATA matched responses : " + str(matched_count))
        
    for response_line in response.iter_lines():
        #print(type(response_line))
        #print(time.strftime("%H:%M:%S", t))
        if (time.localtime().tm_hour == 0 and time.localtime().tm_min == 0 and time.localtime().tm_sec == 0 )  :
            insert_count_in_db(total_count,matched_count,time.localtime())
            logging.info("Reset Counter")
            break
        
        total_count += 1
        if response_line :
            
            json_response = json.loads(response_line)
            #print(type(json_response))
            #pp.pprint(json_response)
            
            if json_response["data"]["lang"] == 'en':
                
                if (json_response["data"]["text"].find("FIFAWorldCupQatar2022") != -1) or (json_response["data"]["text"].find("FIFA") != -1) or (json_response["data"]["text"].find("Qatar") != -1) or (json_response["data"]["text"].find("FIFAWorldCup") != -1): 
                    matched_count += 1
                    mydb.tweeterData.insert_one(json_response)
                    #pp.pprint(json_response)
                    logging.info(time.strftime("%H:%M:%S", time.localtime()))
                    logging.info("total responses : " + str(total_count))
                    logging.info("matched responses : " + str(matched_count))
                    logging.info("Tweets: "+json_response["data"]["text"])

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

def main():
    url = create_url()
    timeout = 0

    while True:
        connect_to_endpoint(url)
        timeout += 1


if __name__ == "__main__":
    main()
