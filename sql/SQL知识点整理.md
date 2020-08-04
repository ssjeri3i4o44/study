# 1、SQL基础

1. 选择 select

2. 表连接 join\left join\right join\union

3. 去重 distinct

4. 筛选 having/where

5. 聚合 max\min\sum\count+group by

6. 排序order by /sort by

7. 条件case when...end

   case when 条件1 then value1 esle nujll end(esle可省略，end不可省略)

8. 字符串 substr/concat/split

   concat(A,B...)返回将A和B顺序连接在一起的字符串，如concat('foo','bar')返回'foobar'

   split(str, regex)将string类型数据按regex提取，分隔后转换为array

   substr(str,0, len)截取字符串从0位开始的长度为len个字符

9. 日期函数 to_date/datediff

   to_date("yyyy-mm-dd hh:mm::ss")：转化为时间数据格式

   datediff(date1,date2):计算两个时间的相差天数

   date_sub(startdate, days):返回开始日期startdate减少days天后的日期

   date_add(startdate, days):返回开始日期startdate增加days天后的日期

10. 分组排序row_number

11. 取百分比percentile

    其使用方式为percentile(col, p)、percentile_approx(col, p,B)， 返回col列p分位上的值。B用来控制内存消耗的精度。实际col中distinct的值<B返回的时精确的值。
    其中percentile要求输入的字段必须是int类型的，而percentile_approx则是数值类似型的都可以 .

12. 窗口排序

    row_number()/rank()/dense_rank()

13. 分区最大/最小

    first_value() over()分组内排序后，截止到当前第一个

    last_value() over()分组内排序后，截止到当前最后一个

    ```sql
    SELECT *,
    		#分组取每个组的最大对应的人
    		FIRST_VALUE(name) 
    		OVER(PARTITION BY deparment ORDER BY cost DESC) as max_cost_user, 
    		#分组取每个组的最少对应的人
    		FIRST_VALUE(name) 
    		OVER(PARTITION BY deparment ORDER BY cost) as min_cost_user
    	FROM
    	    table;
    		
    ```

14. 累积百分比

    cume_dist()  over():返回小于等于当前值的行数/分组内总行数

    sum() over():累计值的占比，

    ```sql
    SELECT *,
            CUME_DIST() 
            OVER(PARTITION BY department ORDER BY cost DESC) AS cume_dist,
            SUM(cost) OVER(PARTITION BY department ORDER BY cost DESC)
            /SUM(cost) OVER(PARTITION BY department) AS s
    FROM 
        tabel
    WHERE 
         department='A'
    ```

15. 错位

    lead/lag 函数：一般用于计算差值，最适用于计算花费时间。

    lead用于统计窗口内往下第n行值，

    lag用于统计窗口内往上第n行值

    ```sql
    #查看部门内每个人花费排名比他更高一名的人的费用
    SELECT *,
           LEAD(cost) OVER(PARTITION by department ORDER BY cost) next_cost
    FROM tabel;
    ```

16. 日期函数

    - 日期（YYYY-MM-dd HH:mm:ss）和unix时间戳之间相互转换

      **日期转unix时间戳**：unix_timestamp(string date, string patten),转换pattern格式的日期到时间戳

      **unix时间戳转日期**：from_unixtime(bigint unixtime, [string format])

      ```sql
      unix_timestamp('20200321 13:01:03','yyyyMMdd HH:mm:ss')
      unix_timestamp('20200321','yyyyMMdd')
      
      #时间戳转日期
      from_unixtime (1584782175)
      from_unixtime (1584782175,'yyyyMMdd')
      from_unixtime (1584782175,'yyyy-MM-dd')
      
      #日期和日期之间也可以通过时间戳转换
      from_unixtime(unix_timestamp('20200321','yyyymmdd'),'yyyy-mm-dd')
      from_unixtime(unix_timestamp('2020-03-21','yyyy-mm-dd'),'yyyymmdd')
      ```

      unix_timestamp(string date)默认转换格式为“yyyyMMdd HH:mm:ss”

    - 日期(yyyyMMdd HH:mm:ss)转换为(yyyyMMdd)格式

      ```sql
      #直接使用to_date函数
      to_date('2020-03-21 17:13:39')
      #字符串提取
      substr('2020-03-21 17:13:39',1,10)
      ```

    - 日期之间加减操作

      **date_add(string satrtdate, int days)**:得到开始日期satrtdate增加days后的日期

      **date_sub(string satrtdate, int days)**:得到开始日期satrtdate减少days后的日期

      **datediff(string enddate, string startdate)**:得到enddate减去startdate的天数

17. 字符串函数

    - **字符串提取**

      substr/substring(string A, int start):返回字符串A从start位置到结尾的字符串

      substring(string A, int start, int len)：返回字符串A从start位置开始，长度为len的字符串

      ```sql
      substring('abcde', 3) 
      返回cde
      
      substring('abcde', 3, 2)
      返回cd
      ```

    - **字符串拼接**

      concat(string A, string B):返回字符串AB的拼接结果，可以多个字符串进行拼接

      concat_ws(string X, string A, string B):返回字符串A和B由X拼接的结果

      ```sql
      concat('abc','def','gh')
      返回abcdefgh
      concat_ws(',','abc','def','gh')
      返回abc,de,gh
      ```

    - **字符串的常见处理函数**

      length(string A)：返回字符串A的长度

      trim(string A) :去除字符串两边的空格

      lower(string A)/lcase(string A):返回字符串小写形式

      upper(string A)/ucase(string A):返回字符串大写形式

    - 不同格式数据转换：cast

      cast(A to sting) :转换为字符串

    - 正则表达式

      **regexp_extract(string subject, string pattern, int index)**:字符串subject按照pattern正则表达式的规则拆分，返回index指定的字符

      **regexp_repalce(string A,string B, string C)**:将字符串A中符合正则表达式B的部分替换为C

      ```sql
      regexp_extract('foothebar','foo(.*?)(bar)',1)
      返回the
      regexp_replace('foobar','oo|ar','')
      返回fb
      ```

    - 字符串解析

      get_json_object(string json_string, string path):解析json字符串json_string, 返回path指定的内容

      ```sql
      get_json_object({"from_remain_count":420,"reason":"collect","to_remain_count":0},'$.from_remain_count')
      返回420
      ```

    


# 2. SQL错题整理：

1.修改表test字段i的缺省值为1000：

```sql
ALTER TABLE test ALTER COLUMN i SET DEFAULT 1000;
```

2.某打车公司将驾驶里程（drivedistanced）超过5000里的司机信息转移到一张称为seniordrivers 的表中,他们的详细情况被记录在表drivers 中

```sql
SELECT * INTO seniordrivers FROM drivers WHERE drivedistanced>=5000;
```

**INSERT INTO** 语句用于**向表格中插入新行**：

```
INSERT INTO table_name VALUES (值1，值2)；
INSERT INTO table_name (列1，列2,...) VALUES (值1，值2,..)
```

**SELECT INTO**语句**从一个表中选取数据，然后把数据插入另一个表中**：

```sql
把所有的列插入新表：
SELECT * 
INTO new_table_name [IN externaldatabase]
FROM old_table_name

SELECT columns_name(s)
INTO new_table_name [IN externaldatabase]
FROM old_table_name
```

3.查询显示雇员的姓名和姓名中是否含有字母A的信息，满足如下条件
如果字符A在姓名的首位，则显示'字符A在首位'
如果字符A在姓名的末位，则显示'字符A在末位'
如果字符A在姓名中不存在，则显示'没有字符A'
其他情况显示'字符A在中间'。

```
SELECT ename, case charindex('A', ename)
WHEN 1 THEN '字符A在首位'
WHEN LEN(ename) THEN '字符A在末位'
WHEN 0 THEN '没有字符A'
ELSE '字符A在中间'
END 名称类别 FROM emp；
```

通过CHARINDEX如果能够找到对应的字符串，则返回该字符串位置，否则返回0。

4.分组查询（group by）

```sql
#不同省份的独立订单数
SELECT 省,COUNT(DISTINCT(订单ID)) 订单数 FROM 订单 GROUP BY 省;
#不同省、不同城市独立订单数
SELECT 省,城市,COUNT(DISTINCT(订单ID)) 订单数 FROM 订单 GROUP BY 省;
```

注意使用GROUP BY语句时，要将GROUP BY后面的元素放在SELECT后面第一位

如果想要知道每个省一共多少订单，其中有多少订单类别是家具类，占比是多少，可以利用IF函数来计算。在COUNT中0也会计算，所以要吧if函数的第三个函数携程null,代表类别不是家具的就排除在外。

```sql
SELECT 省，COUNT(订单ID),COUNT(IF (类别 LIKE '%家具%', 订单ID, NULL) FROM 订单 GROUP BY 省);
```

5.HAVING子句

用于在GROUP BY语句的条件下继续添加条件，注意不能使用WHERE语句，WHERE语句和HAVING语句不能共存。

```sql
#每订单总利润
SELECT 订单ID,地区,省,城市,SUM(利润)利润 FROM 订单 GROUP BY 订单ID HAVING 地区='华东地区'；
```

6.子查询

```
#筛选出退货的订单ID
SELECT 订单ID FROM 退货 WHERE 退货='是';
#找出这些订单详情
SELECT * FROM 退货 WHERE 订单ID IN (SELECT 订单ID FROM 退货 WHERE 退货='是');
```

7.表连接

```sql
1.简单的连接查询
SELECT * FROM Table_A A JOIN Table_B B ON A.订单ID=B.退货ID;
2.内连接
SELECT * FROM Table_A INNER JOIN Table_B B ON A.订单ID=B.退货ID;
3.左连接
SELECT * FROM Table_A LEFT JOIN Table_B B ON A.订单ID=B.退货ID;
```

6.修改数据表中的数据

```sql
1.ALTER语句
#添加数据列，将添加列设置为double类型，长度为10，小数点为2
ALTER TABLE table_name ADD COLUMN column_name DOUBLE(10,2);
#删除数据列
ALTER TABLE table_name DROP COLUMN column_name;

2.UPDATA语句
UPDATE table_name SET new_column=column1-column2;

3.DELETE语句
DELETE FROM table_name WHERE column1='1111';
```

7.函数排名

- row_number( ):将select查询到的数据进行排序，每条数据加一个序号，一般用于分页查询。如果出现相同数字也会依次排序并且序号不同，如12345。

- rank( ):对某一字段进行排序，如果出现相同数字会依次排序并且序号相同。但排序是跳跃性的，如12245.
- dense_rank():和rank()一样，如果出现相同数字会依次排序并且序号相同。但排序是连续的，如12234
- ntile() over(order by [列])：按照指定列对数据进行分组

