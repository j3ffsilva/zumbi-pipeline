#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import config
from db.sql.statements import insert_miner_url_stmt
from db.sql.statements import find_by_url_stmt
from db.sql.statements import update_url_stat_by_id_stmt
from db.sql.statements import update_url_stat_by_url_stmt
from util.database import get_db_connector

class URL:
	def __init__(self, miner, url):
		"""
		Construtor
		miner: the identification of the person who collected the URL
		url: the URL as a string
		"""
		self.__miner = miner
		self.__url = url
		self.id = None

	def text(self):
		"""
		Returns the URL (str)
		"""
		return self.__url

	def miner(self):
		"""
		Returns the identification of the person who mined (collected) the URL
		"""
		return self.__miner

	def find_by_url(self):
		"""
		Returns the id of the URL in the database.
		Need the URL
		"""
		idx = None
		conn = get_db_connector()
		try:
			cursor = conn.cursor()
			cursor.execute(find_by_url_stmt, (self.__url,))
			row = cursor.fetchone()
			if (row):
				idx = int(row[0])
		except:
			return None
		finally:
			try:
				cursor.close()
				conn.close()
			except:
				pass
		self.id = idx
		return idx

	def exists(self):
		"""
		Returns True if URL exists in the database and False otherwise
		"""
		return False if not self.find_by_url() else True

	def persist(self):
		"""
		Persists the URL in the database. 
		Returns False if URL is already in the database and True otherwise.
		"""
		if self.exists():
			return False
		conn = get_db_connector()
		try:
			cursor = conn.cursor()
			cod = self.__miner
			url = self.__url
			cursor.execute(insert_miner_url_stmt, (cod, url))
			conn.commit()
		except:
			return False
		finally:
			try:
				cursor.close()
				conn.close()
			except:
				pass
		return True

	def update_status_by_url(self, new_status, url=None):
		"""
		Updates the URL status in the database.
		"""

		if not url:
			if not self.__url:
				return False
			url = self.__url
		conn = get_db_connector()
		try:
			cursor = conn.cursor()
			cursor.execute(update_url_stat_by_url_stmt, (new_status, url))
			conn.commit()
		except:
			return False
		finally:
			try:
				cursor.close()
				conn.close()
			except:
				pass
		return True

	def update_status_by_id(self, new_status, id=None):
		"""
		Updates the URL status in the database by id.
		"""
		if not id:
			if not self.id:
				return False
			id = self.id
		conn = get_db_connector()
		try:
			cursor = conn.cursor()
			cursor.execute(update_url_stat_by_id_stmt, (new_status, id))
			conn.commit()
		except:
			return False
		finally:
			try:
				cursor.close()
				conn.close()
			except:
				pass
		return True

#url = URL('RA00297746', 'https://g1.globo.com/rs/rio-grande-do-sul/noticia/ufsm-aprova-novo-codigo-de-conduta-apos-casos-de-estupro-e-racismo.ghtml')
