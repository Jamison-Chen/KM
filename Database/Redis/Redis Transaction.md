Redis transaction 確保多個指令可以被一起執行不會被插隊，而因為 Redis is single-threaded，所以這樣一來就可以避免 race condition。

Redis transaction 與一般我們理解的 DB transaction 最大的不同在於：當一個 redis transaction 中有部分指令執行失敗時，並不會影響到後續指令的執行，也不會因此而 rollback。換句話說，==即使使用 redis transaction，也無法讓多個指令有 atomicity==。

與 transaction 相關的 Redis commands 包括 `MULTI`、`EXEC`、`DISCARD` 與 `WATCH`。

Example:

```plaintext
> MULTI
OK

> INCR foo
QUEUED

> INCR bar
QUEUED

> EXEC
1) (integer) 1
2) (integer) 1
```

所有指令會在 `EXEC` 時一次執行，也可以使用 `DISCARD` 捨棄一個尚未 `EXEC` 的 transaction，如此一來 `MULTI` 之後的所有指令都不會被執行而是會直接被捨棄。

### Optimistic Locking using `WATCH`

有時候我們除了希望多個指令間不要參雜著來自其它 client 的指令外，還會希望某個 value 在某個時間區間內都不要被改動，比如有一個 function 會先讀取 `mykey`，然後對 `mykey` 做一些與 Redis 無關的商業邏輯運算，最後要把新的值存進 `mykey`，這個 function 可能會希望 `mykey` 從一開始讀取到最後更新的這段期間都沒有被其它人更新過，此時就可以使用 `WATCH`：

```plaintext
> WATCH mykey
OK

// some computations

> MULTI
OK

> SET mykey $val
QUEUED

> EXEC
1) OK
```

`WATCH` 的功能並不是阻止其它 client 對特定的 key 更改，而是，如果被 watch 的 key 在過程中有被其它 non-transaction 的指令改到值，那後續的 transaction 如果再改那個 key 的值，整個 transaction 就會失敗，這種功能功能被稱為 **optimistic locking**。

舉個會失敗的例子：

```plaintext
> WATCH mykey
OK

> SET mykey 1
OK

> MULTI
OK

> SET mykey 2
QUEUED

> EXEC
(nil)

> GET mykey
"1"
```

在上面的例子中，因為在 `WATCH` 與 `MULTI` 之間有一個 non-transaction 的指令更改了 `mykey`，所以後續 transaction 並不會成功更改 `mykey`。

# 參考資料

- <https://redis.io/docs/latest/develop/interact/transactions/>
