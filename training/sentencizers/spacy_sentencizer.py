#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from spacy.language import Language
import spacy
import re

QUOTE_SYMBOL = "'"

@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):
	quotes_count = 0
	for token in doc[:-1]:
		#print("{}".format(token.text))
		if (token.text == QUOTE_SYMBOL):
			quotes_count += 1
		if (quotes_count % 2 == 1):
			doc[token.i + 1].is_sent_start = False
	return doc

def preprocess(text):
	text = re.sub(QUOTE_SYMBOL,'’', text)
	text = re.sub(r'[“”]', '"', text)
	text = re.sub(r'"', QUOTE_SYMBOL, text)
	text = re.sub(r'  +', ' ', text)
	return text

def clean_sentence(sentence):
	sentence = re.sub(r'\n', ' ', sentence)
	sentence = re.sub(r'  +', ' ', sentence)
	return sentence.strip()

def remove_all_elems_eq_to(sentences, elem):
	count = sentences.count(elem)
	for i in range(count):
		sentences.remove(elem)

def count_elem(text, elem):
	return text.count(elem)

def format(a_sentence):
	return a_sentence + "\n"

def text_2_jsonl_sents(text, filename):
	text = preprocess(text)
	nlp = spacy.load("pt_core_news_lg")
	if (count_elem(text, QUOTE_SYMBOL) % 2 == 0):
		nlp.add_pipe("set_custom_boundaries", before="parser")
	else:
		print("==> did not setting custom boundaries for file {}".format(filename))
	doc = nlp(text)
	sentences = [clean_sentence(sent.text) for sent in doc.sents]
	remove_all_elems_eq_to(sentences, '')
	jsonl_sents = [format(a_sent) for a_sent in sentences]
	return jsonl_sents