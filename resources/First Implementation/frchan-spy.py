import requests,datetime, time,pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime as dt
import logging

log = logging.basicConfig(filename="frchan.log", level=logging.DEBUG, force=True)
logger = logging.getLogger('frchan')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info("Process is Started........")

#A JSON representation of a board catalog. Includes all OPs and their preview replies.
res = requests.get('https://a.4cdn.org/sp/catalog.json')
fchanData = res.json()

client = MongoClient()
client = MongoClient("mongodb://127.0.0.1:27017/")
for db in client.list_database_names():
    if db == "frchanThreads":
        pass
    else:
        mydb = client['frchanThreads']
        mycol_data = mydb["frchanData"]

def fchan():
    for pageno, post in enumerate(fchanData):
        for thread in fchanData[pageno]['threads']:
            yield thread

def get_threads(key: str, default='NaN'):
    return threads.get(key, default)


while True:
    if time.localtime().tm_hour%2 == 0 and time.localtime().tm_min <10:   
        for threads in fchan():
            if 'last_replies' in threads:
                comCount=0
                for comment in threads['last_replies']:
                    comCount+=1
                    com = comment.get('com','NaN')
                    comTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.get('time','NaN')))
                    geoLoca = comment.get('country_name','NaN')
                    #logger.info("Inserting")
                    insert_data = {
                        "timestamp" : comTime,
                        "total_comms" : comCount,
                        "coms" : com,
                        "geoLocation" :geoLoca
                        }
                    mydb.frchanData.insert_one(insert_data)
                logging.info("timestamp:"+comTime)
                logging.info("coms:"+com)
                    #logger.info("Insert Success")
    else:
        logging.info("Sleep")
        time.sleep(600)
                    

def main():
    fchan()


if __name__ == "__main__":
    main()
