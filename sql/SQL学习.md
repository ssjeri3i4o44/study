# SQL



## PART -1 SELECT

表结构 world(name, continet,area, population,gdp)

![](.\img\1.jpg)

- 列出每个国家的名字当中人口是高于俄罗斯的人口

  ```sql
  select name from world where population > (select population where name='Russia');
  ```

- 列出欧洲每个国家人均GDP当中人均GDP要高于英国（United Kingdom）的数值

  ```sql
  select name from population where continent = ‘Europe' and (gdp/population)>(select gdp/population from world where name='United Kingdom');
  ```

- 在阿根廷Argentina及澳大利亚Australia所在洲中，列出当中的国家名字name及洲份continent，按国家名字排序

  ```sql
  select name,continent from world where continet in (select dictinct continet from world where name='Argentina' or name='Australia') order by name;
  ```

- 哪一个国家的人口比加拿大Conada的多，但比波兰Poland的少？列出国家名字name和人口population；

  ```sql
  select name,population from world where population >(select population from world where name='Conada') and population <(select population from world where name='Poland');
  ```

- Germany德国（人口8000万），在欧洲国家的人口最多。Austria奥地利（人口850万）拥有德国人口的11%。显示欧洲国家名称name和每个国家人口的population。以德国人口的百分比作人口显示。

  ```sql
  select name, concat(round(pupulation/(select population where name='Germany')*100,0),'%') as new_po from world where continent='Europe';
  ```

  concat()函数：将多个字符串连接成一个字符串。concat(str1,str2)

  round(x,d)函数：用于数据的四舍五入，x指要处理的树，d指保留几位小数

- 找到世界上人口最多的国家;

  ```sql
  SELECT name from world where population >=ALL(SELECT population from world where population >0);
  ```

  使用populatin>0是因为有些国家的记录中，人口是空的

- 哪些国家的GDP比Europe欧洲的全部国家都要高？只需列出name（有些国家的记录中，GDP是NULL）

  ```sql
  SELECT name FROM world WHERE gdp > ALL(SELECT gdp FROM world WHERE continet='Europe' AND gdp>0);
  SELECT name FROM world WHERE gdp > (SELECT MAX(gdp) FROM world WHERE continet='Europe' AND gdp>0);
  ```

- 在每个洲找到最大面积的国家，列出洲份continent，国家名字name和面积area。

  ```sql
  SELECT continent,name,area FROM world as x WHERE area >=ALL(SELECT area FROM world as y where y.continent=x.continent and area>0)
  ```

- 列出洲份名称和每个洲份中国家名字按字母排序是排首位的国家名

  ```sql
  SELECT continent, name FROM(
      SELECT continent, name，
      ROW_NUMBER() OVER(PARTITION BY continent ORDER BY name) as num
      FROM world
  ) as a
  WHERE a.num=1;
  
  ```

  ROW_NUMBER() OVER(PARTITION BY column OREDER BY column):其中PARTITION BY可以不写，ORDER BY必须写

- 找出洲份当中全部国家人口都少于或等于25000000，在这些洲份当中列出国家名字name,洲份continent和人口population

  ```sql
  解1：
  SELECT name,continent,population 
  FROM world a 
  WHERE
  (SELECT MAX(population) FROM world b 
   WHERE b.continent=a.continent)<=2500000;
   解2：
   SELECT name,continent,population FROM world a WHERE
   2500000 >= ALL(SELECT population FROM world b WHERE b.continent=a.continent and population>0);
  ```

- 有些国家的人口是同洲份所有其他国家的3倍或以上。列出国家名字name和洲份continet;

```sql
SELECT name, continent FROM world a WHERE population/3 >=
ALL(SELECT population FROM world b WHERE a.continent=b.continent and population>0 and a.name!=b.name);
```

PART-2 JION

![](\img\2-1.jpg)

![](\img\2-2.jpg)

![](\img\2-3.jpg)

- 列出赛事编号matchid和球员名player,该球员代表德国队Germany入球的。

```sql
SELECT matchid,player FROM goal WHERE termid='GRE';
```

- 由以上查询，你可见Lars Benher's于赛事1012入球。现在我们想知道此赛事的对赛队伍是哪一个。留意在goal表格中的matchid，是对应表格game的id。只显示赛事1012的 id, stadium, team1, team2

  ```sql
  SELECT id, stadium, team1,team2 FROM game WHERE id=1012
  ```

- 列出每个入球的球员（来自goal表格）和场馆名（来自game表格）。修改它来显示每个德国入球的球员名，队伍名，场馆和日期。

  ```sql
  SELECT a.palyer, a.teamid,b.stadium,b.mdate FROM
  (SELECT matchid,player,teamid FROM goal WHERE teamid='GRE') a
  left join
  (SELECT id, mdate, stadium FROM game) b on a.teamid=b.id;
  ```

- 列出球员名字叫Mario有入球的队伍1team1,队伍2和球员名player.

  ```sql
  SELECT a.palyer,b.team1, b.team2 FROM 
  (SELECT matchid, palyer FROM goal WHERE player like '%Mario%') a
  left join
  (SELECT id, team1, team2 FROM game) b on a.teamid=b.id;
  ```

- 列出每场球赛中前10分钟gtime<=10有入球的球员player，队伍teamid,教练coach,入球时间gtime。

  ```sql
  SELECT a.player,a.teamid,b.coach,a.gtime FROM
  (SELECT teamid,player,gtime FROM goal WHERE gtime <=10) a
  left join
  (SELECT id, coach FROM eteam) c on a.teamid=c.id;
  ```

- 列出'Fernando Santos'作为队伍1team1的教练的赛事时间和队伍名

  ```sql
  SELECT c.coach, c.teamname, a.mdate FROM
  (SELECT id, coach, teamname FROM eteam WHERE coach='Fernando Santos') c
  left join
  (SELECT team1, mdate FROM game) a on a.team1 = c.id
  ```

- 列出场馆“National Stadium, Warsaw”的入球球员

  ```sql
  SELECT b.player FROM 
  (SELECT id, stadium FROM game WHERE stadium='National Stadium, Warsaw') a
  left join
  (SELECT matchid, player FROM goal) b
  WHERE a.id=b.matchid;
  ```

- 修改它，只列出全部赛事，射入德国龙门的球员名字。

  ```sql
  SELECT distinct a.player
  ```

- 列出队伍名称teamname和该队入球总数

  ```sql
  SELECT  c.teamname, count(b.teamid) as goal_num FROM
  (SELECT teamid FROM goal) b
  left join
  (SELECT id, teamname FROM eteam) c
  WHERE b.teamid=c.id
  group by c.teamname;
  ```

- 列出场馆名和在该场馆的入球数字

  ```sql
  SELECT a.stadium， count(b.matchid) FROM
  (SELECT matchid FROM goal) b
  left join
  (SELECT id, stadium FROM game) a
  WHERE a.id=b.matchid
  group by a.stadium
  ```

- 每一场波兰'POL'有参与的赛事中，列出赛事编号matchid，日期date与入球数字

  ```sql
  SELECT b.matchid, a.mdate, count(*) FROM
  (SELECT id, mdate FROM game WHERE team1='POL' or team2='POL') a
  JOIN
  (SELECT matchid FROM gola) b
  on a.id=b.matchid
  group by b.matchid;
  ```

- 每一德国'GER'有参与的赛事中，列出赛事编号matchid，日期date与德国入球数字

  ```sql
  SELECT b.matchid, a.mdate,count(*) FROM
  (SELECT matcid FROM goal HWERE teamid='GER') b
  RIGHT JOIN
  (SELECT id, mdate FROM game WHERE team1='GER' or team2='GER') a
  on a.id=b.matchid
  group by b.matchid;
  ```

  # PART-3 MORE JOIN

  数据库中三个表格：

  movie电影(id编号, title电影名称, yr首影年份, director导演, budget制作费, doss票房收入)

  actor演员(id编号, name姓名)

  casting角色(movieid电影编号,actorid演员编号,ord角色次序)

- 列出1962年的首影电影，显示id,title

  ```sql
  SELECT id, title FROM movie WHERE yr=1962;
  ```

- 列出电影北非谍影‘Casablanca'(moveid=11768)的演员名单

  ```sql
  SELECT b.name FROM
  (SELECT actorid FROM catsing WHERE movieid=11768) c
  LEFT JOIN
  (SELECT id, name FROM actor) b
  on c.actorid=b.id;
  ```

- 显示电影类型’Alian‘的演员清单

  ```sql
  SELECT b.name FROM
  (SELECT id FROM movie WHERE title='Alian') a
  LEFT JOIN
  (SELECT movieid, actorid FROM casting) b
  ON a.id=b.movieid
  LEFT JOIN
  (SELECT id,name FROM actor) c
  ON b.movieid=c.id;
  ```

- 列出演员"Harrison Ford"曾演出的电影

  ```sql
  SELECT a.title FROM
  (SELECT id FROM actor WHERE name = 'Harrison Ford') b
  LEFT JOIN
  (SELECT movieid,actorid FROM casting) c
  ON b.id=c.actorid
  LEFT JOIN
  (SELECT id,title FROM movie) a
  ON a.id = c.movieid;
  ```

- 列出演员"Harrison Ford"曾演出的电影,但他不是第一主角

  ```sql
  SELECT a.title FROM 
  (SELECT id FROM actor WHERE name = 'Harrison Ford') b
  LEFT JOIN
  (SELECT movieid,actorid,ord FROM casting) c
  ON b.id=c.actorid
  LEFT JOIN
  (SELECT id,title FROM movie) a
  ON a.id = c.movieid
  WHERE c.ord!=1;
  ```

- 列出1962年首影的电影及它的第1主角

  ```sql
  SELECT a.title, b.name FROM
  (SELECT id, title FROM movie WHERE yr=1962) a
  LEFT JOIN
  (SELECT movieid, actorid,ord FROM casting) c
  ON a.id=c.movieid
  LEFT JOIN
  (SELECT id,name FROM actor) b
  ON b.id=c.actorid
  WHERE b.ord=1;
  ```

- 'John Travolta'最忙的是哪一年？显示年份和该年的电影数目

  ```sql
  SELECT a.yr, count(*) as movie_num FROM 
  (SELECT id FROM actor WHERE name='John Travolta') b
  LEFT JOIN
  (SELECT movieid, actorid FROM casting) c
  ON b.id=c.actorid
  (SELECT id, yr FROM movie) a
  ON a.id=b.movieid
  group by yr
  order by movie_num DESC
  limit 1;
  ```

- 列出Julie Andrews曾参与的电影名称及其第1主角；

  ```sql
  SELECT a.title, b.name FROM
  (SELECT DISTINCT movieid FROM casting WHERE id = (SELECT id FROM actor WHERE name='Julie Andrews')) c
  LEFT JOIN
  (SELECT movieid,actorid FROM casting WHERE ord=1) d
  ON c.movieid = d.movieid
  LEFT JOIN
  (SELECT id, title FROM movioe) a
  ON a.id = d.movied
  LEFT JOIN
  (SELECT id, name FROM actor) b
  ON b.id=d.actorid;
  ```

- 列出按字母顺序，哪位演员作为第一主角出演30次

```sql
SELECT b.name FROM 
(SELECT actorid AS actor_num FROM casting WHERE ord = 1 group by actorid HAVING COUNT(movieid)>=30) c
LEFT JOIN
(SELECT id,name FROM actor) b
ON b.id=c.actorid；
```

- 列出1978年首影的电影名称及角色数目，按此数目由多到少排列。

  ```sql
  SELECT a.title, count(c.ord) AS ord_num FROM 
  (SELECT id, title FROM movie WHERE yr=1978) a
  INNER JOIN
  (SELECT movieid FROM casting) c
  ON a.id = c.movieid
  GROUP BY title
  ORDER BY ord_num DESC;
  ```

- 列出演员Art Garfunkel合作过的演员姓名

  ```sql
  SELECT b.name FROM
  (SELECT id, name FROM actor) b
  RIGHT JOIN
  (SELECT DISTINCT actorid FROM casting WHERE movieid IN 
   (SELECT movieid FROM casting WHERE 
    actorid = (SELECT id FROM actor WHERE name = 'Art Garfunkel')) and 
    actorid != (SELECT id FROM actor WHERE name ='Art Garfunkel' )) c
   ON b.id=c.actorid;
  ```

  

