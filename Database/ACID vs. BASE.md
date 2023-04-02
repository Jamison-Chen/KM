# CAP Theorem (Brewer's Theorem)

CAP Theorem 指出，一個服務最多只能同時確保 Consistency, Availability 與 Partition Tolerance 三者的其中兩個：

![[Screen Shot 2023-02-04 at 8.30.11 AM.png]]

- Consistency: Clients 總是可以從資料庫讀取到最新的資料
- Availability: 所有 Request 都會得到 non-error 的 Response
- Partition Tolerance: 除了通訊問題以外，服務必須持續運作不間斷

而 ACID Transaction Model 的宗旨即「在具備 Partition Tolerance 的條件下，提供具備 Consistency 的服務」(CP)，銀行業通常會需要這種 Model。

相對地，BASE Transaction Model 的宗旨為「在具備 Partition Tolerance 的條件下，提供具備 Availability 的服務」(AP)。

# Database Transaction

Transaction 字面上的意思：「交易」意味著一手交錢、一手交貨，一旦買方拿不出錢，或者賣方無法提供貨品，或者買方無法接收貨品，或者賣方無法接收錢，這個交易就不算成功。

在資料庫的世界中，transaction 的定義衍變成「一個可以包含若干個 database queries 的工作」，所有 queries 都執行成功後，會進行 "**commit**" 來表示這個 transaction 執行成功。

下面示範如何使用 PostgreSQL 寫一個 transaction：

```PostgreSQL
BEGIN;

-- Update the balance of a bank account.
UPDATE accounts SET balance = balance - 100
WHERE account_number = '123456';

-- Insert a new transaction record.
INSERT INTO transactions (account_number, transaction_date, amount)
VALUES ('123456', CURRENT_DATE, 100);

-- Commit the transaction if all statements have succeeded,
-- rollback otherwise.
COMMIT;
```

其實就是在要打包的 queries 的開頭加上一行 `BIGIN;`，結尾加上一行 `COMMIT;` 而已。

# ACID

### Atomicity

如果一個 transaction 「執行成功」的定義是「transaction 中的每個步驟都成功」，==若任一個步驟執行失敗，就要 **rollback** 到第一個步驟執行前的狀態，好像什麼事都沒發生一樣==，那我們就說這個 transaction 具備 atomicity，白話文就是「不可分割性」。

當一個 transaction 「執行成功」後，會進行一個叫 **commit** 的動作，換言之 transaction 的結局有兩種，分別對應到一個動作：

- 成功：執行 commit
- 失敗：執行 rollback

為何需要 rollback？假設在一個銀行的資料庫中，account A 要轉帳 n 元給 account B，撇除其他細節不談，最重要的步驟有兩個：

1. 將 account A 的 balance 減去 n
2. 將 account B 的 balance 加上 n

如果步驟一執行成功、步驟二執行失敗，但卻沒有 rollback，那 A 的 n 元就從這個世界上蒸發了，由此可見 rollback 的重要性。

*注：「可以 rollback」這個性質叫做 "recoverability"。*

### Consistency

Consistency 包括："Consistency in Data" 與 "Consistency in Read"

- **Consistency in Data**

    a.k.a. [[Integrity Constraint]]

- **Consistency in Read**

    Transaction 讀到的資料永遠是最新的。在某些情境中，完美的 Consistency in Read 是很難達成的，比如當服務是由不止一個 database 在掌管資料時，由於 database 之間的 syncing 須要時間，須要給 databases 一點時間才能達到 Consistency in Read，這叫做 Eventual Consistency。

==Relational Database 相對於 NoSQL 最大的優勢即在於前者在單一 database 的情境下能提供 Consistency，但後者通常只能做到 Eventual Consistency==。

### Isolation

>任兩個進行中 (in-flight) 的 transactions 不應互相影響／干擾，甚至不應看到彼此對資料庫所造成的影響，否則可能會出現 [[Concurrency#^fc28ed|Concurrency Anomalies]]。

**Complete Isolation - Serializability**

在具有一定用戶數量的應用程式中，「同時有多位用戶在存取資料庫」是很正常的事，web server 有能力平行 (parallel) 處理多個 requests，DBMS 也有能力平行處理多個 transactions。而 Perfect Isolation 的目標是：「==多個被同時執行的 transactions 執行完後，資料庫的狀態 (state) 應與 transactions 以某種特定順序一個接著一個被執行的結果一樣==」。

*注：DBMS 會平行處理不同 client connections 所發起的 queries；但同一個 client connection 所發起的多個 queries 只會被一個接著一個處理。*

**Isolation Level**

SQL Standard 將 Isolation 由寬鬆到嚴格分為四種等級：

|Isolation Level|Dirty read|Non-repeatable read|Phantom Read|
|---|---|---|---|
|Read Uncommitted|✅ Possible|✅ Possible|✅ Possible|
|Read Committed|🚫 Not Possible|✅ Possible|✅ Possible|
|Repeatable Read|🚫 Not Possible|🚫 Not Possible|✅ Possible|
|Serializable|🚫 Not Possible|🚫 Not Possible|🚫 Not Possible|

由上表可見，SQL Standard 用來界定 Isolation level 的 anomalies 其實很少（都只與「讀取」相關），所以其實這些 level 間的界線是模糊的，且就算是最高階的 Serializable 也不是完美的 Isolation。

- **Read Uncommitted** *(No Isolation)*

    一個 transaction 可以讀到另一個「執行到一半」的 transaction 對資料庫所做的「所有更動」。

    ![[Screen Shot 2023-02-02 at 1.02.18 PM.png]]

- **Read Committed**

    一個 transaction 可以讀到另一個「執行完」的 transaction 對資料庫所做的「所有更動」。

    ![[Screen Shot 2023-02-02 at 1.02.33 PM.png]]

- **Repeatable Read**

    一個 transaction 可以讀到另一個「執行完」的 transaction 在資料庫「新增」的資料，但讀不到舊資料「被更改後的值」。

    ![[Screen Shot 2023-02-02 at 1.17.00 PM.png]]

- **Serializable**

    一個 transaction 讀不到所有在它開始之後，所有他以外的 transaction 對資料庫做的「所有更動」。

    ![[Screen Shot 2023-02-02 at 1.21.35 PM.png]]

### Durability

一旦 transaction 被 commit 了，即使後來系統當機，結果也應該保存著。

有些服務使用 Memory 來達到 Caching 機制（如 Redis），這種服務就不符合 Durability。

# BASE

### Basically Available

### Soft State

### Eventually Consistent

# 參考資料

- <https://en.wikipedia.org/wiki/CAP_theorem>
- <https://www.youtube.com/watch?v=pomxJOFVcQs>
- <https://phoenixnap.com/kb/acid-vs-base>
- <https://fauna.com/blog/introduction-to-transaction-isolation-levels>
- <https://stackoverflow.com/questions/4980801/how-simultaneous-queries-are-handled-in-a-mysql-database>
