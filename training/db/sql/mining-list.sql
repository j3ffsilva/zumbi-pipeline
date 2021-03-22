select 
	tc.cod as miner_code, 
	tc.name as name, 
	tu.url 
from 
	tb_url tu, 
	tb_collaborators tc 
where 
	tc.cod = tu.cod_miner 
order by tc.cod;