import csv
import json
import winsound
from datetime import datetime
from os import listdir

"""
Converts jsonl formatted tweets to a csv
"""

# JSON
# created_at - UTC Time - "Wed Aug 27 13:08:45 +0000 2008"
# id_str - "1242154431"
# full_text - "blahblah"
# in_reply_to_status_id_str - "124124153135" or null - ????? FETCH?
# in_reply_to_user_id_str - "81895" or null
# in_reply_to_screen_name - "bob" or null
#
# user:
# 	id_str - "81059"
# 	screen_name - "ted"
# 	location - "Internet"
# 	url - "https://gjaga.com"
# 	description - "blaghasd gagdag gasdg gf"
# 	verified - true
# 	followers_counts - 5439
# 	friends_counts - 549
# 	listed_count - 429
# 	statuses_count - 53491
# 	created_at - "Wed Aug 27 13:08:45 +0000 2008"
# 	lang - "en"
#
# coordinates: (nullabled)
# 	coordinates - [-75.13531, 40.53151]
#
# quoted_status_id_str - "1353513" or null
# is_quote_status - false
#
# quoted_status: (nullable) - keep id, user id
# 	tweet object
#
# retweeted status: (nullable) - keep id, user id
# 	tweet object
#
# quote_count - 113
# reply_count - 143
# retweet_count - 5342
# favorite_count - 22
#
# entities:
# 	hashtags - [{"text"}]
# 	user_mentions - [{"screen_name", "id_str"}]
# 	urls - [{"expanded_url"}]
#
# lang - "en" or null

startTime = datetime.now()
path = "D:\Media\Twarc\Tweets\\"
csv_filename = "D:\Media\Twarc\Formatted\Tweets.csv"
fields = ['created_at', 'id_str', 'text', 'is_reply', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
          'in_reply_to_screen_name', 'is_quoted_status', 'quoted_status_id_str', 'quoted_user_id_str',
          'quoted_user_screen_name', 'is_retweeted_status', 'retweeted_status_id_str', 'retweeted_user_id_str',
          'retweeted_user_screen_name', 'retweet_count', 'favorite_count', 'lang', 'hashtags', 'mentioned_user_ids',
          'mentioned_screen_names', 'urls', 'lat', 'long', 'user_id_str', 'user_screen_name', 'user_location',
          'user_description', 'user_verified', 'user_friends_count', 'user_followers_count', 'user_listed_count',
          'user_statuses_count', 'user_created_at', 'user_lang']

csv_file = open(csv_filename, 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(fields)


def tweet_to_csv_line(j):
    created_at = j['created_at']
    id_str = j['id_str']
    text = j['full_text']
    is_reply = "False"
    in_reply_to_status_id_str = ""
    in_reply_to_user_id_str = ""
    in_reply_to_screen_name = ""
    is_quoted_status = "False"
    quoted_status_id_str = ""
    quoted_user_id_str = ""
    quoted_user_screen_name = ""
    is_retweeted_status = "False"
    retweeted_status_id_str = ""
    retweeted_user_id_str = ""
    retweeted_user_screen_name = ""
    retweet_count = str(j['retweet_count'])
    favorite_count = str(j['favorite_count'])
    lang = j['lang']
    hashtags = ""
    mentioned_user_ids = ""
    mentioned_screen_names = ""
    urls = ""
    lat = ""
    long = ""
    user_id_str = j['user']['id_str']
    user_screen_name = j['user']['screen_name']
    user_location = j['user']['location']
    user_description = j['user']['description']
    user_verified = str(j['user']['verified'])
    user_friends_count = str(j['user']['friends_count'])
    user_followers_count = str(j['user']['followers_count'])
    user_listed_count = str(j['user']['listed_count'])
    user_statuses_count = str(j['user']['statuses_count'])
    user_created_at = j['user']['created_at']
    user_lang = j['user']['lang']

    tags = []
    if j['entities']['hashtags']:
        for t in j['entities']['hashtags']:
            tags.append(t['text'])
        hashtags = ' '.join(tags)

    user_ids = []
    user_names = []
    if j['entities']['user_mentions']:
        for u in j['entities']['user_mentions']:
            user_ids.append(u['id_str'])
            user_names.append(u['screen_name'])
        mentioned_user_ids = ' '.join(user_ids)
        mentioned_screen_names = ' '.join(user_names)

    if j['coordinates']:
        lat = str(j['coordinates']['coordinates'][0])
        long = str(j['coordinates']['coordinates'][1])

    if j['in_reply_to_status_id_str']:
        is_reply = "True"
        in_reply_to_status_id_str = j['in_reply_to_status_id_str']
        in_reply_to_user_id_str = j['in_reply_to_user_id_str']
        in_reply_to_screen_name = j['in_reply_to_screen_name']

    if 'quoted_status' in j:
        is_quoted_status = "True"
        quoted_status_id_str = j['quoted_status_id_str']
        quoted_user_id_str = j['quoted_status']['user']['id_str']
        quoted_user_screen_name = j['quoted_status']['user']['screen_name']
        tweet_to_csv_line(j['quoted_status'])

    if 'retweeted_status' in j:
        is_retweeted_status = "True"
        retweeted_status_id_str = j['retweeted_status']['id_str']
        retweeted_user_id_str = j['retweeted_status']['user']['id_str']
        retweeted_user_screen_name = j['retweeted_status']['user']['screen_name']
        tweet_to_csv_line(j['retweeted_status'])

    values = []
    for i in fields:
        values.append(eval(i))

    csv_writer.writerow(values)


file_count = 0
line_count = 0
for f in listdir(path):
    infile = open(path+f)
    for line in infile:
        j = json.loads(line)
        tweet_to_csv_line(j)
        line_count += 1
    infile.close()
    file_count += 1
    print(file_count, ' files written in', datetime.now() - startTime)

csv_file.close()
print('Wrote', line_count, 'lines in', datetime.now() - startTime)

duration = 5000  # millisecond
freq = 440  # Hz
winsound.Beep(freq, duration)
