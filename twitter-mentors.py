from twitter import *
import io, json, string, yaml

with open("twitter-config.yml", "r") as configfile:
	config = yaml.load(configfile)

t = Twitter(
	auth=OAuth(config['access_token'], config['access_token_secret'], config['consumer_key'], config['consumer_secret']))

# since quotes are normal tweets with Tweet URL at end, searching API for the tweet link
result = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=100)

# result is a dictionary with 'serach_metadata' and 'statuses' keys
tweets = {}

# a bit of markdown for README page in /docs
output = "These results are from a basic Twitter search. Lot of enhancements possible. If you notice something wrong or want to be removed, open a GitHub issue or tweet me at [@real_ishan](https://twitter.com/real_ishan)"

output += "\n\n|User|Tweet|"
output += "\n" + "|----|----|"

if result['statuses']:
	for x in xrange(0,len(result['statuses'])):
		# Two things being filtered here:
		#  - Retweets aren't from mentors (RT at beginning)
		#  - Most of the tweets less than ~45 characters aren't about mentorship
		if (result['statuses'][x]['text'].find('RT ') == -1) and (len(result['statuses'][x]['text']) > 45) :
			tweets[result['statuses'][x]['id']] = {
					'text'	: result['statuses'][x]['text'],
					'user'	: {
						'id'			: result['statuses'][x]['user']['id'],
						'name'			: result['statuses'][x]['user']['name'],
						'profile'		: 'https://twitter.com/' + result['statuses'][x]['user']['screen_name'],
						'description'	: result['statuses'][x]['user']['description']
					}
				}
			output += "\n" + "[" + tweets[result['statuses'][x]['id']]['user']['name'] + "](" +  tweets[result['statuses'][x]['id']]['user']['profile'] + ")" + "|" + string.replace(tweets[result['statuses'][x]['id']]['text'], '|', '\|') + "|"

with io.open("docs/README.md", "w", encoding="utf-8") as outfile:
	outfile.write(unicode(output))