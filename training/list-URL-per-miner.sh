#!/bin/bash

mysql -u root -p zumbi_train_pipe_db < db/sql/mining-list.sql > stats/URLs-per-miner.tsv