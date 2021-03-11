#!/usr/bin/env python3

import config
import argparse
from util.database import get_db_connector
from db.sql.statements import insert_collaborator
import traceback

def add_collaborator(cod, name):
	try:
		conn = get_db_connector()
		cursor = conn.cursor()
		cursor.execute(insert_collaborator, (cod, name))
		conn.commit()
		print("Sucessfully added {} as a collaborator".format(name))
	except:
		traceback.print_exc()
	finally:
		try:
			cursor.close()
			conn.close()
		except:
			pass

if (__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--code", type=str, help="Collaborator unique code")

	parser.add_argument("-n", "--name", type=str, help="Collaborator name")

	args = parser.parse_args()
	if (args.code and args.name):
		add_collaborator(args.code, args.name)
	else:
		print("usage")