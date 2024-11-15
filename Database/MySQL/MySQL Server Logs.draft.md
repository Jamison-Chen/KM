|Log Type|Information Written to Log|
|---|---|
|Error log|Problems encountered starting, running, or stopping **mysqld**|
|General query log|Established client connections and statements received from clients|
|Binary log|Statements that change data (also used for replication)|
|Relay log|Data changes received from a replication source server|
|Slow query log|Queries that took more than `long_query_time` seconds to execute|
|DDL logs|Atomic DDL operations performed by DDL statements|

# Binary Log

- 簡稱 binlog
- 被用在 [Database Replication](</System Design/Database Replication.md>) 上，是 master node 用來記錄資料變動的地方，記錄在 binlog 裡的東西會被送到 replica db
- 分為 statement-based logging 與 row-based logging，前者是把每個「可能」會動到資料的 query 都記錄下來（包括改動到 0 筆資料的 `DELETE` query）；後者是把資料的前後差異記錄下來

# Relay Log

#TODO 

# 參考資料

- <https://dev.mysql.com/doc/refman/9.0/en/server-logs.html>
