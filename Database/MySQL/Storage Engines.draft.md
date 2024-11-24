Storage engine 是 MySQL 中負責管理資料如何被儲存、讀取、更新、刪除的 software component。

在 MySQL 中，storage engine 有很多種，不同的 storage engine 有不同功能、適合不同使用場景，使用者可以自行決定要使用什麼 storage engine，這點和 PostgreSQL 不一樣（PostgreSQL 只有一種內建的 storage，透過安裝 extension 來擴充功能）。

# 常見的 Storage Engines

常見的 storage engine 包括 InnoDB、MyISAM、memory、CSV... 等。

### InnoDB

- 是 MySQL 9.0 後預設的 storage engine，也是最普遍被使用的 storage engine。
- 支援 [transaction](</Database/0 - Introduction.md#Database Transaction>)、[Index](</Database/Index.md>)、[row-level lock](</Database/Locks.md#Row-Level Locks>)、[foreign-key constraint](</Database/Integrity Constraints.md#Referential-Integrity Constraint>)，因此==適合高併發讀寫環境==。
- 有 [Buffer Pool](</Database/MySQL/Buffer Pool of InnoDB.md>) 與 [Adaptive Hash Index](</Database/MySQL/Adaptive Hash Index.md>) 可以加快讀取速度。
- 有 checksum 機制，避免當資料損毀時沒被注意到。
- 符合 [ACID model](</Database/ACID vs. BASE.md#ACID>) 的要件。

### MyISAM

不支援 row-level locking，只支援 table-level locking，寫入時會影響到別人讀取的速度，因此==適合 read-only 或 read-mostly== 的使用場景。

### Memory

把所有資料都存在 memory 裡，優點是可以快速存取，缺點是資料具有揮發性 (volatile)，且 memory 的空間通常比 disk 小很多。

這種 storage engine 現在已經越來越不流行了，因為其它 engines 後來也開始會利用 memory 作為 cache 來加快存取的速度，比如 InnoDB 的 Buffer Pool。

### CSV

一個 table 就是一個 CSV file，缺點是不能做 [indexing](</Database/Index.md>)，所以讀取速度很慢。CSV 通常只會在匯入或匯出資料時會使用。

# 相關 SQL

### 查看所有 Storage Engines

在 MySQL CLI 中使用以下 SQL 可以查看所有種類的 storage engine、它們特色，以及 MySQL 是否支援... 等資訊：

```SQL
SHOW ENGINES;
```

### 設定預設選用的 Storage Engine

e.g.

```SQL
SET default_storage_engine=NDBCLUSTER;
```

MySQL 9.0 預設是用 `InnoDB`。

### 建立 Table 時選擇要使用的 Storage Engine

e.g.

```SQL
CREATE TABLE t1 (i INT) ENGINE = InnoDB; -- ENGINE=INNODB not needed unless you have set a different default storage engine.
CREATE TABLE t2 (i INT) ENGINE = CSV;
CREATE TABLE t3 (i INT) ENGINE = MEMORY;
```

### 更改既有 Table 的 Storage Engine

e.g.

```SQL
ALTER TABLE t ENGINE = InnoDB;
```

# 參考資料

- <https://dev.mysql.com/doc/refman/9.0/en/storage-engines.html>
- <https://dev.mysql.com/doc/refman/9.0/en/innodb-storage-engine.html>
- <https://dev.mysql.com/doc/refman/9.0/en/innodb-benefits.html>
