import matplotlib.pyplot as plt
from datetime import datetime
import pymongo
import datetime as dttime
import time

client = pymongo.MongoClient()

start_date = dttime.date(2022, 11, 4)
end_date = dttime.date(2022, 11, 14)

delta = dttime.timedelta(days=1)

db = client['tweeterdb']
collec = db['storeCount']

db2 = client['redditdb']
collec2 = db2['redditPolitics']

reddit_time = []
matchCount = []
count = 0

tweetDate = []
totCount = []


for tweetData in collec.find():
    totCount.append(tweetData['matched_tweets'])
    tweetDate.append(tweetData["timestamp"].split(",")[0][4:10])

tweetDate.sort()

print(totCount)
print(tweetDate)


while (start_date <= end_date):
    print("while start")
    
    count = 0
    for item in collec2.distinct('createdDate'):

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

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# Set position of bar on X axis
br1 = np.arange(len(totCount))
br2 = [x + barWidth for x in br1]


# Make the plot
plt.bar(br1, totCount, color ='grey', width = barWidth,
		edgecolor ='grey', label ='Twitter')
plt.bar(br2, matchCount, color ='black', width = barWidth,
		edgecolor ='grey', label ='Reddit Politics')


# Adding Xticks
plt.xlabel('Date', fontweight ='bold', fontsize = 15)
plt.ylabel('Count', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(totCount))],tweetDate)

plt.legend()
plt.show()
