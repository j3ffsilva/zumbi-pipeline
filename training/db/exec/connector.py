# -*- coding: UTF-8 -*-

import mysql.connector
import credentials
import config

def get_db_connector():
	return mysql.connector.connect(
		host="localhost",
		user=credentials.user,
		password=credentials.pwd,
		database=config.TRAINING_PIPELINE_DB
	)