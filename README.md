Analysis of FIFA 2022 WC based on Daily Tweets, Subreddit Comments and 4chan Boards by extracting data using API calls and storing in MongoDB every day during the tournament to determine racial-abuses,critisism,hateful comments on Players, Teams as well as predict the popularity of Player and Teams as the tournament progresses.

## Tech-stack

* `python` - The project is developed and tested using python v3.9.12. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `MongoDB`- This project uses MongoDB for saving collected data. 
    * [MongoDB Website](https://www.mongodb.com/)
* `Spyder` - IDE used to execute python code [Spyder IDE website](https://www.spyder-ide.org/)

*`Libraries`- Numpy, pandas, etc.*

## Three data-source documentation

* `Twitter`
  * [Sample Stream API](https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/quick-start/sampled-stream) - <Twitter API provides one feature among its various features for its developers which is called Sample Stream. Sample stream basically provides the developers approximately 1 percent sample of tweets in real time.>
* `Reddit` - We are using `r/sports`, `r/FIFA`, `r/WorldcupQatar2022` 
  * [r/sports](https://reddit.com/r/sports) - <A subreddit which has posts, discussions, predictions about different types of sports>
  * [r/FIFA](https://reddit.com/r/FIFA) - <A subreddit which has posts, discussions, comments about FIFA related content>
  * [r/WorldcupQatar2022](https://reddit.com/r/WorldcupQatar2022) - <A subreddit which has posts, discussions, comments about FIFA World Cup happening in Qatar>
* `4chan` 
 *[4chan] (https://4chan.org) <It is an imageboard website which consits of numerous topics with anonymous users that can comment anything within the guidelines of the websites including a variety of hateful comments and slurs on different issues and topics. >
  * [/sp](https://a.4cdn.org/sp/catalog.json) - <This board contains discussions on all the sports. >
