import os
import subprocess

directory = "/data/Tweets/JSON"

for f in os.listdir(directory):
    cmd = "python3 /home/hcrosse/brosse/link_prediction/tweet_to_csv_2.py " + f
    subprocess.Popen(cmd, shell=True)

print('Processes started')
