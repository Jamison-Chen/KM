在 Redis 中，當我們有多個指令要執行時，可以選擇一個一個指令送出 (one-by-one) 或一次送出 (batch) 所有指令，其中一次送出所有指令這種技術在 Redis 中就稱為 **Pipelining**。

因為 Reids 採用的是 transport protocol 是 [[TCP.draft|TCP]]，所以每次建立連線的成本都很高，如果使用者在短時間內須要頻繁地操作 Redis，那 RTT (round-trip time) 就很有可能會成爲效能瓶頸，而 pipelining 的好處就是可以減少 request/response 往返所需的 RTT。

一個 pipeline 中的 commands 是有順序的，且 server 的 output 順序會跟 commands 的順序一致。

若 client 使用 pipelining 一次將多個 commands 送出，則 server 也會把所有操作的 output 集中在一個 response 裡，server 會把執行完但還不能送出的 output 暫存在 memory 中，因此 ==client 也要注意不要一次把太多的 request 都擠在同一個 pipeline，才不會造成 server OOM (out-of-memory)==。

# 參考資料

- <https://redis.io/docs/latest/develop/use/pipelining/>
