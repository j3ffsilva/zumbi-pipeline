#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import config
import argparse
import glob
from util.tsv_reader import read_discard_title
from sentencizers.spacy_sentencizer import text_2_jsonl_sents
from util import filehelper as fh
from n3k.scraper import ScrapedArticle
from tqdm import tqdm
from URL import URL
from time import sleep

def build_urls(input_file):
	return [URL(row[0], row[2]) for row in read_discard_title(input_file)]

def scrape_urls(urls):
	print("==> Started Step #2: Scraping")
	for url in tqdm(urls):
		if not url.exists():
			url.persist()
			sleep(config.SCRAPING_SLEEP_TIME)
			article = ScrapedArticle(url)
			if article and article.save_as_scraped():
				url.update_status_by_url(
					config.get_article_status("scraped"),
					url=url.text())

def sentencize_article(sentencizer_input_dir):
	print("==> Started Step #3: Sentencizing")
	# Make a list of all the files that need to be segmented
	files_4_sentencizer = 									\
		get_articles_4_sentencizer(sentencizer_input_dir)
	# Sentencize each file and update DB
	for full_name in tqdm(files_4_sentencizer):
		jsonl_sents = text_2_jsonl_sents(fh.read(full_name))

		# Save sentences into output directory
		filename = fh.get_filename(full_name)
		save_article_as_sentencized(filename, jsonl_sents)

		# Updates URL status on the DB
		file_id = fh.get_file_id(filename)
		URL('', '').update_status_by_id(
					  config.get_article_status("sentencized"), 
					  id=file_id)

def get_articles_4_sentencizer(article_dir):
	return glob.glob(article_dir + "article_*")

def save_article_as_sentencized(filename, jsonl_sents):
	filename = filename.replace('.txt', '.jsonl')
	output_file = config.SENTENCIZER_OUTPUT_DIR + filename
	fh.write_list(output_file, jsonl_sents)

def main(input_file):
	### Step 1: Scrape URLs
	scrape_urls(build_urls(input_file))

	### Step 2: Sentencize articles
	sentencize_article(config.SENTENCIZER_INPUT_DIR)

if (__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", type=str,
						help="Filename containing the URLs to racial discrimination news articles")
	args = parser.parse_args()
	input_file = None
	if (args.input):
		input_file = args.input
	else:
		input_file = config.MINED_URL_FILENAME
	main(input_file)