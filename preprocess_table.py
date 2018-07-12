import pandas
import os
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.api import TokenizerI
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer



def token_filter(sentence, stop_words, remove_nonalpha):
    """Tokenize, remove unneccesary characters, untokenize"""
    words = word_tokenize(sentence)
    #this table doesnt have any critical numbers, so we can remove all of them
    if remove_nonalpha == True:
        words = [word for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    words = [word.lower() for word in words]

    res = " ".join(words)
    return res

def preprocess(df, model_type):
    """Rearrange and concatenate dataframe into new dataframe"""
    #combine feature vectors into single column


    stop_words = set()
    stop_words = stopwords.words('english')
    columns = list(df)

    print("Spreadsheet contains %d features" % (len(columns) - 1))
    print(columns)
    #case 1 - title, short, long, code
    if (len(columns) - 1) == 3:
        remove_nonalpha = True
        for row in df.index:
            #combine elements into one column, corpus
            df.at[row, 'corpus'] = str(df.at[row, 'title']) + ' ' + str(df.at[row, 'short_description']) + ' ' + str(df.at[row, 'long_description'])
            sentence = df.at[row, 'corpus']
            df.at[row, 'sdg_codes'] = str(df.at[row, 'sdg_codes']) 
            res = token_filter(sentence, stop_words, remove_nonalpha)
            #set corpus equal to the new token filtered string
            df.at[row, 'corpus'] = res

    #case 2 - title, short, long, year, donor, recipient, code
    elif (len(columns) - 1) == 6:
        remove_nonalpha = False
        for row in df.index:
            df.at[row, 'corpus'] = str(df.at[row, 'title'] + ' ' + df.at[row, 'short_description'] + ' '
                                    + df.at[row, 'long_description'] + ' ' + str(df.at[row, 'year']) + ' '
                                    + df.at[row, 'donor'] + ' ' + df.at[row, 'recipient'])
            sentence = df.at[row, 'corpus']


            res = token_filter(sentence, stop_words, remove_nonalpha)
            df.at[row, 'corpus'] = res

    #case 3 - title, short, long, sector code, purpose code, code
    elif (len(columns) - 1) == 5:
        remove_nonalpha = False
        for row in df.index:
            df.at[row, 'corpus'] = str(df.at[row, 'title'] + ' ' + df.at[row, 'short_description'] + ' '
                                    + df.at[row, 'long_description'] + ' ' + str(df.at[row, 'crn_sector_code']) + ' '
                                    + str(df.at[row, 'crn_purpose_code']))

            sentence = df.at[row, 'corpus']
            res = token_filter(sentence, stop_words, remove_nonalpha)
            df.at[row, 'corpus'] = res

    #case 4 - all possible features
    elif (len(columns) - 1) == 8:
        remove_nonalpha = False
        for row in df.index:
            df.at[row, 'corpus'] = str(df.at[row, 'title'] + ' ' + df.at[row, 'short_description'] + ' '
                                    + df.at[row, 'long_description'] + ' ' + str(df.at[row, 'year']) + ' '
                                    + df.at[row, 'donor'] + ' ' + df.at[row, 'recipient'] + ' '
                                    + str(df.at[row, 'crn_sector_code']) + ' ' + str(df.at[row, 'crn_purpose_code']))
            sentence = df.at[row, 'corpus']
            res = token_filter(sentence, stop_words, remove_nonalpha)
            df.at[row, 'corpus'] = res

    #remove all columns that are no longer needed
    #this leaves sdg_codes and corpus
    for title in columns:
        if title != 'sdg_codes' and title != 'corpus':
            print('removing column: %s' % title)
            df.drop(title, inplace=True, axis=1)

    #need to add __label__ to class column for fasttext
    if model_type == "fastText":
        
        cols = df.columns.tolist()
        #rearrange columns 
        cols = cols[-1:] + cols[:-1]
        for row in df.index:
            df.at[row, 'sdg_codes'] = "__label__" + df.at[row, 'sdg_codes'] + " "
            df.at[row, 'sdg_codes'] = df.at[row, 'sdg_codes'] + df.at[row, 'corpus']
            
        df.drop('corpus', inplace=True, axis=1)
        print(df.columns.values)
        fp = os.getcwd() + "/data/" + "truncated.csv"
        print(fp)
        df.to_csv(path_or_buf=fp, index=False, header=False)



