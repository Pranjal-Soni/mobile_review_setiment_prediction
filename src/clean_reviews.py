import joblib
import pandas as pd
import numpy as np
import texthero as hero
from texthero import preprocessing
from nltk import stem
from nltk import tokenize


w_tokenizer = tokenize.WhitespaceTokenizer()
lemmatizer = stem.WordNetLemmatizer()


def lemmatization(text):
    '''
    input  : text 
    output :  lemmazitzed text
    '''
    return ' '.join([lemmatizer.lemmatize(word) for word in w_tokenizer.tokenize(text)])


if __name__ == "__main__":

    mobile_phones = ['redmi note 9',
                 'oneplus 7t pro',
                 'nokia 5.3',
                 'Samsung Galaxy M21',
                 'Apple iPhone 11',
                 'Vivo Y20',
                 'Redmi 8A',
                 'OPPO A5',
                 'OnePlus 8',
                 'Samsung S10'
                 ]
    
    #store the mobile phone reviews in the list reviews
    reviews = []
    for i in range(len(mobile_phones)):
        reviews.append(pd.read_csv(f"../reviews/{mobile_phones[i]}_review.csv"))
    
    #custom pipeline to clean the data
    custom_pipeline = [preprocessing.fillna,
                   preprocessing.lowercase,
                   preprocessing.remove_whitespace,
                   preprocessing.remove_angle_brackets,
                   preprocessing.remove_html_tags,
                   preprocessing.remove_digits,
                   preprocessing.remove_stopwords,
                   preprocessing.remove_diacritics,
                   preprocessing.remove_round_brackets,
                   preprocessing.remove_square_brackets,
                   preprocessing.remove_curly_brackets,
                   preprocessing.remove_punctuation]
    
    #clean each phone review in reviews
    for r in reviews:
        r.review = hero.clean(r.review,custom_pipeline)
    
    #lemmatize reviews:
    for r in reviews:
        r.review = r.review.apply(lemmatization)
    #save clean reviews
    joblib.dump(reviews,'../inputs/mobile_reviews.pkl')