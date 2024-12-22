在 Redis 中，當我們有多個指令要執行時，可以選擇一個一個指令送出 (one-by-one) 或一次送出 (batch) 所有指令，其中一次送出所有指令這種技術在 Redis 中就稱為 **Pipeline**。

因為 Reids 採用的是 transport protocol 是 [[TCP.draft|TCP]]，所以每次建立連線的成本都很高（假設 Redis server 與 client 不在同一個 host 上），如果 client 在短時間內須要頻繁地操作 Redis，那 request/response 往返所需的 RTT (round-trip time) 就很有可能會成爲效能瓶頸，而 pipeline 的好處就是可以減少 RTT。

即使 client 與 server 在同一個 host 上，CPU 也須要花時間在 scheduling 上，當 client 送出指令時，把 CPU time 用在 client process 上；當 server 要接收、執行指令時，把 CPU time 分配到 server process 上，而 CPU scheduling 也須要花時間。

不僅如此，當多個指令分開送出時，Redis server 須要在執行每個指令時都發出一次 `read` 或 `write` [[System Call.draft|system call]]，而執行每個 system call 時 OS kernel 都要做一次 mode switch，kernel mode switch 是一項高成本且耗時的操作，由此可見 pipeline 的另一個好處就是減少 server 負擔。

下方為使用 Redis 原生指令並透過 Netcat 傳入 Redis server 的範例：

```bash
printf "PING\r\nPING\r\nPING\r\n" | nc localhost 6379
```

# Redis Pipeline 的特色

### 有順序

一個 pipeline 中的多個指令間是有順序的，且 server 的 output 順序會跟指令的順序一致。

### 沒有 Atomicity

雖然 Redis pipeline 中的指令是有順序的，但當其中的某個指令執行失敗時，並不會影響到其他指令的執行，一個 pipline 中可能有些指令執行成功、有些失敗，因此不適合將具有強烈前後相依性的指令放在同一個 pipeline 中。

### 無法防止 Race Condition

同一個 pipeline 中的多個指令雖然會被一起送至 Redis server 且有順序性，但這些指令實際被 server 執行時還是有可能會被「插隊」。

舉例來說，假設現在有兩個 pipelines (A, B) 幾乎同時抵達 Redis server，其中 A 包含指令 a1、a2、a3；B 包含指令 b1、b2、b3，則 server 實際執行指令的順序有可能是 a1 → a2 → b1 → b2 → a3 → b3。

插隊的現象有可能會導致 race condition，我們將上面的例子套用實際的 Redis command 來舉例：

```plaintext
// Pipeline A
val = GET mykey  // a1
val = val + 1    // a2
SET mykey $val   // a3

// Pipeline B
val = GET mykey  // b1
val = val + 1    // b2
SET mykey $val   // b3

// Execution Order: a1 -> a2 -> b1 -> b2 -> a3 -> b3
```

如果 `mykey` 的初始值是 0，那麼 a1 與 b1 都會讀到 0，而 a3 與 b3 就都會將 `mykey` 更新為 1。

由此可見 pipeline 並無法防止 race condition，要解決 race condition 的話須要用 [[Redis Transaction]]。

### Batch in, Batch out

若 client 使用 pipeline 一次將多個 commands 送出，則 server 也會把所有操作的 output 集中在一個 response 裡，server 會把執行完但還不能送出的 output 暫存在 memory 中，因此 ==client 也要注意不要一次把太多的 request 擠在同一個 pipeline，才不會造成 server OOM (out-of-memory)==。

# Pipeline in Python

基本用法：

```Python
import redis

r = redis.Redis(decode_responses=True)

# create a pipeline instance
pipe = r.pipeline()

# add commands to the pipeline
pipe.set("a", "a value")
pipe.set("b", "b value")
pipe.get("a")

# execute the pipeline
pipe.execute()
```

多個指令也可以 chain 起來：

```Python
pipe = r.pipeline()
pipe.set("a", "a value").set("b", "b value").get("a").execute()
```

使用 `transaction` 參數可以控制要不要把 pipeline 中的指令包成一個 transaction，`transaction` 預設為 `True`：

```Python
pipe = r.pipeline(transaction=False)
```

# 參考資料

- <https://redis.io/docs/latest/develop/use/pipelining/>
