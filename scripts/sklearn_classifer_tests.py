import preprocess_table
import pandas as pd
from pandas import ExcelFile
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
import argparse
import warnings
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC




#determine the table, data split, which mode to run program in
def parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description='first classifier for SDG dataset')
    parser.add_argument('-t','--table', help="specify data table", required=True)
    parser.add_argument('-r','--random', help="test/train data is split randomly", action='store_true', required=False)
    parser.add_argument('-s', '--split', type=float, help="choose train/test data split ratio", required=False)
    parser.add_argument('-d', '--debug', action='store_true', help="eliminate training for faster debugging", required=False)
    args = parser.parse_args()
    return args

#try to open specified table
def check_args():
    """Accept or reject arguments"""
    path = os.getcwd()
    path = path + "/" +args.table
    print(path)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print("Could not find spreadsheet at %s" % args.table)
        quit()
    return df

if __name__ == "__main__":

    #prevents an error during chi2 test, probably not ideal
    warnings.simplefilter(action='ignore', category=FutureWarning)

    args = parse_args()
    df = check_args()
    df_copy = df.copy()

    #remove unneccesary characters from dataframe
    preprocess_table.preprocess(df,'linearSVC')

    if args.debug == True:
        print(df.columns.values)
        print(df.head(5))
        print(df.tail(5))

    if args.split:
        split = args.split
    else:
        split = 0.33

    if args.debug != True:

        #split data into training set, testing set
        #depending on whether you want random or reproducible results
        if args.random == True:
            train_set, test_set = train_test_split(df, test_size=split)
        else:
            train_set, test_set = train_test_split(df, test_size=split, random_state=42)

        train_set_copy = train_set.copy()
        test_set_copy = test_set.copy()

        #tfidf vectorizer finds word frequency between each corpus


        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', ngram_range=(1,2), stop_words='english', encoding='latin-1')
        features = tfidf.fit_transform(df.corpus)
        labels = df.sdg_codes


        N = 2
        desc_to_code = dict(df.values)
        #perform a chi2 test to find correlation between words and their most frequent sdg codes
        #not necessary, but useful to see
        for code, description in desc_to_code.items():
            whole_sdgs = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700]
            features_chi2 = chi2(features, labels == code)
            indices = np.argsort(features_chi2[0])
            feature_names = np.array(tfidf.get_feature_names())[indices]
            unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
            bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
            if code in whole_sdgs:
                print("# '{}':".format(code))
                print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
                print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))


    #could be phrased better
    if args.debug != True:

        #prepare model for prediction
        if args.random == True:
            X_train, X_test, y_train, y_test = train_test_split(df['corpus'], df['sdg_codes'])
        else:
            X_train, X_test, y_train, y_test = train_test_split(df['corpus'], df['sdg_codes'], random_state = 0)
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        #train model
        clf = MultinomialNB().fit(X_train_tfidf, y_train)
        #feed it a string for classification
        #TODO: same functionality but for an excel spreadsheet
        print(clf.predict(count_vect.transform(["poverty", "hunger", "good health", "education", "gender equality", "clean water sanitation", "affordable clean energy", "economic growth", "industry infrastructure", "inequalities", "sustainable cities communities", "responsible consumption production", "climate", "life water", "life land", "justice institutions", "goal partnerships"])))

        #list of models to plot performance of
        models = [
    
            LinearSVC(max_iter=2000)
        ]

        CV = 5
        cv_df = pd.DataFrame(index=range(CV * len(models)))
        entries = []

        for model in models:
          model_name = model.__class__.__name__
          accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)

          for fold_idx, accuracy in enumerate(accuracies):
            entries.append((model_name, fold_idx, accuracy))

        cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
        sns.boxplot(x='model_name', y='accuracy', data=cv_df)
        sns.stripplot(x='model_name', y='accuracy', data=cv_df,
                      size=8, jitter=True, edgecolor="gray", linewidth=2)


        #print average accuracy for each sklearn model
        cv_df.groupby('model_name').accuracy.mean()
        print(cv_df.groupby('model_name').accuracy.mean())

        plt.show()

        #most accurate model
        model = LinearSVC()
        X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=split, random_state=0)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        #need to figure this out.....
        bad_table = True
        print("You dont want to see this confusion matrix just yet.")
        if bad_table == False:
            sdg_strs=['100','200','300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600','1700']
            conf_mat = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots(figsize=(10,10))
            sns.heatmap(conf_mat, annot=True, fmt='d', xticklabels=10, yticklabels=10)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.show()
