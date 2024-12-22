# On MacOS

### [官方文件](https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/)

### 安裝

```bash
brew install redis
```

>[!Note]
>執行這個指令時，若出現 `command not found: brew`，代表你的電腦中沒有沒有 Homebrew，此時你須要先[安裝 Homebrew](</Tools/Mac/Homebrew.md#安裝>)。

### 啟動 Redis Server 並在前景運行

```bash
redis-server
```

使用 `control` + `c` 關閉 server。

### 在背景執行 Redis Server

```bash
brew services start redis
```

### 關閉背景執行的 Redis Server

```bash
brew services stop redis
```

# On Linux Ubuntu

### 安裝

```bash
sudo apt-get update
sudo apt-get install redis
```

### 在背景執行 Redis Server

```bash
sudo systemctl start redis
```

### 關閉背景執行的 Redis Server

```bash
sudo systemctl stop redis
```

# Redis CLI

所有對 redis 的操作都可以在 Redis CLI 中透過指令來完成。

### Enter Redis CLI

```bash
redis-cli
```

### Quit Redis CLI

```bash
quit
```

也可以使用 `Control` + `C` 送出 [SIGINT](</Operating System/Unix Signal & IPC.md#Unix Signal>)。

# Redis Clients

除了直接使用 Redis CLI 外，Redis 官方也提供了各種程式語言（包括 Java、Go、Python、Node.js 與 C#）專用的 client libraries，詳見[官方文件](https://redis.io/docs/latest/develop/connect/clients/)。

### Python

##### 安裝

```bash
pip install redis
```

##### 連線

```Python
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
```

##### 操作

```Python
r.set('foo', 'bar')  # True
r.get('foo')
```
