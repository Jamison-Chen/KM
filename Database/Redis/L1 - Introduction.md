# Redis 的特色

Redis 是一個將資料存在 memory 的 database，由於存在 memory 的資料可以被快速存取，所以這類型的 database 被廣泛應用在 server side，用來實作 [[Caching.canvas|cache mechanism]]。Redis 包含以下特色：

```mermaid
flowchart TD
    id1(In-Memory)
    id2(Key-Value Model)
    id3(I/O Multiplexing)
    id4(Single-Threaded Read/Write)
```

### In-Memory

##### Pros: Low latency, hight throughput

In-memory database 的存取速度是 disk-base memory 的 1000 倍以上。

![[computer-memory-hierarchy-and-price.png]]

##### Cons

- Volatile，不適合作為 SSoT (single source of truth)
- 由於價格因素，memory 的大小通常比 disk 小很多，不能存太多資料

##### BASE Model

綜合上面的優缺點可知對於 Redis 來說 [[CAP Theorem|availability 比 consistency 重要]]，所以 Redis 屬於 [[ACID vs. BASE#BASE|BASE model]]。

### Key-Value Model

Redis 屬於 NoSQL (non-relational database)。

### IO Multiplexing & Single-Threaded Read/Write

![[redis-io-multiplexing-single-threaded.png]]

- 只有一個 thread 就不需要 [[Locks]] 或其他解決 synchronization problem 的手段
- 只有一個 thread，所以沒有 [[Concurrency]] 問題，比較好 debug
- 只有一個 thread，所以即使 server 有很多 CPUs 也只能利用其中一個（這也意味著一個 server 上有辦法架設多個 Redis instances）

# Redis 如何避免資料遺失？

主要有 persistence options 與 replication 兩種作法：

### Persistence Options

[官方文件](https://redis.io/docs/management/persistence/)

Redis 有提供一些機制避免 server restart 所造成的資料遺失，包含：

- **Redis Database (RDB)**

    每隔一段時間拍一張 snapshot，server restart 後把 snapshot 的資料復原。

- **Append-Only File (AOF)**

    把每一個 operation 記錄成 log file，server restart 後把所有 operations 依序執行一次。

通常在 server restart 後須要花很多時間來重新建置資料，所以實務上較少使用 persistence options，比較常用的是 replication。
### Replication

#TODO 

# 官方文件

<https://redis.io/docs/>

# 參考資料

- <https://blog.techbridge.cc/2016/06/18/redis-introduction/>
- <https://www.youtube.com/watch?v=jgpVdJB2sKQ>
- <https://www.youtube.com/watch?v=nH4qjmP2KEE>
- <https://www.youtube.com/watch?v=a4yX7RUgTxI>
