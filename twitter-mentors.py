from twitter import *
import io, json, re, string, yaml

# read configuration file. For format, see README
with open("twitter-config.yml", "r") as configfile:
	config = yaml.load(configfile)


def escape_text_for_table(text):
	# first, escape the pipe charactesr. They conflict with table pipes on GH pages
	text = string.replace(text, '|', '\|')

	# remove new lines from the text. They cause new row to appear in GH pages table
	text = string.replace(text, '\n', ' ')

	return text

# helper function of make_twitter_link_clickable
def markdown_link(match):
	groups = match.groups() or ''
	link = groups[0]
	
	return '[{0}]({0})'.format(link)

# the tweets are not in search results. At the end, there is a link. Make link clickable
# so visitors can go to the specific tweet to reply or 
def make_twitter_link_clickable(text):
	# The link to tweet is at end of text
	replaced = re.sub('(https\://t.co/.*)', markdown_link, text)
	return replaced

t = Twitter(
	auth=OAuth(config['access_token'], config['access_token_secret'], config['consumer_key'], config['consumer_secret']))

# since quotes are normal tweets with Tweet URL at end, searching API for the tweet link
result = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=100)

# result is a dictionary with 'serach_metadata' and 'statuses' keys
tweets = {}

# a bit of markdown for README page in /docs
output = "This page contains a list of people (along with their tweets) who are willing to help/mentor other programmers. I am working on a searchable index. For now, just do a Ctrl/Cmd + F and see if you can find the tech you want help with."
output += "\n\nIf you notice something wrong or want to be removed, open a GitHub issue or tweet me at [@real_ishan](https://twitter.com/real_ishan)"
output += "\n\nThanks to [Stephanie Hurlburt](https://twitter.com/sehurlburt/) who [asked people to help](https://twitter.com/sehurlburt/status/889004724669661184)!\n\n----"

output += "\n\n|User|Profile Description|Tweet|"
output += "\n" + "|----|----|----|"

if result['statuses']:
	while True:
		# process results and output
		for x in xrange(0,len(result['statuses'])):
			# Two things being filtered here:
			#  - Retweets aren't from mentors (RT at beginning)
			#  - Most of the tweets less than ~45 characters aren't about mentorship
			if (result['statuses'][x]['text'].find('RT ') == -1) and (len(result['statuses'][x]['text']) > 45) :
				tweets[result['statuses'][x]['id']] = {
						'text'	: result['statuses'][x]['text'].encode('utf-8'),
						'user'	: {
							'id'			: result['statuses'][x]['user']['id'],
							'name'			: result['statuses'][x]['user']['name'].encode('utf-8'),
							'profile'		: 'https://twitter.com/' + result['statuses'][x]['user']['screen_name'].encode('utf-8'),
							'description'	: result['statuses'][x]['user']['description'].encode('utf-8')
						}
					}

				# add username + profile link
				output += "\n" + "[" + tweets[result['statuses'][x]['id']]['user']['name'] + "](" +  tweets[result['statuses'][x]['id']]['user']['profile'] + ")" + "|"

				# add the description
				output += escape_text_for_table(tweets[result['statuses'][x]['id']]['user']['description']) + "|"

				# add tweet
				output += make_twitter_link_clickable(escape_text_for_table(tweets[result['statuses'][x]['id']]['text'])) + "|"

		# no more crawling if results were less than 100 in last call
		if len(result['statuses']) < 100:
			break
		else:
			# take the ID of last tweet we had, get everything until that one
			last_tweet_id = min(tweets.keys())
			result = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=100, max_id=last_tweet_id)


with io.open("docs/_includes/twitter_table.md", "w", encoding="utf-8") as outfile:
	outfile.write(unicode(output.decode('utf-8')))