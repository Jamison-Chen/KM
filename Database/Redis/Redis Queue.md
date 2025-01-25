Redis 的 [[2 - Redis 中的資料結構.draft|list 與 set 資料結構]]可以用來實作 [[Message-Queuing System|message queue]]，在 Redis 5.0 後還多的 stream 這種專門用來當作 message queue 的資料結構。

# 以 List 實作最基本的 Message Queue

### Enqueue

```plaintext
LPUSH {QUEUE_NAME} {TASK}
```

若指定的 `{QUEUE_NAME}` 本來不存在，則會自動先建立 list 再 push。

### Dequeue

```plaintext
RPOP {QUEUE_NAME}
```

若指定的 `{QUEUE_NAME}` 裡沒有東西，則會回傳 `(nil)`。

### Peek

```plaintext
LRANGE {QUEUE_NAME} {START_IDX} {STOP_IDX}
```

`{START_IDX}`/`{STOP_IDX}` 若大於等於 0，是從 list 的左邊 (head) 開始數起，也可以是負數，代表從右邊 (tail) 數起。

# Reliable Queue

在一個基本的 Redis queue 中，若 consumer 在 dequeue 某個 task 後、處理完該 task 前 crash 了，則即使之後重啟 consumer，那個 task 也不會被重新處理，因此我們須要 reliable queue 來避免這種情況發生。

Reliable queue 的概念是：除了主要的 message queue (main queue) 外，還有一個 temporary queue，當 consumer 認領了某個 task 後，該 task 會從 main queue 中被移除，同時被放進 temporary queue，當 consumer 確定處理完該 task 後，再將 task 從 temporary queue 中移除。如此一來即使 task 處理到一半 consumer crash 了，只要將 temporary queue 中的 task 放回 main queue 即可。

### 實作

使用 `RPOPLPUSH` 將 task 從 main queue 移到 temporary queue：

```plaintext
RPOPLPUSH {MAIN_QUEUE} {TEMP_QUEUE}
```

Consumer 處理完 task 後，使用 `LREM` 將 task 從 queue 中移除：

```plaintext
LREM {TEMP_QUEUE} 1 {TASK}
```

之所以是使用 `LREM` 而不是 `RPOP`，是因為我們假設有不只一個 consumer，而每個 task 所需的時間都不同，所以有可能比較晚被認領的 task 卻比較早被完成，換句話說，tail task 不一定是最先被處理完的。

# Blocking Queue

#TODO 

# Delayed Tasks

# Priority Queue

# 參考資料

- <https://redis.io/glossary/redis-queue/>
