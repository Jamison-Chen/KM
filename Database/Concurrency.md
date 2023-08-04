其實不只在 Database 的領域，在 Operating System 與程式語言的領域中，Concurrency 都是重要的議題。

# Concurrency Anomalies

可以簡單地將 Concurrency Anomalies 理解為資料庫世界裡的 Race Condition。Concurrency Anomalies 包含以下六種：

- [Dirty Read](<#Dirty Read>)
- [Non-Repeatable Read](<#Non-Repeatable Read>)
- [Phantom Read](<#Phantom Read>)
- [Lost Update](<#Lost Update>)
- [Dirty Write](<#Dirty Write>)
- [Write Skew](<#Write Skew>)

### Dirty Read

舉例：

一個 transaction T1 要將商品存貨 -1，然後新增一筆訂單，但執行到一半時（只將商品存貨 -1）另一個 transaction T2 來讀取商品存貨與訂單，目的是檢查「商品存貨 + 訂單」的總和是否有誤，此時 T2 得到的結論就是「有誤」，因為它看到的狀態是訂單還沒被建立前的狀態，即使不久後 T1 就建立了訂單。

### Non-Repeatable Read

舉例：

有一個 transaction T1 來讀取存貨數量兩次，同時有另一個 transaction T2 正在執行，T2 包含讀取商品存貨數量、將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒 commit，但 T1 第二次讀取時，T2 已經 commit 了，此時 T1 讀取到的存貨數量就會比第一次少一個。

### Phantom Read

舉例：

有一個 transaction T1 來讀取所有訂單並計算數量兩次，同時有另一個 transaction T2 正在執行，T2 包含讀取商品存貨數量、將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒新增訂單，但 T1 第二次讀取時，T2 已經新增訂單，此時 T1 計算出來的訂單數量就會比第一次多一個。

>Non-Repeatable Read Anomaly 是由「某些資料的某些欄位值被更改」所導致；Phantom Read Anomaly 則是由「新增或刪除某些資料」所導致。

### Lost Update

若兩個以上的 transactions 同時要更改同一筆資料，該筆資料最終的狀態是由最晚 commit 的 transaction 決定。

舉例：

兩個 transactions T1, T2 同時要讀取商品存貨數量，然後將商品存貨數量 -1，然後新增一筆訂單。假設原存貨數量為 100，T1, T2 都讀到 100，-1 後就都會是 99，所以商品存貨就會被更新為 99 兩次，然而，訂單卻多了兩筆，導致「商品存貨 + 訂單」的結果與原本不一致。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/lost_update.png>)

### Dirty Write

每個 Transactions 間是獨立的，執行 rollback 的 transaction 不會知道在自己這個 transaction 的過程中是否有其他 transaction 對同樣的資料做更動，所以只會 rollback 回「對自己而言」的原始狀態，這會導致過程中的其它 transactions 對這些資料做的更動都被抹除。

舉例：

兩個 transactions T1, T2 都是要「先讀取商品存貨數量，然後將商品存貨數量 -1，最後新增一筆訂單」。假設原存貨數量為 100，T1 已經讀取且率先將其更新為 99，準備新增訂單，此時 T2 才讀取存貨數量 (99)，並且將其更新為 98，然後準備新增訂單。然而此時 T1 因為新增訂單失敗而 rollback 回「對它 (T1) 而言的原始狀態」，所以存貨數量被改回 100，然後 T2 成功新增訂單。最終的結果是存貨不變 (100)，訂單卻多了一筆。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/dirty_write.png>)

### Write Skew

現在有多個同時進行進行的 transactions，有可能它們「個別」來看都符合資料庫 schema 的 constraints，但綜合起來後就不符合了。

由於這些 transactions 間是獨立的，不知道與自己同時在進行的 transactions 有哪些以及會做哪些事，所以 Write Skew Anomaly 較難偵測及預防。

舉例：

假設資料庫中**商品** relation 有「售價必須高於成本 」這個 constraint，現在有一個商品的售價為 10 元，成本為 8 元，此時有一個 transaction T1 會先讀取售價與成本，若成本 += 1 元後仍然符合 constraint，就將成本 += 1；同時有另一個 transaction T2 一樣先讀取售價與成本，若售價 -= 1 元後仍然符合 constraint，就將售價 -= 1，若 T1 與 T2 讀到的 `(售價, 成本)` 皆為 `(10, 8)`，他們就都會判斷可以對成本／售價進行更改，然而，若 T1 率先將成本 += 1 且 commit，此時 T2 再將售價 -= 1 就會因不符合 constraint 而無法 commit。

>Lost-Update Anomaly 是兩個 transactions 更改同一筆資料的不同欄位 (disjoint set of data)；Write Skew Anomaly 則是更改同一筆資料的同一個欄位 (overlapping set of data)。

# Concurrency Control Protocols

### 分類

###### 積極型

不多做檢查，不管有多少平行的 transactions 都直接執行，如果有誰 commit 時出錯了，就 rollback 那些出錯的 transactions 並 re-execute，直到成功為止。

###### 消極型

執行 transaction 中的每個步驟時都先檢查這個動作會不會破壞 [[Integrity Constraint]]，如果會的話就把該 transaction block 住，等危機解除後再放行。

由於消極型的 protocols 容易導致 [[Deadlocks (死結)]]，因此多數 DBMS 都有與防機制，比如定期將被 block 過久的 transaction 做 rollback and re-execute。

### 手段

###### 🔓 Locking

當一個 transaction T 存取資料時，將這些被存取的資料加上 locks，被加上 lock 的資料將無法被其它 transaction 存取或做某些操作（視 lock 的種類而定），直到 T commit 後才將 lock 解除。

###### Serialization Graph Checking

將平行執行的 transactions 轉換成與其「等價」（最後會產生相同資料庫狀態）的 serialized schedual，若將這個 schedual 視覺化為流程圖，則圖裡應不能出現任何「循環」，若出現則應以「最小成本」將造成循環的 transaction(s) 拔除。

但去除循環後，並不一定要真的按照 serialized schedual 一個接著一個執行，仍可以選擇同時執行。

###### Timestamp Ordering

將平行執行的 transactions 轉換成與其「等價」（最後會產生相同資料庫狀態）的 serialized schedual，並確實依序執行。將每個 transaction 標記一個唯一的 timestamp，用來決定執行順序。

###### Commitment Ordering

將每個 transaction 標記一個唯一的 timestamp，用來決定「commit 的順序」，並且確保下面兩件事：

- 較早執行 commitment 的 transaction 不會受到 commitment order 比自己晚的 transactions 影響

- 較晚執行 commitment 的 transaction 可以存取到比自己早 commit 的 transactions 對資料庫所做的變動

>[!Note]
>上述這些手段並非只能擇一，可以搭配使用。

### 主流做法

- [[MVCC vs. SS2PL#MVCC|MVCC (Multi-Version Concurrency Control)]]
- [[MVCC vs. SS2PL#SS2PL|SS2PL (Strong-Strict Two-Phase Locking)]]

# 參考資料

- <https://en.wikipedia.org/wiki/Concurrent_computing>
- <https://en.wikipedia.org/wiki/Concurrency_control>
