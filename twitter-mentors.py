from twitter import *
import yaml

with open("twitter-config.yml", "r") as configfile:
	config = yaml.load(configfile)

# t = Twitter(
# 	auth=OAuth())
# t.statuses.user_timeline(screen_name="sehurlburt")

print(config)