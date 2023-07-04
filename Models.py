#Model training code for Google Colaboratory

from google.colab import drive
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
import numpy as np


drive.mount('/content/drive')
os.chdir('drive/MyDrive/Capstone Project Files')

df3 = pd.read_csv("Extracted Lyrics-English Only-Bad Characters Removed.csv")

Tfidf = TfidfVectorizer(min_df=10, max_df=.7, ngram_range=(3, 4), stop_words='english')

lyrics_pipe = Pipeline([
    ('Encoder', Tfidf),
    ('SVD', TruncatedSVD(n_components=100))
])


features = lyrics_pipe.fit_transform(df3['Lyrics'])

np.save('Features-v019-Tfidf-min_df-10-min_df-70pct-ngram_range-34-stop_words-Eng-TruncatedSVD-nComponents-100.npy', features)

nn = NearestNeighbors(n_neighbors=51).fit(features)

dists, indices = nn.kneighbors(features)

matrix = pd.DataFrame(indices)

#Table below exported to PosgreSQL public.similar_songs table and accessed in App.py and Database.py:

matrix.to_csv('Predicted Neighbors-NN50-v019-Tfidf-min_df-10-min_df-70pct-ngram_range-34-stop_words-Eng-TruncatedSVD-nComponents-100.csv', header=False, index_label='Row_Index')
