#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import nltk
import numpy as np
from math import log
from sklearn import metrics
from spacy.lang.pt import Portuguese
from spacy.tokenizer import Tokenizer
from . import classifiers_config as config
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class RacialClassifier:
	""" 
	Constructor
	"""
	def __init__(self, file_id=None, text=None):
		self.__nlp = Portuguese()
		self.__stemmer = SnowballStemmer(language='portuguese')
		discr_terms = self.__read_discriminatory_terms_lst()
		self.__racial_stems = self.__stem_discriminative_terms(discr_terms)
		self.__file_id = file_id
		self.__text = text
		self.__model = None

	"""
	Public methods
	"""

	def calc_terms_probs(self, articles):
		print("==>\tCalculating discriminative term probabilities")
		# freq_vector: accumulated term frequency
		freq_vector = self.__initiaze_freq_vector()
		for article_id in articles.keys():
			text = articles[article_id]
			tokens = self.__tokenizer(text)
			stems = self.__stem(tokens)
			# rsp_vec: 1 if a racial stem is present in the text, 0 otherwise 
			rsp_vec = self.__racial_stem_presence_vector(stems)
			# sum vectors for probability calculation
			freq_vector = self.__sum_vecs(rsp_vec, freq_vector)
		prob_vector = self.__make_term_prob_vec(freq_vector, len(articles))
		# Write probabilities into a file
		self.__write_term_probs(prob_vector)
		print("==>\tWritten term probabilities in file {}".format(config.PROBS_FILE))

	def score(self, text, article_id=None):
		tokens = self.__tokenizer(text)
		stems = self.__stem(tokens)
		racial_term_freq = self.__racial_stem_freq_vector(stems)
		probs = self.__read_terms_probs()
		score = self.__score_formula(racial_term_freq, probs, len(tokens))
		return [article_id, score]

	def predict(self, text, article_id=None):
		features = self.__vectorize(text)
		return self.__model.predict(features)

	def train_nb(self):
		print("==>\tStarted Training")
		X, y = self.__split_text_and_target(config.SCORE_FILE)
		X_vec = self.__vectorize(X)
		X_train, X_test, y_train, y_test = train_test_split(X_vec, y, random_state=1)
		# Use multinomial naive bayes
		classifier = MultinomialNB(class_prior=[0.7,0.3])
		# Train model
		self.__model = classifier.fit(X_train, y_train)
		return self.__model, X_test, y_test

	"""
	Private methods
	"""

	def __read_lines(self, filename):
		with open(filename, 'r') as file:
			return file.read().split('\n')

	def __split_text_and_target(self, filename):
		text, target = [], []
		lines = self.__read_lines(filename)
		for line in lines:
			cols = line.split('\t')
			text.append(cols[1])
			target.append(cols[0])
		return text, target

	def __vectorize(self, texts):
		vec = []
		for text in texts:
			tokens = self.__tokenizer(text)
			stems = self.__stem(tokens)
			vec.append(self.__racial_stem_freq_vector(stems))
		return vec

	def __read_discriminatory_terms_lst(self):
		with open(config.DISCRIMINATIVE_TERMS_FILE, 'r') as file:
			return file.read().split('\n')

	def __stem_discriminative_terms(self, discr_terms):
		stemmed = []
		for i in range(len(discr_terms)):
			stem = self.__stemmer.stem(discr_terms[i])
			if (stem not in stemmed):
				stemmed.append(stem)
		return stemmed

	def __racial_stem_presence_vector(self, text_stems):
		return [1 if stem in text_stems else 0 for stem in self.__racial_stems]

	def __racial_stem_freq_vector(self, text_stems):
		return [text_stems.count(stem) for stem in self.__racial_stems]

	def __tokenizer(self, text):
		doc = self.__nlp.tokenizer(text)
		return [t.text for t in doc]

	def __stem(self, tokens):
		return [self.__stemmer.stem(token) for token in tokens]

	def __make_term_prob_vec(self, freq_vector, num_files):
		return [elem/num_files for elem in freq_vector]

	def __vec2str(self, vector):
		res = ""
		i = 0
		for item in vector:
			res = res + str(item)
			if (i < len(vector)):
			 	res += "\t"
			else:
			 	res += "\n"
			i += 1
		return res

	def __write_term_probs(self, prob_vector):
		with open(config.PROBS_FILE, 'w') as file:
			probs_str = self.__vec2str(prob_vector)
			file.write(probs_str)

	def __initiaze_freq_vector(self):
		return [0] * len(self.__racial_stems)

	def __sum_vecs(self, vec1, vec2):
		return [vec1[i]+vec2[i] for i in range(len(vec1))]

	def __read_terms_probs(self):
		with open(config.PROBS_FILE, 'r') as file:
			probs_str = file.read().split('\t')
			return [p_str for p_str in probs_str]

	def __score_formula(self, freq_vec, probs, num_words):
		tam_vec = len(freq_vec)
		return sum([log(freq_vec[i] + 1) * float(probs[i]) for i in range(tam_vec)])