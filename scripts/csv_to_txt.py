import csv
import os
import codecs

ifp = os.getcwd() + '/Cambodia_2000_2013_uncoded.csv'
ofp = os.getcwd() + '/Cambodia_2000_2013_uncoded.txt'
text_list = []


with codecs.open(ifp, 'r', encoding='latin-1') as csv_file:
	for line in csv_file.readlines():

		text_list.append(line)

with open(ofp, 'w') as txt_file:
	for line in text_list:
		txt_file.write(line)

