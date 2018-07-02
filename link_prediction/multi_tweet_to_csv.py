import os

directory = "/data/Tweets/JSON"

for f in os.listdir(directory):
    print("nohup python3 tweet_to_csv_2.py " + f + " &")

print('Processes started')
