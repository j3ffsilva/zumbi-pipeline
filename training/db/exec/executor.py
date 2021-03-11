#!/usr/bin/env python

import traceback
from db.exec.connector import get_db_connector

def execute_batch(stmt, vals, msg="Successfull"):
	try:
		conn = get_db_connector()
		cursor = conn.cursor()
		for val in vals:
			try:
				cursor.execute(stmt, val)
			except:
				print("URL {} is probably not unique".format(val))

		conn.commit()
		print(msg)
	except:
		traceback.print_exc()
	finally:
		try:
			cursor.close()
			conn.close()
		except:
			pass

def execute(stmt, val, msg="Sucessfull"):
	try:
		conn = get_db_connector()
		cursor = conn.cursor()
		cursor.execute(stmt, val)
		conn.commit()
		print(msg)
	except:
		traceback.print_exc()
	finally:
		try:
			cursor.close()
			conn.close()
		except:
			pass

def execute(stmt, val, msg="Sucessfull"):
	try:
		conn = get_db_connector()
		cursor = conn.cursor()
		cursor.execute(stmt, val)
		conn.commit()
		print(msg)
	except:
		traceback.print_exc()
	finally:
		try:
			cursor.close()
			conn.close()
		except:
			pass