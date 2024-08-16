

## mysql命令
```sql
--增添列
ALTER TABLE torrents
ADD COLUMN status VARCHAR(20) DEFAULT 'active';

--改列名
ALTER TABLE mikantorrents
CHANGE COLUMN infoHash infoHash VARCHAR(2048);

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
    
--删除表    
DROP TABLE mikantorrents;


-- 将符合条件的数据从源表转移到目标表
INSERT INTO tem
SELECT * FROM torrents
WHERE type = "mikan";


-- 完全重置id，把所有数据的id从1开始全部重新排序

-- 1. 创建一个临时表来保存现有数据
CREATE TEMPORARY TABLE temp_table AS SELECT * FROM your_table;

-- 2. 删除原始表中的所有数据，并重置自增ID
TRUNCATE TABLE your_table;

-- 3. 将数据从临时表插入回原始表，并重新生成ID
INSERT INTO mikantorrents (type, pubDate, title, description, link, enclosureLink, infoHash, savePath, isDownloaded)
SELECT type,pubDate, title, description, link, enclosureLink, infoHash,  savePath, isDownloaded FROM tem;

-- 4. 删除临时表
DROP TEMPORARY TABLE tem;
```