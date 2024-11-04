Redis 支援多種資料結構，相對地另一個有名的 in-memory database - Memcached 只支援 string。

# String

Redis 中的資料型態不包含 integer 或 float，所有數字都會被轉為 string。

e.g.

```plaintext
127.0.0.1:6379> set age 20
OK
127.0.0.1:6379> get age
"20"
```

# List

支援 left push、left pop、right push 與 right pop，故可以實現 queue 和 stack 等 [ADT](</Data Structures & Algorithms/ADT.draft.md>)。

e.g.

```plaintext
127.0.0.1:6379> rpush names Alice Bob
(integer) 2
127.0.0.1:6379> lrange names 0 -1
1) "Bob"
2) "Alice"
127.0.0.1:6379>
```

# Hash

以 key-value pair 做為某個 key 的 value，但最多就這兩層，無法繼續將 hash 中的某個 key 的 value 設為 hash。

e.g.

```plaintext
127.0.0.1:6379> hset person name Alice
(integer) 1
127.0.0.1:6379> hget person name
"Alice"
```

# Set

e.g.

```plaintext
127.0.0.1:6379> sadd words 1 2 2
(integer) 2
127.0.0.1:6379> smembers words
1) "1"
2) "2"
127.0.0.1:6379>
```

# Sorted Set

#TODO

# Bit Array

# Hyper Log

# Stream
