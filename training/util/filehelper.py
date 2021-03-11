#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

def read(full_filename):
	"""
	Read the content of a file
	"""
	with open(full_filename, 'r') as file:
		return file.read()

def write(full_filename, text):
	"""
	Save the file into a specific directory
	"""
	with open(full_filename, 'w') as file:
		file.write(text)

def write_list(full_filename, text_lst):
	"""
	Save the content as a list
	"""
	with open(full_filename, 'w') as file:
		for text in text_lst:
			file.write(text)

def get_filename(full_filename):
	"""
	Returns the last element of a path, which is the filename
	"""
	return full_filename.split("/")[-1]

def get_file_id(filename):
	"""
	Returns the database id of a file
	"""
	return re.split("[_.]", filename)[1]