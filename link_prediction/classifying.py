import numpy as np
import pandas as pd
from keras import callbacks
from keras.layers import Activation, Dense
from keras.models import Sequential
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

df = pd.read_csv('Data/graph_info_v2.csv')

names = df[['original', 'potential_friend']]
df.drop(['original', 'potential_friend'], axis=1, inplace=True)

# DROPPING COLUMNS BASED ON GNB/FILLNA/UNDIR (77.5% accuracy)
# df.drop('orig_outdegree', axis=1, inplace=True)  # ~4% increase
# df.drop('orig_indegree', axis=1, inplace=True)  # ~1% increase
# df.drop('orig_spl', axis=1, inplace=True)  # ~1% increase
# df.drop('friend_spl', axis=1, inplace=True)  # ~1% increase

# %%%%%

# DROPPING COLUMNS BASED ON KNN/FILLNA/UNDIR WHERE N=5, 77.6% accuracy
# df.drop('orig_outdegree', axis=1, inplace=True)  # ~3% increase
# df.drop('orig_degree', axis=1, inplace=True)  # ~2% increase
# df.drop('shortest_path_len', axis=1, inplace=True)  # ~2% increase
# # these two combine for a .5% increase
# df.drop('orig_spl', axis=1, inplace=True)
# df.drop('friend_outdegree', axis=1, inplace=True)

# N=9, drop orig_outdegree, orig_degree, and orig_transitivity for 77.9%

# N=13, drop orig_outdegree and spl for 77.8%

# N=15, drop none, 77.8%

# %%%%%

# SVM, rbf=77.2%, linear=77.8%, sigmoid=78.2%, sigmoid=78.5% after dropping orig_degree

# poly = 79.7% after drops:
# df.drop('orig_indegree', axis=1, inplace=True)
# df.drop('orig_degree', axis=1, inplace=True)
# df.drop('orig_outdegree', axis=1, inplace=True)
# df.drop('friend_indegree', axis=1, inplace=True)
# df.drop('friend_outdegree', axis=1, inplace=True)
# df.drop('friend_degree', axis=1, inplace=True)
# df.drop('orig_transitivity', axis=1, inplace=True)
# df.drop('friend_transitivity', axis=1, inplace=True)

# %%%%%

# RF, N=10 ~73% (with large 12% CI) after drops, n=100 has more tuning-space but CI makes this hard:
# df.drop('orig_degree', axis=1, inplace=True)
# df.drop('orig_spl', axis=1, inplace=True)
# df.drop('orig_outdegree', axis=1, inplace=True)
# df.drop('friend_indegree', axis=1, inplace=True)  # keep on n=100

undir_target = df.connected
in_target = df.in_connected
out_target = df.out_connected
df.drop(['connected', 'in_connected', 'out_connected'], axis=1, inplace=True)

# pd.set_option('display.max_columns', 500)
# print(df.head())

df.fillna(0, inplace=True)

gnb = GaussianNB()
gnb_scores = cross_val_score(gnb, df, undir_target, cv=10)
print("GNB Accuracy: %0.3f (+/- %0.3f)" % (gnb_scores.mean(), gnb_scores.std() * 2))

knn = KNeighborsClassifier(n_neighbors=15)
knn_scores = cross_val_score(knn, df, undir_target, cv=10)
print("KNN Accuracy: %0.3f (+/- %0.3f)" % (knn_scores.mean(), knn_scores.std() * 2))

svm = SVC(kernel='poly')
svm_scores = cross_val_score(svm, df, undir_target, cv=10)
print("SVM Accuracy: %0.3f (+/- %0.3f)" % (svm_scores.mean(), svm_scores.std() * 2))

rf = RandomForestClassifier(n_estimators=10)  # mess with n_estimators, default=10
rf_scores = cross_val_score(rf, df, undir_target, cv=10)
print("RF Accuracy: %0.3f (+/- %0.3f)" % (rf_scores.mean(), rf_scores.std() * 2))

# N-NET, mess with optimizers, nodes, layers, etc.
# n_input = len(df.columns)
# n_classes = 1
#
# model = Sequential([
#     Dense(32, input_shape=(n_input,)),
#     Activation('relu'),
#     Dense(n_classes),
#     Activation('softmax'),
# ])
#
# model.compile(optimizer='adam',
#               loss='binary_crossentropy',
#               metrics=['accuracy'],)
#
# kfold = StratifiedKFold(n_splits=10, shuffle=True)
# cvscores = []
# for train, test in kfold.split(df, undir_target):
#     model.fit(df.iloc[train], undir_target.iloc[train], epochs=10, batch_size=100)
#     print('hi')
#     scores = model.evaluate(df.iloc[test], undir_target.iloc[test], batch_size=100)
#     print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
#     cvscores.append(scores[1] * 100)
# print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))


for column in df.columns:
    df2 = df.drop(column, axis=1)
    print(column)

    # gnb_scores = cross_val_score(gnb, df2, undir_target, cv=10)
    # print("GNB Accuracy: %0.3f (+/- %0.3f)" % (gnb_scores.mean(), gnb_scores.std() * 2))

    # knn_scores = cross_val_score(knn, df2, undir_target, cv=10)
    # print("KNN Accuracy: %0.3f (+/- %0.3f)" % (knn_scores.mean(), knn_scores.std() * 2))

    # svm_scores = cross_val_score(svm, df2, undir_target, cv=10)
    # print("SVM Accuracy: %0.3f (+/- %0.3f)" % (svm_scores.mean(), svm_scores.std() * 2))

    # rf_scores = cross_val_score(rf, df2, undir_target, cv=10)
    # print("RF Accuracy: %0.3f (+/- %0.3f)" % (rf_scores.mean(), rf_scores.std() * 2))
