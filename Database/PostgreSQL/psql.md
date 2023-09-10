psql 是 PostgreSQL 的 CLI。

# 進入 psql

```sh
psql <DB_NAME>

# 若沒有指定 db，就連到預設的 db:
psql
```

在 MacOS 中的 `~/.zprofile` 或 `~/.zshrc` 中加入 environment variable 可以設定預設要連到哪個 database，比如：

```bash
export PGDATABASE=postgres
```

這樣就會預設連到名為 `postgres` 的 database。

# Meta Commands

### `\q` 離開 psql

>[!Note]
>離開 psql 並不等於停止 PostgreSQL server，若要停止 server，請參考 [[Database/PostgreSQL/安裝與啟用#關閉背景執行的 PostgreSQL Server|這裡]]。

### `\l` 列出所有 Databases

### `\c` 連線至指定 Database

### `\df` 查看目前 Database 中有哪些可用的 Functions

### `\dt` 列出目前連線的 Database 的所有 Tables

### `\du` 列出所有 Database Roles (Users)

也可以使用 `SELECT * FROM pg_catalog.pg_user;` 達到類似的效果，但 `SELECT * FROM pg_catalog.pg_user;` output 的資訊更詳細，且就像操作一般 table 一樣可以做 `WHERE`、`ORDER BY`、`GROUP BY` 等操作。

這個指令與 `SELECT * FROM user;` 不同，`SELECT * FROM user;` 只會列出可以存取目前所連線的 DB 的 users。

### `\i <path/to/sql/file>` 執行 `.sql` 檔案

### `\x` 切換呈現結果的方式

Table 的呈現方式分為直式與橫式，當 table 欄位過多時適合切換為直式。

### `\?` 查看所有 Meta Commands

# 參考資料

- <https://www.postgresql.org/docs/current/app-psql.html>
