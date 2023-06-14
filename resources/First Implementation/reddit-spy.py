import requests
import pprint
import json
from pymongo import MongoClient
import time
import logging

log = logging.basicConfig(filename="reddit.log", level=logging.DEBUG, force=True)
logger = logging.getLogger('reddit')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info("Process is Started........")

pp = pprint.PrettyPrinter(indent=4,sort_dicts=True)

 
client = MongoClient()
client = MongoClient("mongodb://127.0.0.1:27017/")


for db in client.list_database_names():
    if db == "redditdb":
        pass
    else:
        mydb = client['redditdb']
        mycol_count = mydb['redditCount']
        mycol_data = mydb["redditData"]



# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('UB3whFhun4mxM1T16vFDcQ', 'qfuUbXBLi7QJwleLOu01dwnJrjm2-Q')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'Moist_Government_734',
        'password': 'Shravani123!'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

iter = 0;
subreddits= ['FIFA','Sports','WorldcupQatar2022','football']

FIFA_count = 0 
Sports_count = 0 
WorldcupQatar2022_count = 0 
football_count = 0 
loop_end = time.time() + 5
while True :  
    if time.localtime().tm_hour%2 == 0 and time.localtime().tm_min <10: 
        logging.info("\n\nStart Time iter : " + str(iter) +"  "+ str(time.strftime("%c", time.localtime())))
        for subr in subreddits:   
            
            get_url = "https://oauth.reddit.com/r/" + subr +"/comments?limit=1"
            logging.info("\n"+get_url)
            res = requests.get(get_url, headers=headers)
                
            counts_subreddits = {
                "time" : str(time.strftime("%c", time.localtime())),
                "FIFA_count" : FIFA_count,
                "Sports_count" : Sports_count,
                "WorldcupQatar2022_count" : WorldcupQatar2022_count,
                "football_count" : football_count
                }
            
            mydb.redditCount.insert_one(counts_subreddits)
            
            FIFA_count = 0 
            Sports_count = 0 
            WorldcupQatar2022_count = 0 
            football_count = 0
            iter = 0
            logging.debug('Reset Counter')
            
            temp = json.loads(res.text)
            
            for item in temp["data"]["children"] :
                insert_data = {
                    "linkURL" : item["data"]["link_url"],
                    "linkTitle" : item["data"]["link_title"],
                    "commentID" : item["data"]["id"],
                    "CommBody" : item["data"]["body"],
                    "Subreddit" : item["data"]["subreddit"]
                    }
                
                mydb.redditData.insert_one(insert_data)
    
                if subr == "FIFA":
                    FIFA_count += 1
                    
                    
                elif subr == "Sports":
                    Sports_count += 1
                    
                elif subr == "WorldcupQatar2022":
                    WorldcupQatar2022_count += 1                   
                    
                elif subr == "football":
                    football_count += 1                  
                   
            logging.info("Subreddit : " + subr + "\nFIFA_count : " + str(FIFA_count))
            logging.info("Subreddit : " + subr + "\nSports_count : " + str(Sports_count))
            logging.info("Subreddit : " + subr + "\nWorldcupQatar2022_count: " + str(WorldcupQatar2022_count))
            logging.info("Subreddit : " + subr + "\nfootball_count : " + str(football_count))
        iter+=1
    else:
        logging.info("Sleep")
        time.sleep(600)
