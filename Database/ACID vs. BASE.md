# ACID

### Atomicity

一個 [[淺談 Database#Database Transaction|Transaction]] 「執行成功」的定義是「transaction 中的每個步驟都成功」，==若任一個步驟執行失敗，就要 **rollback** 到第一個步驟執行前的狀態，好像什麼事都沒發生一樣==。

當一個 transaction 「執行成功」後，會進行一個叫 **commit** 的動作，換言之 transaction 的結局有兩種，分別對應到一個動作：

- 成功：執行 commit
- 失敗：執行 rollback

為何需要 rollback？假設在一個銀行的資料庫中，account A 要轉帳 n 元給 account B，撇除其他細節不談，最重要的步驟有兩個：

1. 將 account A 的 balance 減去 n
2. 將 account B 的 balance 加上 n

如果步驟一執行成功、步驟二執行失敗，但卻沒有 rollback，那 A 的 n 元就從這個世界上蒸發了，由此可見 rollback 的重要性。

**Recoverability**

「可以 rollback」這個性質叫做 "recoverability"，有兩種做法可以達到 recoverability：

- **Logging**

    紀錄每一個對資料庫的操作紀錄，紀錄的資訊包括「在什麼時候」把「什麼資料」的值「從什麼改成什麼」，commit 失敗時依據 log 把資料庫回溯為原先的狀態。

- **Shadow Paging**

    把當前 transaction 預計要改動到的資料所在的 page 先複製一份出來，transaction 是對複製出來的資料做改動，commit 成功才將指向原本 page 的 pointer 改為指向複製出來的 page；反之，若 commit 失敗就直接把複製出來的 page 捨棄即可。

    這個做法現在較少見，主要是因為效能問題。目前採用此做法的資料庫包括 CouchDB。

### Consistency

Consistency 包括："Consistency in Data" 與 "Consistency in Read"

- **Consistency in Data**

    aka [[Integrity Constraint]]

- **Consistency in Read**

    Transaction 讀到的資料永遠是最新的。在某些情境中，完美的 Consistency in Read 是很難達成的，比如當服務是由不止一個 database 在掌管資料時，由於 database 之間的 syncing 須要時間，須要給 databases 一點時間才能達到 Consistency in Read，這叫做 Eventual Consistency。

==Relational Database 相對於 NoSQL 最大的優勢即在於前者在單一 database 的情境下能提供 Consistency，但後者通常只能做到 Eventual Consistency==。

### Isolation

任兩個進行中 (in-flight) 的 transactions 不應互相影響／干擾，甚至不應看到彼此對資料庫所造成的影響，否則可能會出現 [[Concurrency#Concurrency Anomalies|Concurrency Anomalies]]。

##### Complete Isolation - Serializability

在具有一定用戶數量的應用程式中，「同時有多位用戶在存取資料庫」是很正常的事，web server 有能力平行 (parallel) 處理多個 requests，DBMS 也有能力平行處理多個 transactions。而 Perfect Isolation 的目標是：「==多個被同時執行的 transactions 執行完後，資料庫的狀態 (state) 應與 transactions 以某種特定順序一個接著一個被執行的結果一樣==」。

*注：DBMS 會平行處理不同 client connections 所發起的 queries；但同一個 client connection 所發起的多個 queries 只會被一個接著一個處理。*

##### Isolation Level

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

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/read-uncommitted.png>)

- **Read Committed**

    一個 transaction 可以讀到另一個「執行完」的 transaction 對資料庫所做的「所有更動」。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/read-committed.png>)

- **Repeatable Read**

    一個 transaction 可以讀到另一個「執行完」的 transaction 在資料庫「新增」的資料，但讀不到舊資料「被更改後的值」。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/repeatable-read.png>)

- **Serializable**

    一個 transaction 讀不到所有在它開始之後，所有他以外的 transaction 對資料庫做的「所有更動」。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/serializable.png>)

### Durability

一旦 transaction 被 commit 了，即使後來系統當機，結果也應該保存著。

有些服務使用 Memory 來達到 Caching 機制（如 Redis），這種服務就不符合 Durability。

# BASE

### Basically Available

#TODO 

### Soft State

#TODO 

### Eventually Consistent

#TODO 

# 參考資料

- <https://www.youtube.com/watch?v=pomxJOFVcQs>
- <https://phoenixnap.com/kb/acid-vs-base>
- <https://fauna.com/blog/introduction-to-transaction-isolation-levels>
- <https://stackoverflow.com/questions/4980801/how-simultaneous-queries-are-handled-in-a-mysql-database>
