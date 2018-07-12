import sqlite3
import pandas as pd
import preprocess_table
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.api import TokenizerI
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer


if __name__ == '__main__':

	datafile = 'data/sdg_master_unique_cleaned.xlsx'
	df = pd.read_excel(datafile)
	stop_words = set()
	stop_words = stopwords.words('english')
	remove_nonalpha = True

	sqlite_file = 'data/testdb.sqlite'
	table_name = 'sdg'
	primary_key = 'rowid'
	columns = ['title', 'short', 'long', 'sdg_code']

	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	c.execute("CREATE TABLE {} ({} {} )".format(table_name, primary_key, 'INTEGER'))
	for col in columns:
		c.execute("ALTER TABLE {} ADD COLUMN '{}' {}".format(table_name, col, 'TEXT'))
	
	i = 0
	for row in df.index:
		title_text = str(df.at[row,'title'])
		title_text = preprocess_table.token_filter(title_text, stop_words, remove_nonalpha)
		short_d = str(df.at[row,'short_description'])
		short_d = preprocess_table.token_filter(short_d, stop_words, remove_nonalpha)
		long_d = str(df.at[row,'long_description'])
		long_d = preprocess_table.token_filter(long_d, stop_words, remove_nonalpha)
		code = str(df.at[row,'sdg_codes'])

		c.execute("INSERT INTO {} ({}, {}, {}, {}, {}) VALUES ({}, '{}', '{}', '{}', '{}')"
			.format(table_name, primary_key, columns[0], columns[1], columns[2], columns[3], 
				i, title_text, short_d, long_d, code))

		i = i + 1

	conn.commit()
	conn.close()