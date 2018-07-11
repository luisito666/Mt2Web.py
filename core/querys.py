# Copyright (c) 2017-2018 ferchoafta@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php
event_top="""
CREATE EVENT IF NOT EXISTS actualizar_top ON SCHEDULE EVERY 1 HOUR STARTS "2018-01-01 00:00:00" DO BEGIN INSERT INTO varios_top(id, account_id, name,exp,level,ranking) select id,account_id,name,exp,0,0 from player.player where id>(SELECT IFNULL(MAX(id), 0) from varios_top); UPDATE varios_top t1 JOIN player.player t2 ON t1.id = t2.id and t1.level != t2.level SET t1.level = t2.level, t1.ranking=1+(select 	IFNULL(max(ranking),0) from (select * from varios_top) as ga where level=t2.level); update varios_top t1 JOIN player.guild_member t2 ON t1.id=t2.pid JOIN player.guild t3 ON t2.guild_id=t3.id SET t1.guild_name=t3.name; END ;
"""