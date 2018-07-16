import preprocess_table
import pandas as pd
import numpy as np
import seaborn as sns
import os
import subprocess
import matplotlib.pyplot as plt
import argparse
import warnings
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.feature_selection import chi2
from sklearn.svm import LinearSVC



class ML_Model:
    def __init__(self, model_type, case, table, split = 0.33):
        self.type = model_type
        self.case = case
        self.split = split
        self.table = table
        self.path = str(os.getcwd() + "/" + table)
        self.df = None

    def __str__(self):
        ret = "Model type: {} - Learning case: {} - Test/Train split: {}\n".format(self.type, self.case,self.split)
        ret += "{}\n".format(self.df.columns.values)
        return ret

    def create_df(self, path):
        try:
            self.df = pd.read_excel(path)
            print("df created.")
            print("path: %s" % path)
            print("features: {}\n".format(self.df.columns.values))
        except FileNotFoundError:
            print("Could not find table at %s" % path)
            quit()


def parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description="Linear SVC model for SDG classification")
    parser.add_argument('-t','--table',help="run model on specified table", required=False)
    parser.add_argument('-s', '--split', type =float, help="choose train/test data split ratio", default=0.33, required=False)
    parser.add_argument('-d','--debug', help="run script in debug mode. tests all tables", action="store_true", required=False)
    args = parser.parse_args()
    return args

def make_model_list():
    model_list = []
    #case1_model = ML_Model(model_selection, 1, "Final_SDG_dataset_case_1.xlsx", args.split)
    #case1_model.create_df(case1_model.path)
    #case2_model = ML_Model(model_selection, 2, "Final_SDG_dataset_case_2.xlsx", args.split)
    #case2_model.create_df(case2_model.path)
    #case3_model = ML_Model(model_selection, 3, "Final_SDG_dataset_case_3.xlsx", args.split)
    #case3_model.create_df(case3_model.path)
    #case4_model = ML_Model(model_selection, 4, "Final_SDG_dataset_case_4.xlsx", args.split)
    #case4_model.create_df(case4_model.path)
    updated_dataset = ML_Model(model_selection, 5, "sdg_master_unique_cleaned.xlsx", args.split)
    updated_dataset.create_df(updated_dataset.path)
    truncated_dataset = ML_Model(model_selection, 5, "truncated_codes.xlsx", args.split)
    truncated_dataset.create_df(truncated_dataset.path)

    #model_list.append(case1_model)
    #model_list.append(case2_model)
    #model_list.append(case3_model)
    #model_list.append(case4_model)
    model_list.append(updated_dataset)
    model_list.append(truncated_dataset)
    return model_list

#def fast_text(dataset):


if __name__ == "__main__":

    args = parse_args()

    #choose model to apply
    print("Select a model")
    print("   -LinearSVC: 1")
    print("   -fastText: 2")
    model_selection = input()
    if model_selection == '1':
        model_selection = 'LinearSVC'
    elif model_selection == '2':
        model_selection = 'fastText'
    else:
        print("unacceptable selection")
        quit()

    #test all tables in /data
    if args.debug:
        model_list = make_model_list()
    #test single table
    elif args.table:
        model_list = []
        model_args = ML_Model(model_selection, args.table, args.split)
        model_list.append(model_args)
        df = model_args.create_df(model_args.path)
    else:
        print("please specify a dataset. run with -h to see arguments")
        quit()




    if model_selection == "LinearSVC":
        for model in model_list:
            preprocess_table.preprocess(model.df, model_selection)
            print(model.df['sdg_codes'].unique())
            split = model.split
            train_set, test_set = train_test_split(model.df, test_size=split)
            tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', ngram_range=(1,2), stop_words='english', encoding='latin-1')
            features = tfidf.fit_transform(model.df.corpus)
            labels = model.df.sdg_codes

            desc_to_code = dict(model.df.values)

            X_train, X_test, y_train, y_test = train_test_split(model.df['corpus'], model.df['sdg_codes'])
            count_vect = CountVectorizer()
            X_train_counts = count_vect.fit_transform(X_train)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

            clf = MultinomialNB().fit(X_train_tfidf, y_train)
            print(clf.predict(count_vect.transform(["sadly those qualities are not hallmarks of this guy queen cheese water infrastructure housing crisis poor people etc"])))
            print(clf.predict(count_vect.transform([" water quality pollution"])))

            model_to_use = LinearSVC()
            model_name = model_to_use.__class__.__name__
            CV = 5
            entries = []
            accuracies = cross_val_score(model_to_use, features, labels, scoring='accuracy', cv=CV)
            for fold_idx, accuracy in enumerate(accuracies):
                entries.append((model_name, fold_idx, accuracy))
            cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
            X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, model.df.index, test_size=0.33, random_state=0)
            model_to_use.fit(X_train, y_train)
            y_pred = model_to_use.predict_proba(X_test)
            y_pred = model_to_use.predict(X_test)
            model_to_use.predict(["water quality pollution"].reshape(1, -1))
            from sklearn.metrics import confusion_matrix
            conf_mat = confusion_matrix(y_test, y_pred)
            #print average accuracy for each sklearn model
            cv_df.groupby('model_name').accuracy.mean()
            print(cv_df.groupby('model_name').accuracy.mean())
            warnings.filterwarnings('always')
            from sklearn import metrics
            print(metrics.classification_report(y_test, y_pred, labels=np.unique(y_pred)))


    elif model_selection == "fastText":
        for model in model_list:
            preprocess_table.preprocess(model.df, model_selection)
            #subprocess.call(['ls','-la'])
            split = model.split
            train_set, test_set = train_test_split(model.df, test_size=split)
            train_set_fp = os.getcwd() + "/data/truncated_train.csv"
            valid_set_fp = os.getcwd() + "/data/truncated_valid.csv"
            train_set.to_csv(path_or_buf=train_set_fp, index=False, header=False)
            test_set.to_csv(path_or_buf=valid_set_fp, index=False, header=False)
