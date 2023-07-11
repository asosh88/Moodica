from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import re

sw = list(pd.read_csv('Stopwords-English.csv', header=None)[0])

def black_color(word, font_size, position, orientation, random_state=None, **kwargs):
    
    return("hsl(0,100%, 1%)")


def word_cloud(txt):
    
    txt = re.sub(r'\[.+?\]', '', txt)
    
    cv = CountVectorizer(max_features=500, stop_words=sw)
    
    features = cv.fit_transform([txt])
    
    feature_names = cv.get_feature_names_out()

    dense = features.todense().tolist()
    
    words = pd.DataFrame(dense, columns=feature_names).transpose()
    
    #words = words.sum(axis=1)
    
    wordcloud = WordCloud(background_color="white", width=450, height=300).generate_from_frequencies(words[0])
    
    wordcloud.recolor(color_func = black_color)
    
    return wordcloud