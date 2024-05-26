使用 `SELECT … FOR UPDATE` 的時機，是當你需要「先撈出資料，花一點時間處理，然後才更新資料」時，==其目的是避免 [Concurrency Anomaly](</Database/Concurrency.md#Concurrency Anomalies>)==。

若有一個 transaction: T1，其中的 `SELECT` statement 後面有 `FOR UPDATE`，T1 就需要先取得 target table(s) 的 [Row Share Lock](</Database/Locks.md#Row Share Lock>) 以及 target row(s) 的 [FOR UPDATE Lock](</Database/Locks.md#FOR UPDATE Lock>) 才能成功執行該 statement，其中 row-level 的 `FOR UPDATE` Lock 發揮了「避免在 T1 處理資料的過程中有其他 transactions 對相同的 row(s) 進行 `UPDATE`, `DELETE`, 或 `SELECT … FOR UPDATE`」的功用。

反之，當同時有別的 transaction: T2 握有 `FOR UPDATE` Lock 時，若有 T1 要 `UPDATE`, `DELETE`, 或 `SELECT … FOR UPDATE`，就必須等到 T2 將 lock 釋出。

須特別注意的是，即使 `SELECT … FOR UPDATE` 中有 `WHERE` 只將想要的 rows 篩選出來，==若沒有使用到 [Index](</Database/Index.md>)（若觸發 full-table scan），那就需要**所有**即將被 scan 的 rows 的 `FOR UPDATE` Lock==。

### `NOWAIT`

有時候一個 transaction 可能不想等待，希望若 `SELECT FOR UPDATE` 的 target rows 已經被 lock 就直接跳 error 並 rollback，那方法是 `SELECT … FOR UPDATE NOWAIT`。

### `SKIP LOCKED`

有時候一個 transaction 可能會想要在「不等待」的情況下，只 `SELECT FOR UPDATE` 某 table 中尚未被 lock 的 rows，則方法是 `SELECT … FOR UPDATE SKIP LOCKED`。

### 對 Foreign Key 的影響

已知 table: T1 中的某個 column 為 foreign key（reference 到 table: T2 的 Primary Key），若某 transaction 握有 T1 的 row: R1 的 `FOR UPDATE` Lock，則 R1 的 Foreign Key 所對應到的 T2 的 row: R2 也會被加上一個 lock。但 R2 上的 lock 只是 [FOR KEY SHARE Lock](</Database/Locks.md#FOR KEY SHARE Lock>)，也就是說此時 R2 只是不能被刪除，至於修改，除了被 T1 reference 的 column (Primary Key) 不能改以外，其它 columns 還是可以被其他 transactions 更改。

# 參考資料

- <https://www.cockroachlabs.com/blog/select-for-update/>
