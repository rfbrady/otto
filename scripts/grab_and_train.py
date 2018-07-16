import argparse
import os
import csv
import sqlite3
import pandas as pd
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
from sklearn.model_selection import train_test_split
from fastText import train_supervised

def print_results(N, p, r):
	print("N\t" + str(N))
	print("P@{}\t{:.3f}".format(1, p))
	print("R@{}\t{:.3f}".format(1, r))

def parse_args():
	parser = argparse.ArgumentParser(description='Pull data from sqlite DB and train a FastText model on it')
	parser.add_argument('-d', '--database', help='Specify sqlite DB', required=False, default='testdb.sqlite')
	parser.add_argument('-s', '--split', help='Choose test/train split, default is .2', required=False, default=.2, type=float)
	args = parser.parse_args()
	return args

def token_filter(sentence, stop_words, remove_nonalphanum):
	"""Tokenize, remove unneccesary characters, untokenize"""
	words = word_tokenize(sentence)
	#this table doesnt have any critical numbers, so we can remove all of them
	if remove_nonalphanum == True:
	    words = [word for word in words if word.isalnum()]
	words = [word for word in words if word not in stop_words]
	words = [word.lower() for word in words]

	res = " ".join(words)
	return res



def print_prediction(prediction):
	for i in range(5):
		print("{} with probability {}".format(prediction[0][i].replace('__label__',''), str(round(prediction[1][i], 3))))

if __name__ == '__main__':
	args = parse_args()
	database = os.getcwd() + '/' + args.database

	conn = sqlite3.connect(database)
	cur = conn.cursor()
	with open('data.csv', 'w') as f:
		writer = csv.writer(f)
		for row in cur.execute('SELECT * FROM {}'.format('sdg')):
			writer.writerow(row)
	conn.close()

	df = pd.read_csv('data.csv')

	stop_words = set()
	stop_words = stopwords.words('english')

	#remove rowid
	df.drop(df.columns[0], axis=1, inplace=True)
	df.columns = ['title', 'short_description', 'long_description', 'sdg_codes']
	cols = df.columns.tolist()




	cols = cols[-1:] + cols[:-1]
	for row in df.index:
		#combine elements into one column, corpus
		df.at[row, 'corpus'] = str(df.at[row, 'title']) + ' ' + str(df.at[row, 'short_description']) + ' ' + str(df.at[row, 'long_description'])
		sentence = df.at[row, 'corpus']
		df.at[row, 'sdg_codes'] = str(df.at[row, 'sdg_codes']) 
		res = token_filter(sentence, stop_words, True)
		#set corpus equal to the new token filtered string
		df.at[row, 'corpus'] = res


	for title in df.columns:
		if title != 'sdg_codes' and title != 'corpus':
			df.drop(title, inplace=True, axis=1)
	for row in df.index:
		df.at[row, 'sdg_codes'] = "__label__" + df.at[row, 'sdg_codes'] + " "
		df.at[row, 'sdg_codes'] = df.at[row, 'sdg_codes'] + df.at[row, 'corpus']

	df.drop('corpus', inplace=True, axis=1)

	train_set, test_set = train_test_split(df, test_size=args.split)

	train_set.to_csv(path_or_buf='train.csv', index=False, header=False)
	test_set.to_csv(path_or_buf='test.csv', index=False, header=False)

	text_list = []
	with open('train.csv', 'r') as csv_file:
		for line in csv_file.readlines():
			text_list.append(line)

	with open('sdg.train', 'w') as txt_file:
		for line in text_list:
			txt_file.write(line)

	text_list = []
	with open('test.csv', 'r') as csv_file:
		for line in csv_file.readlines():
			text_list.append(line)

	with open('sdg.test', 'w') as txt_file:
		for line in text_list:
			txt_file.write(line)

	train_data = os.getcwd() + '/sdg.train'
	test_data = os.getcwd() + '/sdg.test'

	epoch_list = [500]
	lr_list = [.4]

	for epoch in epoch_list:
		for lr in lr_list:
			model = train_supervised(
				input=train_data, epoch=epoch, lr=lr, wordNgrams=2, verbose=2, minCount=1, bucket=500000
			)
			print("epoch: {} lr: {}".format(epoch, lr))
			print_results(*model.test(test_data))

			p1 = str(round(model.test(test_data)[1], 3))
			r1 = str(round(model.test(test_data)[2], 3))

			p2 = str(round(model.test(test_data, 2)[1], 3))
			r2 = str(round(model.test(test_data, 2)[1], 3))

			p3 = str(round(model.test(test_data, 3)[1], 3))
			r3 = str(round(model.test(test_data, 3)[1], 3))

			print("{}{}".format(p1, r1))
			print("{}{}".format(p2, r2))
			print("{}{}".format(p3, r3))

			model.save_model('sdg_model')
			model.save_model('../flask_app1/sdg_model')





