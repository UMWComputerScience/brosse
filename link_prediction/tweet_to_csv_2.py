import csv
import json
import sys

filename = sys.argv[1]
number = filename[-2:]

j_directory = '/data/Tweets/JSON/'
t_directory = '/data/Tweets/CSV/Tweets/'
u_directory = '/data/Tweets/CSV/Users/'
e_directory = '/data/Tweets/CSV/Edges/'

tweet_fields = ['TweetID', 'CreatedAt', 'UserID', 'Text', 'IsReply', 'IsRetweet', 'IsQuote']
user_fields = ['UserID', 'UserCreatedAt', 'ScreenName', 'Description', 'IsVerified', 'FriendsCount', 'FollowersCount',
               'ListedCount', 'StatusesCount', 'Lang']
edge_fields = ['TweetID', 'CreatedAt', 'User1', 'User2', 'Type']

tweet_csv = open((t_directory + 'tsplit' + number + '.csv'), 'w', encoding='utf-8', newline='')
user_csv = open((u_directory + 'usplit' + number + '.csv'), 'w', encoding='utf-8', newline='')
edge_csv = open((e_directory + 'esplit' + number + '.csv'), 'w', encoding='utf-8', newline='')
tweet_writer = csv.writer(tweet_csv)
user_writer = csv.writer(user_csv)
edge_writer = csv.writer(edge_csv)

if number == '00':
    tweet_writer.writerow(tweet_fields)
    user_writer.writerow(user_fields)
    edge_writer.writerow(edge_fields)


def tweet_to_lines(j):
    TweetID = j['id_str']
    CreatedAt = j['created_at']
    UserID = j['user']['id_str']
    Text = j['full_text']
    UserCreatedAt = j['user']['created_at']
    ScreenName = j['user']['screen_name']
    Description = j['user']['description']
    IsVerified = str(j['user']['verified'])
    FriendsCount = str(j['user']['friends_count'])
    FollowersCount = str(j['user']['followers_count'])
    ListedCount = str(j['user']['listed_count'])
    StatusesCount = str(j['user']['statuses_count'])
    Lang = j['user']['lang']

    IsReply = 'in_reply_to_status_id_str' in j
    IsRetweet = 'retweeted_status' in j
    IsQuote = 'quoted_status' in j

    banned_mentions = []
    if IsReply:
        User2 = j['in_reply_to_user_id_str']
        banned_mentions.append(User2)
        edge_values = [TweetID, CreatedAt, UserID, User2, 'Reply']
        edge_writer.writerow(edge_values)

    if IsRetweet:
        User2 = j['retweeted_status']['user']['id_str']
        banned_mentions.append(User2)
        edge_values = [TweetID, CreatedAt, UserID, User2, 'Retweet']
        edge_writer.writerow(edge_values)

    if IsQuote:
        User2 = j['quoted_status']['user']['id_str']
        banned_mentions.append(User2)
        edge_values = [TweetID, CreatedAt, UserID, User2, 'Quote']
        edge_writer.writerow(edge_values)

    if j['entities']['user_mentions']:
        for m in j['entities']['user_mentions']:
            if m['id_str'] not in banned_mentions:
                edge_values = [TweetID, CreatedAt, UserID, m['id_str'], 'Mention']
                edge_writer.writerow(edge_values)

    tweet_values = []
    for t in tweet_fields:
        tweet_values.append(eval(t))

    user_values = []
    for u in user_fields:
        user_values.append(eval(u))

    tweet_writer.writerow(tweet_values)
    user_writer.writerow(user_values)


infile = open(j_directory+filename)
for line in infile:
    if line[0] == '{' and line[-1] == '}':
        j = json.loads(line)
        tweet_to_lines(j)

infile.close()
tweet_csv.close()
user_csv.close()
edge_csv.close()
