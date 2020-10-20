import config
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score


if __name__ == "__main__":

    #load the dataset
    df = pd.read_csv(config.DATA)

    #split data into train, test and dev
    train,dev,test = df.iloc[:8544],df.iloc[8544:9645],df.iloc[9645:]

    #drop Nan values
    train,test,dev = train.dropna(),test.dropna(),dev.dropna()

    #split datasets into X and y to train model
    train_X, train_y = train.text, train.label
    dev_X, dev_y = dev.text, dev.label
    test_X, test_y = test.text, test.label

    #convert text data into tfidf matrix
    tf_idf = TfidfVectorizer()

    #fit training to tf_idf
    tf_idf.fit(train_X)

    #transform train,test and dev data
    train_X = tf_idf.transform(train_X)
    dev_X = tf_idf.transform(dev_X)
    test_X = tf_idf.transform(test_X)

    #fit Support Vector classifier
    clf = svm.SVC()
    clf.fit(train_X,train_y)

    #predict the score for dev and test data
    pred_dev = clf.predict(dev_X)
    print(f"Accurcy score for Validation data : {accuracy_score(dev_y,pred_dev)}")
    pred_test = clf.predict(test_X)
    print(f"Accurcy score for Test data : {accuracy_score(test_y,pred_test)}")

    #save tf_idf vectorizer
    joblib.dump(tf_idf,"../inputs/tf_idf.pkl")

    #save the model
    joblib.dump(clf, '../models/svm_model.pkl')