當資料庫需要同時處理多個 transactions 時，就同時要面對 [Concurrency](</Database/Concurrency.md>) 的議題，本文將解釋 MVCC 以及 SS2PL 兩個常見的 [Concurrency Control Mechanisms](</Database/Concurrency.md#Concurrency Control Protocols>)。

# MVCC

MVCC 的全名是 multi-version concurrency control。

與此機制搭配的 Isolation Level 通常是 [Serializable](</Database/ACID vs. BASE.md#Isolation Level>)。

MVCC 讓資料庫中的每筆資料都可能有若干個版本，可以想像每一個 transaction 開始時都會對資料庫拍一張照，拍下來的照片會紀錄的是當下每筆資料的最新版本。

這張照片對 transaction 而言就是資料庫的初始狀態，一個 transaction T 所做的任何 read 與 write 動作都是對它的照片內容在動做，所以 T 在進行的過程中不會知道其它 transactions 對資料庫做了什麼，相對地，T commit 後，其它 transactions 已經在進行中（已經先拍好照）的 transactions 也不會知道，只有在 T commit 後才開始（拍照）的 transaction 才會知道 T 做了什麼。

若某個舊的版本的資料不再存在於任何 transaction 的照片的初始狀態中，該資料的該版本就應該被某種 [Garbage Collection](</Computer Science/Garbage Collection.md>) 機制徹底刪除（通常是使用 Stop-the-world process *aka 時間暫停之術*）。

前面使用「照片」來說明 MVCC 只是個比喻，實際 implement 的方法可以參考[這篇維基百科](https://en.wikipedia.org/wiki/Multiversion_concurrency_control#Implementation)。

# SS2PL

SS2PL 的全名是 strong strict two-phase locking，是一種結合 [Locking](</Database/Concurrency.md#🔓 Locking>) 與 [Commitment Ordering](</Database/Concurrency.md#Commitment Ordering>) 的 Concurrency Control Protocol，也是目前最廣泛被使用的 protocol。

### Two Phases

將一個 transaction 取得和釋出 locks 的時間完美切分為兩個階段：

- **Expanding Phase**

    在這個階段，transaction 只能取得 locks，不能釋出任何 lock。

- **Shrinking Phase**

    一旦 transaction 取得了所有它需要的 locks 後，就會進入這個階段，此階段中 transaction 只能釋出 locks，不能再取得新的 lock。

SS2PL 要求必須在 transaction commit 成功或 rollback 完成後，才可以開始釋放 locks，也就是說 Shrinking Phase 發生在 transaction 結束後。

在 Two-Phase Locking 中，與 "Strong Scrict" 相對的是 **"Conservative"** (C2PL)。SS2PL 允許在 trasaction 開始後再慢慢拿到所有 locks；C2PL 要求 transaction 在要先取得所有 locks 才能開始，也就是說 Expanding Phase 發生在 transaction 開始前，目的是為了避免 [Deadlocks](</Operating System/Deadlocks.md>) 發生。

# 參考資料

- <https://en.wikipedia.org/wiki/Multiversion_concurrency_control>
- <https://en.wikipedia.org/wiki/Two-phase_locking>
