import pandas as pd 
import config
import joblib

def sentiment_val(val):
    '''
    input : take a float value between [0,1]
    output : setiment corresponding the input
    '''
    if val==1:
        return('very negative')
    elif val==2:
        return('negative')
    elif val == 3:
        return('neutral')
    elif val == 4:
        return('positive')
    elif val == 5:
        return('very positive') 

if __name__ == "__main__":

    

    #list of different mobile reviews
    reviews = joblib.load(config.MOBILE_REVIEWS)

    #tf-idf vecotrizer
    tf_idf = joblib.load(config.TF_IDF)

    #svm classifier
    clf = joblib.load(config.SVM_MODEL)

    #list to store predicted sentiments
    reviews_sentiments =[]

    
    for i in range(len(reviews)):
        #convert each mobile review into tf_idf matrix
        matrix = tf_idf.transform(reviews[i].review)

        #predict sentiment
        reviews_sentiments.append(clf.predict(matrix))

    #save sentiment for each phone
    for i in range(len(reviews)):
        df = pd.concat([reviews[i],pd.Series(reviews_sentiments[i])],axis=1)
        df.columns=['review','sentiment']
        df.sentiment = df.sentiment.apply(sentiment_val)
        name = mobile_phones[i]+'_review_setiment.csv'
        df.to_csv(f"../review_sentiments/{name}",index = None)