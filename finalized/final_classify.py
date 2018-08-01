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


if __name__ == '__main__':
	warnings.simplefilter(action='ignore', category=FutureWarning)
	args = parse_args()
	cur_dir = os.getcwd()
	table_loc = cur_dir + '/' + args.data
	print(table_loc)
	df = read_table(table_loc)

	if args.train == True:
		if args.fasttext and args.linearSVM == False:
			print("You must select a ML model to use for training/classification")
			quit()
		print("training on {}".format(args.data))

	elif args.model.endswith('.bin'):
		print(args.fasttext)
		print(args.linearSVM)
		if args.fasttext and args.linearSVM == False:
			print("You must select a ML model to use for training/classification")
			quit()
		print("classifying {} using {}".format(args.data, args.model))
	else:
		print("Incorrect usage: specify a table to train or on or both model and a table to classify")
		quit()
