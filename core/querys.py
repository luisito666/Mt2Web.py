# Copyright (c) 2017-2018 ferchoafta@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php
event_top="""
DROP EVENT IF EXISTS `actualizar_top`;
CREATE event IF NOT EXISTS actualizar_top ON schedule every 1 hour starts "2018-01-01 00:00:00" do 
BEGIN 
	INSERT INTO estadisticas_registroconectados 
				(TIME, 
				 count) 
	VALUES      (Now(), 
				 (SELECT Count(*) 
				  FROM   player.player 
				  WHERE  last_play > Date_sub(Now(), interval 55 minute)) ) ;
  INSERT INTO varios_top 
              ( 
                          id, 
                          account_id, 
                          NAME, 
                          exp, 
                          level, 
                          ranking,
                          ip 
              ) 
  SELECT id, 
         account_id, 
         NAME, 
         exp, 
         0,0,
         ip
  FROM   player.player 
  WHERE  id> 
         ( 
                SELECT ifnull(max(id), 0) 
                FROM   varios_top); 
   
  update varios_top t1 
  JOIN   player.player t2 
  ON     t1.id = t2.id 
  AND    t1.level != t2.level 
  SET    t1.level = t2.level, 
         t1.ranking=1+ 
         ( 
                SELECT ifnull(max(ranking),0) 
                FROM   ( 
                              SELECT * 
                              FROM   varios_top) AS ga 
                WHERE  level=t2.level); 
   
  update varios_top t1 
  JOIN   player.guild_member t2 
  ON     t1.id=t2.pid 
  JOIN   player.guild t3 
  ON     t2.guild_id=t3.id 
  SET    t1.guild_name=t3.NAME; 

end ;"""

event_top=event_top.replace("\n","")
event_top=event_top.replace("\r","")
event_top=event_top.replace("      ","")
# print (event_top)