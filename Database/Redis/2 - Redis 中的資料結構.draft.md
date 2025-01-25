Redis 支援多種資料結構，相對地另一個有名的 in-memory database - Memcached 只支援 string。

# String

==Redis 中沒有 integer 和 float 這兩種資料型態==，所有數字都會被轉為 string。

e.g.

```plaintext
> set age 20
OK

> get age
"20"
```

# List

支援 left push、left pop、right push 與 right pop，所以可以實現 queue 和 stack 等 [ADT](</Data Structures & Algorithms/ADT.draft.md>)。

e.g.

```plaintext
> rpush names Alice Bob
(integer) 2

> lrange names 0 -1
1) "Bob"
2) "Alice"
```

# Hash

以 key-value pair 做為某個 key 的 value，但最多就這兩層，無法繼續將 hash 中的某個 key 的 value 設為 hash。

e.g.

```plaintext
> hset person name Alice
(integer) 1

> hget person name
"Alice"
```

# Set

e.g.

```plaintext
> sadd words 1 2 2
(integer) 2

> smembers words
1) "1"
2) "2"
```

# Sorted Set

#TODO

# Bit Array

# Hyper Log

# Stream

Redis stream 是 Redis 5.0 後新增的資料結構，行為像是一個 append-only log。

Stream 支援多種同的 consumption strategies，是一種適合用來當作 message queue 的資料結構。

### Basic Commands

- `XADD`
- `XREAD`
- `XRANGE`
- `XLEN`
