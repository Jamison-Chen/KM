|Log Type|Information Written to Log|
|---|---|
|Error log|Problems encountered starting, running, or stopping **mysqld**|
|General query log|Established client connections and statements received from clients|
|Binary log|Statements that change data (also used for replication)|
|Relay log|Data changes received from a replication source server|
|Slow query log|Queries that took more than `long_query_time` seconds to execute|
|DDL logs|Atomic DDL operations performed by DDL statements|

# Binlog

- 全名是 binary log
- 被用在 [[Database Replication]] 上
- 分為 statement-based logging 與 row-based logging，前者是把每個會動到資料的 query 記錄下來；後者是把資料的前後差異記錄下來

# 參考資料

- <https://dev.mysql.com/doc/refman/9.0/en/server-logs.html>
