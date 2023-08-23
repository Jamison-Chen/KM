# 特色

```mermaid
flowchart TD
    id1(Key-Value Model)
    id2(In-Memory Dataset)
    id3(BASE Model)
```

### Key-Value Model

Redis 屬於 NoSQL。

### In-Memory Dataset

- 優點：存取速度快
- 缺點：Volatile，不適合作為 single source of truth (SSoT)

### BASE Model

對於 Redis 來說，[[CAP Theorem|availability 比 consistency 重要]]，故屬於 [[ACID vs. BASE#BASE|BASE Model]]。

# Redis 中的資料型態

### String

#TODO 

### List

支援 "left push"、"left pop"、"right push" 與 "right pop"，故可以實現 queue 和 stack 等 [[常見的資料結構與 ADT#ADT|ADT]]。

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

# 參考資料

- <https://redis.io/docs/>
- <https://blog.techbridge.cc/2016/06/18/redis-introduction/>
- <https://www.youtube.com/watch?v=jgpVdJB2sKQ>
