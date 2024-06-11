為了避免 query 執行時間過長，可以設定「最長執行時間」。

# On PostgreSQL

### 設定

```SQL
SET statement_timeout = <TIME_OUT>;
```

其中 `<TIME_OUT>` 若為數字 0，則代表沒有時間上限，其它有效時間上限皆為 string，可用的單位包括 us (微秒)、ms (毫秒)、s (秒)、min (分)、h (小時) 以及 d (天)，舉例而言：

```SQL
SET statement_timeout = '1min';
```

### 查詢 `statement_timeout`

```SQL
SHOW statement_timeout;
```

# On MySQL

> [!Note]
> MySQL 的 timeout 只能限制 `SELECT` statements。

### 設定

```SQL
SET <SCOPE> MAX_EXECUTION_TIME=<MS>;
```

- `<SCOPE>` 代表此設定的有效的期間，可以為 keyword `GLOBAL`（直到下次更改前）或 keyword `SESSION`（僅本次連線 session）
- `<MS>` 的值須為一個整數，單位為 ms（毫秒）

e.g.

```SQL
SET GLOBAL MAX_EXECUTION_TIME=2000;
```

### 查詢 `MAX_EXECUTION_TIME`

```SQL
SHOW VARIABLES LIKE 'MAX_EXECUTION_TIME';
```
