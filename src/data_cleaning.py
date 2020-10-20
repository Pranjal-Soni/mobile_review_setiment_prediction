import config
import nltk
import pandas as pd
from nltk import stem
from nltk import tokenize
import texthero as hero 
from texthero import preprocessing

w_tokenizer = tokenize.WhitespaceTokenizer()
stemmer = stem.snowball.EnglishStemmer()
lemmatizer = stem.WordNetLemmatizer()


def lemmatization(text):
    '''
    input  : text 
    output :  lemmazitzed text
    '''
    return ' '.join([lemmatizer.lemmatize(word) for word in w_tokenizer.tokenize(text)])

def stemming(text):
    '''
    input  : text 
    output :  stemmed text
    '''
    return ' '.join([stemmer.stem(word) for word in w_tokenizer.tokenize(text)])


if __name__ == "__main__":


    #loading train, test, and dev data to train the model
    train = pd.read_csv(config.TRAIN,sep="\t", names=['label', 'text'],encoding="ISO-8859-1")
    test = pd.read_csv(config.TEST,sep="\t",names=['label', 'text'],encoding="ISO-8859-1")
    dev = pd.read_csv(config.DEV,sep="\t",names=['label', 'text'],encoding="ISO-8859-1")



    #combine train,test and dev data for data cleaning
    final_dataset = pd.concat([train,dev,test],axis=0)

    #create custom pipeline to clean the dataset
    custom_pipeline =[ preprocessing.fillna,
                    preprocessing.lowercase,
                    preprocessing.remove_whitespace,
                    preprocessing.remove_punctuation,
                    preprocessing.remove_stopwords,
                    preprocessing.remove_digits,
                    preprocessing.remove_urls
                    ]
    #copy dataset to df to clean it
    df = final_dataset.copy()

    #claen text data in the dataset
    df['text'] = hero.clean(df['text'], custom_pipeline)

    #lemmatize reviews
    df.text = df.text.apply(lemmatization)

    #save the cleaned dataset
    df.to_csv("../inputs/data.csv",index = False)