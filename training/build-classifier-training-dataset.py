#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import glob
import re

def clean_text(text):
	text = re.sub(r"[ \n\t]+", " ", text)
	text = re.sub(r"\"", "'", text)
	return text

def read_file(filename):
	with open(filename, 'r') as file:
		return file.read()

def save_file(filename, text):
	with open(filename, 'w') as file:
		file.write(text)

def main():
	directory = 'data/stp02_scraping/1_merged/'
	target_files = glob.glob(directory + "target_*")
	other_files = glob.glob(directory + "other_*")

	training_data = ""
	for filename in target_files:
		text = clean_text(read_file(filename))
		training_data += 'racismo\t{}\n'.format(text)

	for filename in other_files:
		text = clean_text(read_file(filename))
		training_data += 'other\t{}\n'.format(text)

	out_file = 'classifiers/training_set/training_data.tsv'
	save_file(out_file, training_data)

main()
