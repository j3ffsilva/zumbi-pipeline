# -*- coding: UTF-8 -*-

import csv

def read_discard_title(input_file, title_len=1):
	"""
	Read a tsv file discarding titles
	Default: 1 title line discarded
	"""
	lst = [row[0].split("\t") for row in csv.reader(open(input_file))]
	del lst[0:title_len]
	return lst
