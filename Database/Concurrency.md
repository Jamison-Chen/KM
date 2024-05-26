Concurrency 意即「同時進行」，在資料庫中指的就是同時在進行的若干個 transactions。其實不只在資料庫領域，在 operating system 以及所有支援 multi-threading 或 multi-processing 的程式語言中，concurrency 都是重要的議題，因為有些時候，看似沒有問題的系統／程式面臨 concurrency 時，就會開始出現讓人無法預測的錯誤。

# Concurrency Anomalies

Concurrency anomalies 指的就是發生在資料庫的 race condition，包含以下六種：

- [Dirty Read](<#Dirty Read>)
- [Non-Repeatable Read](<#Non-Repeatable Read>)
- [Phantom Read](<#Phantom Read>)
- [Dirty Write](<#Dirty Write>)
- [Lost Update](<#Lost Update>)
- [Write Skew](<#Write Skew>)

### Dirty Read

e.g.

一個 [transaction](</Database/淺談 Database.md#Database Transaction>) T1 要將商品存貨 -1，然後新增一筆訂單，但執行到一半時（只將商品存貨 -1）另一個 transaction T2 來讀取商品存貨與訂單，目的是檢查「商品存貨 + 訂單」的總和是否有誤。

此時 T2 得到的結論就是「有誤」，因為它看到的狀態是訂單還沒被建立前的狀態，即使不久後 T1 就建立了訂單。

### Non-Repeatable Read

e.g.

有一個 transaction T1 會先後讀取存貨數量兩次，同時有另一個 transaction T2 正在執行，T2 會將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒 commit，但 T1 第二次讀取時，T2 已經 commit 了，此時 T1 讀取到的存貨數量就會比第一次少一個。

### Phantom Read

e.g.

有一個 transaction T1 來讀取所有訂單並計算數量兩次，同時有另一個 transaction T2 正在執行，T2 會將商品存貨數量 -1、新增一筆訂單。T1 第一次讀取時，T2 還沒 commit，但 T1 第二次讀取時，T2 已經新增訂單並 commit，此時 T1 計算出來的訂單數量就會比第一次多一個。

>[!Note]
>Non-Repeatable Read 是由「某些資料的某些欄位值被更改」所導致；Phantom Read 則是由「新增或刪除某些資料」所導致。

### Dirty Write

Dirty write 包含以下兩種現象：

- Transactions 進行 rollback 時，只會將資料狀態退回「對 transaction 自己而言」的原始狀態，這會導致過程中的其它 transactions 對這些資料做的更動都被抹除
- Transaction 在 rollback 前，若有其它 transactions 讀到還沒 rollback 的「髒資料」，就有可能因此做出最後看起來錯誤的決策

e.g. (1)

兩個 transactions T1, T2 都是要「先讀取商品存貨數量、將商品存貨數量 -1，最後新增一筆訂單」。假設原存貨數量為 100，T1 已經讀取且率先將其更新為 99，準備新增訂單，此時 T2 才讀取存貨數量 (99)，並且將其更新為 98，然後準備新增訂單。然而此時 T1 因為新增訂單失敗而 rollback 回「對它 (T1) 而言的原始狀態」，所以存貨數量被改回 100，然後 T2 成功新增訂單。最終的結果是存貨不變 (100)，訂單卻多了一筆。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/dirty_write.png>)

e.g. (2)

某商品的存貨剩 1 件，現在有兩個 transactions T1, T2，都是要「先讀取商品存貨數量、將商品存貨數量 -1，最後新增一筆訂單」。假設 T1 先讀取並將商品存貨數量 -1，然後 T2 才讀取存貨數量，此時因為存貨為 0，T2 判斷不能下訂單，因此告訴消費者商品售罄，接著 T1 因為新增訂單時出錯所以 rollback（將商品庫存改回 1），於是消費者就來抱怨為什麼明明看到庫存剩 1 卻被告知商品售罄。

### Lost Update

若同時有若干個 transactions 要更改同一個 row，則該筆資料最終的狀態是由最晚 commit 者決定。

e.g.

兩個 transactions T1, T2 同時要讀取商品存貨數量、將商品存貨數量 -1，然後新增一筆訂單。假設原存貨數量為 100，T1, T2 都讀到 100，-1 後就都會是 99，所以商品存貨就會被更新為 99 兩次，然而訂單卻多了兩筆，導致「商品存貨 + 訂單」的結果與原本不一致。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/lost_update.png>)

### Write Skew

Write Skew 與 Lost Update 類似，但 lost update 關注的是兩個 transactions 更改同一筆資料的同一個欄位，進而引發的「資料覆寫」問題；write skew 則關注在因讀到過時資料而造成的「錯誤決定」。

e.g.

某商品的存貨剩 1 件，現在有兩個 transactions T1, T2，都是要「先讀取商品存貨數量、將商品存貨數量 -1，最後新增一筆訂單」。若 T1 與 T2 都讀到剩 1 件存貨，因此都覺得存貨還夠就建立了訂單，那麼賣家就會頭很痛。（其實這隱含了 lost update，T1 與 T2 都將存貨數量改為 0）

# Concurrency Control Protocols

### 分類

- 積極型

    不多做檢查，不管有多少平行的 transactions 都直接執行，如果有誰 commit 時出錯了，就 rollback 那些出錯的 transactions 並 retry，直到成功為止。

- 消極型

    執行 transaction 中的每個步驟時都先檢查這個動作會不會破壞 [Integrity Constraint](</Database/Integrity Constraint.md>)，如果會就把該 transaction block 住，等危機解除後再放行。

    由於消極型的 protocols 容易導致 [Deadlocks](</Operating System/Deadlocks.md>)，因此多數 DBMS 都有與防機制，比如定期將被 block 過久的 transaction 做 rollback & retry。

### 手段

##### 🔓 Locking

當一個 transaction T 存取資料時，將這些被存取的資料加上 [Locks](</Database/Locks.md>)，被加上 lock 的資料將無法被其它 transaction 存取或做某些操作（視 lock 的種類而定），直到 T commit 後才將 lock 解除。

##### Serialization Graph Checking

將 concurrent transactions 轉換成與其「等價」（最後會產生相同資料庫狀態）的 serialized schedual，若將這個 schedual 視覺化為流程圖，則圖裡應不能出現任何「循環」，若出現則應以「最小成本」將造成循環的 transaction(s) 拔除。

去除循環後，並不一定要真的按照 serialized schedual 一個接著一個執行，仍可以選擇同時執行沒有被去除的 transactions。

##### Timestamp Ordering

將 concurrent transactions 轉換成與其「等價」（最後會產生相同資料庫狀態）的 serialized schedual，並確實依序執行。將每個 transaction 標記一個唯一的 timestamp，用來決定執行順序。

##### Commitment Ordering

將每個 transaction 標記一個唯一的 timestamp，用來決定「commit 的順序」，並且確保下面兩件事：

- Commitment order 較早的 transaction 不會受到 commitment order 比自己晚的 transactions 影響

- Commitment order 較晚的 transaction 可以存取到比自己早 commit 的 transactions 對資料庫所做的變動

>[!Note]
>上述這些手段並非只能擇一，可以搭配使用。

### 主流做法

- [[MVCC vs. SS2PL#MVCC|MVCC (Multi-Version Concurrency Control)]]
- [[MVCC vs. SS2PL#SS2PL|SS2PL (Strong-Strict Two-Phase Locking)]]

# 參考資料

- <https://en.wikipedia.org/wiki/Concurrent_computing>
- <https://en.wikipedia.org/wiki/Concurrency_control>
