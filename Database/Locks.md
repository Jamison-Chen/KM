Locking 是許多 DBMS 用來進行 [concurrency control](</Database/Concurrency.md#Concurrency Control Protocols>) 的手段之一，比如 PostgreSQL 就有以下四種 locks：

- [Table-Level Locks](<# Table-Level Locks>)
- [Row-Level Locks](<# Row-Level Locks>)
- [Advisory Locks](<# Advisory Locks>)
- Page-Level Locks *(在 Application Level 通常毋須關注，故此處不詳述)*

其中 table-level lock 與 row-level lock 又可分為很多種 modes，某些 locks 彼此間會有 "conflict"，==任兩個進行中的 transactions 不能同時擁有相互 conflict 的 locks==，但一個 transaction 可以擁有會相互 conflict 的 locks，有些 locks 甚至自己與自己 conflict，那就代表這個 lock 一個時間只能為一個 transaction 所擁有。

# Table-Level Locks

### Access Share Lock

要執行 `SELECT` 就需要這種 lock。

### Row Share Lock

注意，雖然名字裡有 row，但它屬於 table-level lock。

要執行 `SELECT ... FOR UPDATE`, `SELECT ... FOR NO KEY UPDATE`, `SELECT ... FOR SHARE`, `SELECT ... FOR KEY SHARE` 就需要這種 lock。

### Row Exclusive Lock

注意，雖然名字裡有 row，但它屬於 table-level lock。

要執行 `UPDATE`, `DELETE`, `INSERT`,  `MERGE` 就需要這種 lock。換言之，只要是與「更動資料」相關就需要 row exclusive lock。

### Share Update Exclusive Lock

要執行 `VACUUM`, `ANALYZE`, `CREATE INDEX CONCURRENTLY`, `CREATE STATISTICS`, `COMMENT ON`, `REINDEX CONCURRENTLY` 等 commands，就需要這種 locks。

### Share Lock

要執行 `CREATE INDEX` 就需要這種 locks。

### Share Row Exclusive Lock

要執行 `CREATE TRIGGER` 就需要這種 locks。

### Exclusive Lock

要執行 `REFRESH MATERIALIZED VIEW CONCURRENTLY` 就需要這種 locks。

### Access Exclusive Lock

要執行 `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL`, `REFRESH MATERIALIZED VIEW` 就需要這種 locks。另外，其實執行 `LOCK TABLE` command 時預設就是取得 access exclusive lock。

---

### Conflicting Table

`❗: Conflict`

||Access Share|Row Share|Row Excl.|Share Update Excl.|Share|Share Row Excl.|Excl.|Access Excl.|
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|**Access Share**||||||||❗|
|**Row Share**|||||||❗️|❗️|
|**Row Excl.**|||||❗️|❗️|❗️|❗️|
|**Share Update Excl.**||||❗️|❗️|❗️|❗️|❗️|
|**Share**|||❗️|❗️||❗️|❗️|❗️|
|**Share Row Excl.**|||❗️|❗️|❗️|❗️|❗️|❗️|
|**Excl.**||❗️|❗️|❗️|❗️|❗️|❗️|❗️|
|**Access Excl.**|❗️|❗️|❗️|❗️|❗️|❗️|❗️|❗️|

# Row-Level Locks

### `FOR UPDATE` Lock

要執行 `SELECT ... FOR UPDATE`, `DELETE`, `UPDATE` 都需要有 target rows 的 `FOR UPDATE` lock。

若 transaction 握有某 row: R 的 `FOR UPDATE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT` 但後面不可以加上任何 `FOR ...` statement

### `FOR NO KEY UPDATE` Lock

若 transaction 握有某 row: R 的 `FOR UPDATE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT`（不加任何 `FOR ...`）以及 `SELECT ... FOR KEY SHARE`

### `FOR SHARE` Lock

若 transaction 握有某 row: R 的 `FOR SHARE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT`，但不可以 `SELECT ... FOR UPDATE` 與 `SELECT ... FOR NO KEY UPDATE`

### `FOR KEY SHARE` Lock

若 transaction 握有某 row: R 的 `FOR KEY SHARE` lock，則 R：

- 不可以被其它 transaction `DELETE`
- 可以被其它 transaction `SELECT` 但不可以 `SELECT ... FOR UPDATE`
- 可以被其它 transaction `UPDATE`「除了 key 以外」的欄位

---

### Conflicting Table

`❗: Conflict`

||For Key Share|For Share|For No Key Update|For Update|
|---|---|---|---|---|
|**For Key Share**||||❗|
|**For Share**|||❗️|❗️|
|**For No Key Update**||❗️|❗️|❗️|
|**For Update**|❗️|❗️|❗️|❗️|

# Advisory Locks

#TODO 

# 如何觸發與避免 Deadlocks

Deadlocks 是 OS 以及 DBMS 常常需要關注的議題，如果你還不熟悉，建議先讀 [此文](</Operating System/Deadlocks.md>)。

這裡舉一個在 DMBS 中可能會觸發 deadlocks 的例子。在一個銀行的資料庫中，現在有下面兩個 transactions 同時在進行，分別是 a 要轉帳 100 元給 b，以及 b 要轉帳 1000 元給 a，SQL 如下：

**Transaction 1**

```PostgreSQL
BEGIN
UPDATE balance SET balance = balance - 100 WHERE id = 'a';  -- (1)
UPDATE balance SET balance = balance + 100 WHERE id = 'b';  -- (2)
COMMIT
```

**Transaction 2**

```PostgreSQL
BEGIN
UPDATE balance SET balance = balance - 1000 WHERE id = 'b';  -- (3)
UPDATE balance SET balance = balance + 1000 WHERE id = 'a';  -- (4)
COMMIT
```

若銀行的資料庫採用 [SS2PL Protocol](</Database/MVCC vs. SS2PL.md#SS2PL>) 進行 concurrency control，且 schedule 的順序是 `(1)` $\to$ `(3)` $\to$ `(2)` $\to$ `(4)`，那 Deadlocks 就會在 `(3)` 跟 `(2)` 之間產生！

為了執行 `(1)`，Transaction 1 握著 balance(a) 的 row exclusive lock；為了執行 `(3)`，Transaction 2 握著 balance(b) 的 row exclusive lock。而若要執行 `(2)`，Transaction 1 就需要取得 balance(b) 的 row exclusive lock；若要執行 `(4)`，Transaction 2 就需要取得 balance(a) 的 row exclusive lock。因為現在使用的是 SS2PL protocol，所以要在 commit 或 rollback transaction 後，locks 才會被釋放，於是雙方進入了 deadlocks。

那在這個例子中，可以怎麼避免 deadlocks 呢？答案就是==注意 SQL 的順序==！如果兩個 transactions 都先對 balance(a) `UPDATE`，再對 balance(b) `UPDATE`，那無論 schedule 的結果如何，都不會進入 deadlocks。

當然，這只是一個簡單且好解決的例子，實務上有些時候 deadlocks 會在哪裡發生是很難設想周到的，好在 PostgreSQL 會定期檢查，透過 abort deadlocks 中的其中一個 transaction 來解除 deadlocks。

# 參考資料

- <https://www.postgresql.org/docs/current/explicit-locking.html>
