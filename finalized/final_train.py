import os
import fasttext as ft 
import pandas as pd
import argparse
import warnings

def parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description="Train/Test a model")
    parser.add_argument('-d','--data',help="specify data table", type=str, required=True)
    parser.add_argument('-f', '--fasttext', help="use fasttext to train/classify", required=False, action='store_true', default=False)
    parser.add_argument('-l', '--linearSVM', help="use linearSVM to train/classify", required=False, action='store_true', default=False)
    parser.add_argument('-s', '--split', type =float, help="choose train/test data split ratio", default=0.2, required=False)
    args = parser.parse_args()
    return args

def read_table(table):
	if table.lower().endswith('.csv'):
		table_df = pd.read_csv(table)
	elif table.lower().endswith('.xlsx'):
		table_df = pd.read_excel(table)
	else:
		print("Table must be csv for xlsx format")
		quit()
	return table_df

def preprocess_table(df, algorithm):
	stop_words = set()
	stop_words = stop_words.words('english')
	if algorithm == "linearSVM":



if __name__ == '__main__':
	warnings.simplefilter(action='ignore', category=FutureWarning)
	args = parse_args()
	if args.fasttext == False and args.linearSVM == False:
		print("Incorrect usage: you must specify a ML algorithm")
		quit()
	cur_dir = os.getcwd()
	table_loc = cur_dir + '/' + args.data
	df = read_table(table_loc)

	print(df)

	#for fasttext this is a txt file, for linearSVM this is a df
	if args.fasttext == True:
		final_data = preprocess_table(df, 'fasttext')
	elif args.linearSVM == True:
		final_data = preprocess_table(df, 'linearSVM')
	
	






	

