

## mysql命令
```sql
--增添列
ALTER TABLE torrents
ADD COLUMN status VARCHAR(20) DEFAULT 'active';

--改列名
ALTER TABLE torrents
CHANGE COLUMN torrentPath filePath VARCHAR(255);
```