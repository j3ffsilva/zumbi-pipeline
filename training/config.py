# -*- coding: UTF-8 -*-

TRAINING_PIPELINE_DB = "zumbi_train_pipe_db"

# Step 1
MINED_URL_DIR = "data/stp01_url-mining/"
MINED_URL_FILENAME = MINED_URL_DIR + "stp01-URLs-on-racial-discrimination.tsv"

# Step 2
SCRAPER_OUTPUT_DIR = "data/stp02_scraping/1_scraped/"
SCRAPING_SLEEP_TIME = 0 # (in seconds)

# Step 3
SENTENCIZER_INPUT_DIR = SCRAPER_OUTPUT_DIR
SENTENCIZER_OUTPUT_DIR = "data/stp03_annotation/1_sentencized/"

def get_article_status(key):
	article_status_dict = {
		"mined": 1, 
		"scraped": 2, 
		"scraped_failed":3, 
		"sentencized": 4,
		"sentencized_failed": 5
	}
	return article_status_dict[key]