psql 是 PostgreSQL 的 CLI。

# 進入 psql

```bash
psql {DB_NAME}

# 若沒有指定 {DB_NAME}，就會連到預設的 DB
psql
```

在 MacOS 中的 `~/.zprofile` 與 `~/.zshrc` 中加入 environment variable 可以設定預設要連到哪個 database，比如：

```bash
export PGDATABASE=hello
```

這樣就會預設連到名為 `hello` 的 database。

>[!Note]
>剛安裝 PostgreSQL 時，DBMS 中只會有一個 default user 叫 `postgres`，這個 user 的密碼為 `postgres`，另外也會有一個 default DB 叫 `postgres`。
>
>然而進入 psql 時，預設會使用 OS 的 username 作為登入 DBMS 的 username，比如你在 OS 中的 username 叫 `ubuntu`，那在輸入 `psql` 進入 psql 時，會嘗試登入名為 `ubuntu` 的 DB user，此時就會看到「User "ubuntu" 不存在」的錯誤訊息。
>
>解決方法是切換 OS 的 user 至 `postgres`：
>
>```bash
>sudo -u postgres psql
>```

# Meta Commands

### `\q` 離開 psql

>[!Note]
>離開 psql 並不等於停止 PostgreSQL server，若要停止 server，請參考[這裡](</Database/PostgreSQL/0 - Installation.md#關閉背景執行的 PostgreSQL Server>)。

### `\l` 列出所有 Databases

### `\c` 連線至指定 Database

### `\conninfo` 印出目前連線狀態

### `\df` 查看目前 Database 中有哪些可用的 Functions

### `\dt` 列出目前連線的 Database 的所有 Tables

### `\du` 列出所有 Database Roles (Users)

也可以使用 `SELECT * FROM pg_catalog.pg_user;` 達到類似的效果，但 `SELECT * FROM pg_catalog.pg_user;` 輸出的資訊更詳細，且就像操作一般 table 一樣可以做 `WHERE`、`ORDER BY`、`GROUP BY` 等操作。

這個指令與 `SELECT * FROM user;` 不同，`SELECT * FROM user;` 只會列出可以存取目前所連線的 DB 的 users。

### `\i {path/to/sql/file}` 執行 `.sql` 檔案

### `\x` 切換呈現結果的方式

Table 的呈現方式分為直式與橫式，當 table 欄位過多時適合切換為直式。

### `\?` 查看所有 Meta Commands

# 參考資料

- <https://www.postgresql.org/docs/current/app-psql.html>
