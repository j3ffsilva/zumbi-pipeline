select 
	tc.cod as miner_code, 
	tc.name as name, 
	count(tu.cod_miner) as num_urls 
from 
	tb_collaborators tc, 
	tb_url tu 
where 
	tc.cod = tu.cod_miner 
group by tc.cod, tc.name;