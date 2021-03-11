#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from spacy.language import Language
import spacy
import re

@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):
	quotes_count = 0
	for token in doc[:-1]:
		#print("{}".format(token.text))
		if (token.text == "\""):
			quotes_count += 1
		if (quotes_count % 2 == 1):
			doc[token.i + 1].is_sent_start = False
	return doc

def preprocess(text):
	text = re.sub(r'[“”]', '"', text)
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

def sent2jsonl(a_sentence):
	return "{\"text\":\"" + a_sentence + "\"}" + "\n"

def text_2_jsonl_sents(text):
	preprocess(text)
	nlp = spacy.load("pt_core_news_sm")
	nlp.add_pipe("set_custom_boundaries", before="parser")
	doc = nlp(text)
	sentences = [clean_sentence(sent.text) for sent in doc.sents]
	remove_all_elems_eq_to(sentences, '')
	jsonl_sents = [sent2jsonl(a_sent) for a_sent in sentences]
	return jsonl_sents