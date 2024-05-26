Pagination 主要有三種實現方式，分別為：

1. [#Offset Pagination](</./Database/Pagination.md#Offset Pagination>)
2. [#Keyset Pagination](</./Database/Pagination.md#Keyset Pagination>)
3. [#Cursor-Based Pagination](</./Database/Pagination.md#Cursor-Based Pagination>)

# Offset Pagination

舉例：

```PostgreSQL
SELECT * FROM table_name
ORDER BY column_name
LIMIT 10
OFFSET 20;
```

### 注意事項

1. 為了讓每次分頁的結果都一樣，因此需要 `ORDER BY`
2. 為了讓排序更有效率，用來排序的 column 必須有 index

### 優點：可以跳到任意的分頁

只要給一個 `OFFSET` 的數字，就可以跳到指定的分頁。

### 缺點：效能瓶頸

以上方範例程式碼為例，雖然看似只 `select` 了 10 筆資料，但實際上是選了 30 筆資料然後把前面 20 筆丟掉。

# Keyset Pagination

舉例：

```PostgreSQL
SELECT * FROM table_name
WHERE key > 20
ORDER BY key
LIMIT 10;
```

### 注意事項

1. 作為分頁依據的 key **一定要**放在 `ORDER BY` 子句中，也因此，key 通常會有 index
2. Key 必須有 Unique Constraint

### 優點：處理大量資料時較有效率

Keyset Pagination 不像 Offset Pagination 會把 target page「前」的所有資料都先取出來然後丟掉。

### 缺點：不一定可以跳到任意的分頁

當 key 的值不可預測時，無法只能透過「上一頁」、「下一頁」的方式換頁。

### 含有其他排序規則的查詢

舉例：

（第一頁）

```PostgreSQL
SELECT * FROM book
ORDER BY price, id
LIMIT 10;
```

假設第一頁選出的資料中，最高的價格為 410，最大的 id (key) 為 629，那麼查下一頁的 query 就會變成：

```PostgreSQL
SELECT * FROM book
WHERE (price = 410 AND id > 629) OR (price > 410)
ORDER BY price, id
LIMIT 10;
```

1. 由於 `WHERE` 子句必須精確到有辦法讓第 n 頁與第 n+1 頁的資料沒有任何重疊，因此作為分頁依據的 key 仍然必須放在 `WHERE` 子句中
2. `ORDER BY` 子句中，key 一定還是要出現，只是順位一定在最後

# Cursor-Based Pagination

Cursor-Based Pagination 其實是 Keyset Pagination 的一種，只是 client side 不會知道 DBMS 具體用了哪個 column 作為分頁用的 key，原因是在 server side 會先將 key 進行編碼 (encode) 或加密 (encrypt)，才將它送給 client。

例如，假設 DBMS 在某張表上使用了 `id` 作為分頁用的 key，讀了第一頁後現在要以 `id > 29` 作為下一頁的開頭，於是有 `{"id": 29}` 這樣的資訊，而若將 `{"id": 29}` 經過 base64 編碼，會得到 `eyJpZCI6IDI5fQ==`，此時，server 可以給 client 以下資料：

```json
{
    "data": [...],
    "cursor": {
        "previous": null,
        "next": "eyJpZCI6IDI5fQ=="
    }
}
```

### 優點：Cursor 可以夾帶額外資訊

做「含有其他排序規則的查詢」時，可以將所有判斷條件一起編碼／加密，再拿 Keyset Pagination 段落中的例子舉例，在查詢第二頁時，就是將 `{"id": 629, "price": 410}` 編碼／加密。

### 缺點：無法跳到任意的分頁

由於 cursor 經過編碼或加密，一定無法預測，所以一定只能透過「上一頁」、「下一頁」的方式換頁。

# 參考資料

- <https://vladmihalcea.com/sql-seek-keyset-pagination/>
- <https://tec.xenby.com/36-%E9%BE%90%E5%A4%A7%E8%B3%87%E6%96%99%E5%BA%AB%E5%88%86%E9%A0%81%E6%96%B9%E6%A1%88-cursor-based-pagination>
