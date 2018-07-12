import csv
import os

ifp = os.getcwd() + '/truncated_valid.csv'
ofp = os.getcwd() + '/truncated_valid.txt'
text_list = []


with open(ifp, 'r') as csv_file:
	for line in csv_file.readlines():

		text_list.append(line)

with open(ofp, 'w') as txt_file:
	for line in text_list:
		txt_file.write(line)

