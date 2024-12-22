Locking 是許多 DBMS 用來進行 [concurrency control](</Database/Concurrency.md#Concurrency Control Protocols>) 的手段之一，比如 PostgreSQL 就有以下四種 locks：

- [Table-Level Locks](<# Table-Level Locks>)
- [Row-Level Locks](<# Row-Level Locks>)
- [Advisory Locks](<# Advisory Locks>)
- Page-Level Locks *(在 Application Level 通常毋須關注，故此處不詳述)*

其中 table-level lock 與 row-level lock 又可分為很多種 modes，某些 locks 彼此間會有 "conflict"，==任兩個進行中的 transactions 不能同時擁有相互 conflict 的 locks==，但一個 transaction 可以擁有會相互 conflict 的 locks，有些 locks 甚至自己與自己 conflict，那就代表這個 lock 一個時間只能為一個 transaction 所擁有。

# Table-Level Locks

### Access Share Lock

Related query：`SELECT`

### Row Share Lock

雖然名字裡有 row，但它屬於 table-level lock！

Related query：`SELECT ... FOR UPDATE`、`SELECT ... FOR NO KEY UPDATE`、`SELECT ... FOR SHARE`、`SELECT ... FOR KEY SHARE`

### Row Exclusive Lock

雖然名字裡有 row，但它屬於 table-level lock！

只要是與「更動資料」相關就需要 row exclusive lock。

Related query：`UPDATE`、`DELETE`、`INSERT`、`MERGE`

### Share Update Exclusive Lock

Related query：`VACUUM`、`ANALYZE`、`CREATE INDEX CONCURRENTLY`、`CREATE STATISTICS`、`COMMENT ON`、`REINDEX CONCURRENTLY`

### Share Lock

Related query：`CREATE INDEX`

### Share Row Exclusive Lock

Related query：`CREATE TRIGGER`

### Exclusive Lock

Related query：`REFRESH MATERIALIZED VIEW CONCURRENTLY`

### Access Exclusive Lock

Related query：`DROP TABLE`、`TRUNCATE`、`REINDEX`、`CLUSTER`、`VACUUM FULL`、`REFRESH MATERIALIZED VIEW`

執行 `LOCK TABLE` command 時預設是取得 access exclusive lock。

---

### Conflicting Table

`❗: Conflict`

| |Access Share|Row Share|Row Excl.|Share Update Excl.|Share|Share Row Excl.|Excl.|Access Excl.|
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

Related query：`SELECT ... FOR UPDATE`、`DELETE`、`UPDATE`

若 transaction 握有某 row (R) 的 `FOR UPDATE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT` 但後面不可以加上任何 `FOR ...` statement

### `FOR NO KEY UPDATE` Lock

若 transaction 握有某 row (R) 的 `FOR UPDATE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT`（不加任何 `FOR ...`）以及 `SELECT ... FOR KEY SHARE`

### `FOR SHARE` Lock

若 transaction 握有某 row (R) 的 `FOR SHARE` lock，則 R：

- 不可以被其它 transaction `DELETE`、`UPDATE`
- 可以被其它 transaction `SELECT`，但不可以 `SELECT ... FOR UPDATE` 與 `SELECT ... FOR NO KEY UPDATE`

### `FOR KEY SHARE` Lock

若 transaction 握有某 row (R) 的 `FOR KEY SHARE` lock，則 R：

- 不可以被其它 transaction `DELETE`
- 可以被其它 transaction `SELECT` 但不可以 `SELECT ... FOR UPDATE`
- 可以被其它 transaction `UPDATE`「除了 key 以外」的欄位

---

### Conflicting Table

`❗: Conflict`

| |For Key Share|For Share|For No Key Update|For Update|
|---|---|---|---|---|
|**For Key Share**||||❗|
|**For Share**|||❗️|❗️|
|**For No Key Update**||❗️|❗️|❗️|
|**For Update**|❗️|❗️|❗️|❗️|

# Advisory Locks

#TODO 

# Deadlocks - 如何觸發與避免

>[!Note]
>關於 deadlocks 的基本知識可以看[[Deadlocks|這篇]]。

這裡舉一個在 DMBS 中可能會觸發 deadlocks 的例子：在一個銀行的資料庫中，現在有下面兩個 transactions 同時在進行，分別是 a 要轉帳 100 元給 b，以及 b 要轉帳 1000 元給 a，SQL 如下：

**Transaction 1**

```SQL
BEGIN;
UPDATE balance SET balance = balance - 100 WHERE id = 'a';  -- (1)
UPDATE balance SET balance = balance + 100 WHERE id = 'b';  -- (2)
COMMIT;
```

**Transaction 2**

```SQL
BEGIN;
UPDATE balance SET balance = balance - 1000 WHERE id = 'b';  -- (3)
UPDATE balance SET balance = balance + 1000 WHERE id = 'a';  -- (4)
COMMIT;
```

若銀行的資料庫採用 [[MVCC vs. SS2PL#SS2PL|SS2PL Protocol]] 進行 concurrency control，且 schedule 的順序是 `(1)` $\to$ `(3)` $\to$ `(2)` $\to$ `(4)`，那 deadlocks 就會在 `(3)` 跟 `(2)` 之間產生！

為了執行 `(1)`，Transaction 1 握著 balance(a) 的 row exclusive lock；為了執行 `(3)`，Transaction 2 握著 balance(b) 的 row exclusive lock。而若要執行 `(2)`，Transaction 1 就需要取得 balance(b) 的 row exclusive lock；若要執行 `(4)`，Transaction 2 就需要取得 balance(a) 的 row exclusive lock。因為現在使用的是 SS2PL protocol，所以要在 commit 或 rollback transaction 後，locks 才會被釋放，於是雙方進入了 deadlocks。

那在這個例子中，可以怎麼避免 deadlocks 呢？答案就是==注意 SQL 的順序==！如果兩個 transactions 都先對 balance(a) `UPDATE`，再對 balance(b) `UPDATE`，那無論 schedule 的結果如何，都不會進入 deadlocks。

當然，這只是一個簡單且好解決的例子，實務上 DB 可能在同一時間處理很多個 transactions，其中哪些 transactions 間會產生 deadlocks 是很難設想周到的。好在大部分 DBMS（比如 PostgreSQL）都會定期檢查，透過 abort deadlocks 中的其中一個 transaction 來解除 deadlocks。

#TODO 

# Optimistic Locking vs. Pessimistic Locking

Optimistic locking 與 pessimistic locking 是兩類不同的實作 lock 的方式／策略：

- Optimistic locking
    - 認爲在 read 與 update 中間的 time gap 裡「不會」有其他人來更新這筆資料
    - 在 read 與 update 中間的 time gap 裡「不會」阻止其他人來更新或刪除這筆資料
    - 萬一真的有人更新了這筆資料，那失敗的是擁有 lock 的人
- Pessimistic locking
    - 認爲在 read 與 update 中間的 time gap 裡會有其他人來更新這筆資料
    - 在 read 與 update 中間的 time gap 裡會阻止其他人來更新或刪除這筆資料
    - 可能會造成 deadlock

# 參考資料

- <https://www.postgresql.org/docs/current/explicit-locking.html>
- <https://www.aneasystone.com/archives/2017/10/solving-dead-locks-one.html>
- <https://www.aneasystone.com/archives/2017/11/solving-dead-locks-two.html>
- <https://www.aneasystone.com/archives/2017/12/solving-dead-locks-three.html>
- <https://www.aneasystone.com/archives/2018/04/solving-dead-locks-four.html>
