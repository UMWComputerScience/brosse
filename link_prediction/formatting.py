import pandas as pd

tweets = pd.read_csv("Data/tweets.csv", encoding="ISO-8859-1")

dates = []
ids = []
creators = []
mentionees = []
for index, tweet in tweets.iterrows():
    if '@' in tweet.text:
        words = tweet.text.split(' ')
        for word in words:
            if word[0] is '@':
                dates.append(tweet.created_at)
                ids.append(index)
                creators.append(tweet.user_screen_name)
                mentionees.append(word)

df = pd.DataFrame({'created_at': dates, 'id': ids, 'creator': creators, 'mentioned': mentionees})
df['created_at'] = pd.to_datetime(df.created_at)
june = df[df.created_at < pd.to_datetime('Mon Jul 02 22:33:15 +0000 2018')]
july = df[~df.isin(june)].dropna()

print(len(june), len(july), (len(june) + len(july)), len(df))

df.to_csv("Data/mentions.csv", index=False)
june.to_csv("Data/june_mentions.csv")
july.to_csv("Data/july_mentions.csv")
