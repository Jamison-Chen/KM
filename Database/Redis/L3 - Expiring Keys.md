「將不必要／過時的資料移除」這個動作之所以重要的主要原因有二：

- Redis 是 in-memory database，而 memory 相對較貴的資源，不應該留一堆沒有在存取的資料在 memory 裡面
- Redis 被用來實現 caching mechanism，而在某些 [cache writing policy](</System Design/Caching.canvas>) 中可能會出現某些資料過於老舊的現象

# 設置資料的有效期限

- 使用 `expire <key> <seconds>` 為一個已存在的 key 設定有效期限：

    ```plaintext
    127.0.0.1:6379> expire age 120
    (integer) 1
    ```

    回傳 `(integer) 1` 代表設置成功。

- 使用 `setex <key> <second> <value>` 設置一個具有有效期限的新 key-value pair：

    ```plaintext
    127.0.0.1:6379> setex age 120 20
    OK
    ```

# 查詢資料再多久過期

使用 `ttl <key>` 查詢再多久過期：

```plaintext
127.0.0.1:6379> ttl age
(integer) 114
127.0.0.1:6379> ttl age
(integer) -2
```

回傳 `(integer) -2` 代表該 key 已過期。

# 可以為 Hash 中的特定 Field 設置有效期限嗎？

#TODO 
