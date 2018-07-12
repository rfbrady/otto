import pandas
import time
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import argparse
import os
import random
import csv

filedir = os.path.dirname(os.path.realpath('__file__'))
print(filedir)

filename = os.path.join(filedir, 'data\Final_SDG_dataset_case_1.xlsx')
print(filename)


parser = argparse.ArgumentParser(description="practice")
parser.add_argument('-l','--list',)

args = parser.parse_args()

if args.list:
	print('list arg is used')
debug = 1


if debug == 1:

	file = os.getcwd() + '\\data\\Final_SDG_dataset_case_1.xlsx'
	xl = pandas.ExcelFile(file)
	df = xl.parse('Final_SDG_dataset')
	ret = open('low_sdg_codes.csv', 'w')
	writer = csv.writer(ret, dialect='excel')
	writer.writerow('blah')
	codes = []
	codes_count = {}
	start_time = time.time()
	rows = df.shape[0]



	for i in range(rows):
		codes.append(df['sdg_codes'][i])

	print('\n there are %d unique codes' % len(set(codes)))
	print("\n---%s seconds to run---" % (time.time() - start_time))

	for val in set(codes):
		codes_count[val] = codes.count(val)
		#print("number of occurences of code {}: {}".format(val, codes.count(val)) )


	sorted_dict = sorted(codes_count.items())
	for val in set(codes):
		print("number of occurences of code {}: {}".format(val, codes.count(val)))

	#pretending to write code at the moment, this shouldnt need to go much longer. while it would be fun to go to amber ox, i think that I Will
	#just stay here, or go home. I shouldnt go home and get trashed, but I probably Will
	#reasons to go: would be fun, would be able to chat with my coworkers
	#reasons to not go, kayla might be there, it would be awkward to see the people that i ghosted.
	print("Show all codes that have less than __ values: ")
	num_values = 0
	selection = int(input())


	while selection != 666:
		for val in set(codes):
			if codes.count(val) <= selection:
				num_values = num_values + 1
				print("code {} occurs {} times".format(val, codes.count(val)))
		print("there are {} codes that are <= {}".format(num_values,selection))

		num_values = 0

		print("Show all codes that have <= __ values: ")
		selection = int(input())


	with open('code_frequency.csv','w', newline='') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['code','freq'])
	    for row in sorted_dict:
	        csv_out.writerow(row)
