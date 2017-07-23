# Twitter Mentors

This is a small script that crawls replies to [@sehurlburt](https://twitter.com/sehurlburt)'s tweet about mentorship and indexes the mentors.

## Running Yourself
You need to have [Python Twitter Tools](https://github.com/sixohsix/twitter/tree/master) and Python YAML package installed. 

If these are present, just create a config file `twitter-config.yml` in same folder as `twitter-mentors.py` with following format:

````yaml
consumer_key: xxxx
consumer_secret: xxxx
access_token: 1234-xxxx
access_token_secret: xxxx
````

Now, just run the `twitter-mentors.py` file. 