# -*- coding: UTF-8 -*-

insert_collaborator = "INSERT INTO tb_collaborators(cod, name) VALUES (%s, %s);"

### URL
insert_miner_url_stmt = "INSERT INTO tb_url(cod_miner, url) VALUES (%s, %s);"
last_url_index = "SELECT max(id) FROM tb_url;"
find_by_url_stmt = "SELECT id FROM tb_url WHERE url = %s;"
update_url_stat_by_id_stmt = "UPDATE tb_url SET art_status = %s WHERE id = %s;"
update_url_stat_by_url_stmt = "UPDATE tb_url SET art_status = %s WHERE url = %s;"