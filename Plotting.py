from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import re

sw = list(pd.read_csv('Stopwords-English.csv', header=None)[0])

def word_cloud(txt):
    
    txt = re.sub(r'\[.+?\]', "", txt)
    
    pattern = r'\b(\w)\1+\w?\b'
    
    txt = re.sub(pattern, '', txt)
    
    cv = CountVectorizer(max_features=500, stop_words=sw)
    
    features = cv.fit_transform([txt])
    
    feature_names = cv.get_feature_names_out()

    dense = features.todense().tolist()
    
    words = pd.DataFrame(dense, columns=feature_names).transpose()
    
    wordcloud = WordCloud(min_font_size=1, background_color="white", scale=10, prefer_horizontal=.65, width=400, height=400, max_words=500).generate_from_frequencies(words[0])
    
    wordcloud.recolor(color_func=lambda *args, **kwargs: 'black')
    
    return wordcloud