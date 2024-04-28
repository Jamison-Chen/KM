# 特色

```mermaid
flowchart TD
    id1(Key-Value Model)
    id2(In-Memory Dataset)
    id3(IO Multiplexing)
    id4(Single-Threaded)
```

### Key-Value Model

Redis 屬於 NoSQL (non-relational database)。

### In-Memory Dataset

##### 優點：存取的 latency 低、throughput 高

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/computer-memory-hierarchy-and-price.png>)

##### 缺點

- Volatile，不適合作為 single source of truth (SSoT)
- 由於價格因素，RAM 的大小通常比 disk 小很多，不能存太多資料

##### BASE Model

綜合上面的優缺點可知對於 Redis 來說，[[CAP Theorem|availability 比 consistency 重要]]，所以 Redis 屬於 [[ACID vs. BASE#BASE|BASE Model]]。

### IO Multiplexing & Single-Threaded Read/Write

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/redis-io-multiplexing-single-threaded.png>)

- 只有一個 thread 就不需要 [[Locks]] 或其他解決 synchronization problem 的手段
- 只有一個 thread，所以沒有 [[Concurrency]] 問題，比較好 debug
- 只有一個 thread，所以即使 server 有很多 CPUs 也只能利用其中一個（有些人會因為這樣就在一個 server 上架多個 Redis instances）
# Redis 中的資料型態

### String

#TODO 

### List

支援 left push、left pop、right push 與 right pop，故可以實現 queue 和 stack 等 [[ADT]]。

e.g.

```plaintext
127.0.0.1:6379> rpush names Alice Bob
(integer) 2
127.0.0.1:6379> lrange names 0 -1
1) "Bob"
2) "Alice"
127.0.0.1:6379>
```

### Hash

以 key-value pair 做為某個 key 的 value，但最多就這兩層，無法繼續將 hash 中的某個 key 的 value 設為 hash。

e.g.

```plaintext
127.0.0.1:6379> hset person name Alice
(integer) 1
127.0.0.1:6379> hget person name
"Alice"
```

### Set

e.g.

```plaintext
127.0.0.1:6379> sadd words 1 2 2
(integer) 2
127.0.0.1:6379> smembers words
1) "1"
2) "2"
127.0.0.1:6379>
```

### Sorted Set

#TODO 

>[!Note]
>Redis 中的資料型態不包含 integer 或 float，所有數字都會被轉為 string。
>
>e.g.
>
>```plaintext
>127.0.0.1:6379> set age 20
>OK
>127.0.0.1:6379> get age
>"20"
>127.0.0.1:6379>
>```

# 如何避免 Data Loss？

### Persistence Options

[官方文件](https://redis.io/docs/management/persistence/)

Redis 有提供一些機制避免 server restart 所造成的 data loss，包含：

- **Redis Database (RDB)**

    每隔一段時間拍一張 snapshot，server restart 後把 snapshot 的資料復原。

- **Append-Only File (AOF)**

    把每一個 operation 記錄成 log file，server restart 後把所有 operations 依序執行一次。

通常在 server restart 後須要花很多時間來重新建置資料，所以實務上較少使用 persistence options，比較常用的是 replication。
### Replication

#TODO 

# 基本操作

### 設置資料的有效期限

使用 `expire <key> <seconds>` 為一個已存在的 key 設定有效期限：

```plaintext
127.0.0.1:6379> expire age 120
(integer) 1
127.0.0.1:6379>
```

回傳 `(integer) 1` 代表設置成功。

---

使用 `ttl <key>` 查詢再多久過期：

```plaintext
127.0.0.1:6379> ttl age
(integer) 114
127.0.0.1:6379> ttl age
(integer) -2
```

回傳 `(integer) -2` 代表該 key 已過期。

---

使用 `setex <key> <second> <value>` 設置一個具有有效期限的新 key-value pair：

```plaintext
127.0.0.1:6379> setex age 120 21
OK
127.0.0.1:6379>
```

# 官方文件

<https://redis.io/docs/>

# 參考資料

- <https://blog.techbridge.cc/2016/06/18/redis-introduction/>
- <https://www.youtube.com/watch?v=jgpVdJB2sKQ>
- <https://www.youtube.com/watch?v=nH4qjmP2KEE>
- <https://www.youtube.com/watch?v=a4yX7RUgTxI>
