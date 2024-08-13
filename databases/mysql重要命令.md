

## mysql命令
```sql
--增添列
ALTER TABLE torrents
ADD COLUMN status VARCHAR(20) DEFAULT 'active';

--改列名
ALTER TABLE torrents
CHANGE COLUMN torrentPath filePath VARCHAR(255);

ALTER TABLE my_table 
CHANGE old_column new_column VARCHAR(255);

--第一列之前插入新的列并赋默认值
ALTER TABLE employee ADD COLUMN employee_id INT DEFAULT 0 FIRST;
ALTER TABLE torrents ADD COLUMN isDownloaded BOOL DEFAULT FALSE;

ALTER TABLE torrents
ADD COLUMN type VARCHAR(255) DEFAULT 'null' AFTER id;

--删除列
ALTER TABLE torrents
DROP COLUMN status;


--修改
UPDATE employees
SET employee_id = 1
WHERE employee_id = 0;

--LIKE
SELECT * FROM customers
WHERE name LIKE '_a%';

--清空表
TRUNCATE TABLE table_name;
```