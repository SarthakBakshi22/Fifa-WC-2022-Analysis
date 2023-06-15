import matplotlib.pyplot as plt
from datetime import datetime
import pymongo
import datetime as dttime
import time


# consider the start date as 2021-february 1 st
start_date = dttime.date(2022, 11, 4)
 
# consider the end date as 2021-march 1 st
end_date = dttime.date(2022, 11, 14)
 
# delta time
delta = dttime.timedelta(days=1)

client = pymongo.MongoClient()

db = client['redditdb']
collec = db['redditPolitics']

reddit_time = []
matchCount = []
count = 0

while (start_date <= end_date):
    print("while start")
    
    count = 0
    for item in collec.distinct('createdDate'):
        #obj = item['_id']

        times = item
        #print(type(times))
        #print(times)
        #print("--------")
        created_time = time.strftime('%Y-%m-%d', time.localtime(times))
        created_time = datetime.strptime(created_time, '%Y-%m-%d')
        #print(created_time)
        #print(type(created_time))
        #print("--------")
        date_inst = created_time.date()
        #print(date_inst)
        #print(type(date_inst))
        #print("--------")

        if date_inst == start_date:
            #print("match")
            count+=1
            continue
    #print(start_date, end="\n")
    #print(type(start_date))
    reddit_time.append(start_date.strftime("%Y-%m-%d"))
    start_date += delta
    matchCount.append(count)

print(matchCount)
print(reddit_time)

barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(reddit_time, matchCount, color ='black',
        width = 0.4)
 
plt.xlabel("Time")
plt.ylabel("Politics Count")
plt.title("Reddit Politics Data Analysis")
plt.show()
