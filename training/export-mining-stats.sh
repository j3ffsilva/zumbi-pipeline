#!/bin/bash

mysql -u root -p zumbi_train_pipe_db < db/sql/mining-stats.sql > stats/mining-stats.tsv