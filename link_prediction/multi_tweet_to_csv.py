import os
import subprocess

directory = "/data/Tweets/JSON"

for f in os.listdir(directory):
    subprocess.run("python3 tweet_to_csv_2.py " + f + " &")

print('Processes started')
