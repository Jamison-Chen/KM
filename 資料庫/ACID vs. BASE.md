# CAP Theorem (Brewer's Theorem)

---

CAP Theorem 指出，一個服務最多只能同時確保 Consistency, Availability 與 Partition Tolerance 三者的其中兩個：

![[Screen Shot 2023-02-04 at 8.30.11 AM.png]]

- Consistency: End users 總是可以從資料庫讀取到最新的資料
- Availability: 所有 Request 都會得到 non-error 的 Response
- Partition Tolerance: 除了通訊問題以外，服務必須持續運作不間斷

而 ACID Transaction Model 的宗旨即「在具備 Partition Tolerance 的條件下，提供具備 Consistency 的服務」，銀行業通常會需要這種 Model。

相對地，BASE Transaction Model 的宗旨為「在具備 Partition Tolerance 的條件下，提供具備 Availability 的服務」。

# 何謂 Transaction

---

Transaction 最原始的定義其實就是字面上的意思：「交易」，必須一手交錢一手交貨，一旦買方拿不出錢，或者賣方無法提供貨品，或者買方無法接收貨品，或者賣方無法接收錢，這個交易就不算成功。

同理，在資料庫的世界中，一個 transaction 可能包含若干個與資料庫溝通 (query) 的步驟，所有步驟都執行成功後，會進行 "**commit**" 來表示這個 transaction 執行成功。

# ACID

---

### Atomicity

如果一個 transaction 「執行成功」的定義是「transaction 中的每個步驟都成功」，==若任一個步驟執行失敗，就要 **rollback** 到第一個步驟執行前的狀態，好像什麼事都沒發生一樣==，那我們就說這個 transaction 具備 atomicity，白話文就是「不可分割性」。

當一個 transaction 「執行成功」後，會進行一個叫 **commit** 的動作，換言之 transaction 的結局有兩種，分別對應到一個動作：

- 成功：執行 commit 
- 失敗：執行 rollback

為何需要 rollback？假設在一個銀行的資料庫中，account A 要轉帳 n 元給 account B，撇除其他細節不談，最重要的步驟有兩個：

1. 將 account A 的 balance 減去 n
2. 將 account B 的 balance 加上 n

如果步驟一執行成功、步驟二執行失敗，但卻沒有 rollback，那 A 的 n 元就從這個世界上蒸發了，由此可見 rollback 的重要性。

### Consistency

Consistency 包括："Consistency in Data" 與 "Consistency in Read"

- **Consistency in Data**
	
	- [[Referential Integrity (參照完整性)]]
	- 其他自定義的規則（比如：商品的售價一定要大於成本）

- **Consistency in Read**
	
	Transaction 讀到的資料永遠是最新的。在某些情境中，完美的 Consistency in Read 是很難達成的，比如當服務是由不止一個 database 在掌管資料時，由於 database 之間的 syncing 須要時間，須要給 databases 一點時間才能達到 Consistency in Read，這叫做 Eventual Consistency。

==Relational Database 相對於 NoSQL 最大的優勢即在於前者在單一 database 的情境下能提供 Consistency，但後者通常只能做到 Eventual Consistency==。

### Isolation

在具有一定用戶數量的應用程式中，「同時有多位用戶在存取資料庫」是很常發生的事，web app 有能力平行 (parallel) 處理多個 requests，資料庫也有能力平行處理多個 queries。

>資料庫會平行 (parallel) 處理每個不同 client connection 所發起的 queries；但同一個 client connection 所發起的多個 queries 則會被一個接著一個處理。

而 Isolation 的定義即：「任兩個進行中 (in-flight) 的 transactions 不應互相影響／干擾，甚至不應看到彼此對資料庫所造成的影響」，否則可能會出現 concurrency bugs。

==完美的 Isolation 應該做到的是：「多個被平行執行的 transactions 執行完後，資料庫的狀態 (state) 與 transactions 一個接著一個被執行的結果一樣。」==

常見的 Concurrency bugs 包含以下幾種：

- **Lost-Update Anomaly**
	
	舉例：
	
	兩個 transactions T1, T2 同時要讀取商品存貨數量，然後將商品存貨數量 -1，然後新增一筆訂單。假設原存貨數量為 100，T1, T2 都讀到 100，-1 後就都會是 99，所以商品存貨就會被更新為 99 兩次，然而，訂單卻多了兩筆，導致「商品存貨 + 訂單」的結果與原本不一致。
 ^9c95ff
- **Dirty-Write Anomaly**
	
	舉例：
	
	兩個 transactions T1, T2 同時要讀取商品存貨數量，然後將商品存貨數量 -1，然後新增一筆訂單。假設原存貨數量為 100，T1 已經讀取且率先將其更新為 99，準備新增訂單，此時 T2 才讀取存貨數量 (99)，並且將其更新為 98，然後準備新增訂單。然而此時 T1 因為新增訂單失敗而 rollback 回「對它而言的初始狀態」，所以存貨數量被改回 100，然後 T2 成功新增訂單。最終的結果是存貨不變 (100)，訂單卻多了一筆。

- **Dirty-Read Anomaly**
	
	舉例：
	
	一個 transaction T1 要將商品存貨 -1，然後新增一筆訂單，但執行到一半時（只將商品存貨 -1）另一個 transaction T2 來讀取商品存貨與訂單，目的是檢查「商品存貨 + 訂單」的總和是否有誤，此時 T2 得到的結論就是「有誤」，因為它看到的狀態是訂單還沒被建立前的狀態，即使不久後 T1 就建立了訂單。

- **Non-Repeatable Read Anomaly**
	
	舉例：
	
	有一個 transaction T1 來讀取存貨數量兩次，同時有另一個 transaction T2 正在執行，T2 包含讀取商品存貨數量、將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒 commit，但 T1 第二次讀取時，T2 已經 commit 了，此時 T1 讀取到的值就會不同。

- **Phantom Read Anomaly**
	
	舉例：
	
	有一個 transaction T1 來讀取所有訂單並計算數量兩次，同時有另一個 transaction T2 正在執行，T2 包含讀取商品存貨數量、將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒新增訂單，但 T1 第二次讀取時，T2 已經新增訂單，此時 T1 計算出來的數量就會不同。
	
	> Phantom Read Anomaly 與 Non-Repeatable Read Anomaly 的差別在於：後者是由「某些資料的某些欄位值被更改」所導致；前者則是由「新增或刪除某些資料」所導致。

- **Write Skew Anomaly**
	
	舉例：
	
	假設資料庫中商品表有以下 constraint：「售價必須高於成本 」，並且存在一個商品的售價為 10 元，成本為 8 元。此時有一個 transaction T1 會先讀取售價與成本，若成本 +1 元後仍然符合 constraint，就將成本 +1；同時有另一個 transaction T2 會先讀取售價與成本，若售價 -1 元後仍然符合 constraint，就將售價 -1，假設 T1 與 T2 讀到售價與成本皆為 (10, 8)，因此他們都會判斷可以對成本／售價進行更改，假設 T1 率先將成本 +1，此時 T2 將售價 -1 就會報錯。
	
	>Write Skew Anomaly 與 Lost-Update Anomaly 的差別在於：後者是兩個 transaction 更改同一筆資料的不同欄位 (disjoint set of data)；前者則是更改同一筆資料的同一個欄位 (overlapping set of data)。

SQL Standard 將 Isolation 由寬鬆到嚴格分為四種等級：

|Isolation Level|Dirty read|Non-repeatable read|Phantom Read|
|---|---|---|---|
|Read Uncommitted|✅ Possible|✅ Possible|✅ Possible|
|Read Committed|🚫 Not Possible|✅ Possible|✅ Possible|
|Repeatable Read|🚫 Not Possible|🚫 Not Possible|✅ Possible|
|Serializable|🚫 Not Possible|🚫 Not Possible|🚫 Not Possible|

由上表可見，SQL Standard 用來界定 Isolation level 的 anomalies 其實很少（都只與「讀取」相關），所以其實這些 level 間的界線是模糊的，且就算是最高階的 Serializable 也不是完美的 Isolation。

- **Read Uncommitted** (No Isolation)
	
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

---

### Basically Available

### Soft State

### Eventually Consistent

# 參考資料

---

https://en.wikipedia.org/wiki/CAP_theorem

https://www.youtube.com/watch?v=pomxJOFVcQs

https://phoenixnap.com/kb/acid-vs-base

https://fauna.com/blog/introduction-to-transaction-isolation-levels

https://stackoverflow.com/questions/4980801/how-simultaneous-queries-are-handled-in-a-mysql-database