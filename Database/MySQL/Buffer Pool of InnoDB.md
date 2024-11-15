>[!Info]
>本文假設你對 [[Caching.canvas|Caching]] 已經有基礎的認識。

MySQL 中的 [[Storage Engines.draft#InnoDB|InnoDB storage engine]] 會使用 main memory 將經常被存取的 table 與 index cache 住，這個 component 叫做 Buffer Pool。

### A List of Pages

Buffer pool 的結構是 "a linked list of pages"，一個 page 可以存若干個 rows，新增／移除 cache 的單位是 page，buffer pool 使用的 [[Cache Replacement Policy.canvas|replacement policy]] 是 ==LRU 的變體==，每當有新的 page 要被加入但空間不夠時，最久沒被使用的 page 就會被 evict。

可以把 buffer pool 二分為相對較常被存取的 "new sublist" 與相對較少被存取的 "old sublist"，new list 預設佔整個 buffer pool 的 5/8；old list 則佔 3/8，越靠近 old list 尾端的資料會越優先被 evict。下圖為 buffer pool 的結構：

![[mysql-innodb-buffer-pool-list.png]]

- 可以透過 MySQL 設定檔中的 `innodb_old_blocks_pct` 參數來設定 old sublist 的比例。
### Midpoint Insertion

從上面的圖可知，new sublist 的尾端與 old sublist 的開頭相接，這個相接地方叫做 midpoint，MySQL InnoDB 會將所有 table scan 的結果都存進 buffer pool 的 midpoint 這個位置（在 new sublist 的尾端）這個行為叫做 **midpoint insertion**。

採用 midpoint insertion 的好處是不會因為最新要存入 buffer pool 的資料很大就把 buffer pool 中所有既有的資料都 evict。

### 查看 Buffer Pool 的狀態

```SQL
SHOW ENGINE INNODB STATUS\G
```

- `\G` 的用途是讓 output 方便閱讀

在 output 中會找到一個叫 `BUFFER POOL AND MEMORY` 的區塊，內容會像這樣：

```plaintext
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 0
Dictionary memory allocated 509481
Buffer pool size   8191
Free buffers       7213
Database pages     978
Old database pages 381
Modified db pages  0
Pending reads      0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 0, not young 0
0.00 youngs/s, 0.00 non-youngs/s
Pages read 835, created 143, written 193
0.00 reads/s, 0.00 creates/s, 0.00 writes/s
No buffer pool page gets since the last printout
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
LRU len: 978, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
```

# 參考資料

- <https://dev.mysql.com/doc/refman/9.0/en/innodb-buffer-pool.html>
