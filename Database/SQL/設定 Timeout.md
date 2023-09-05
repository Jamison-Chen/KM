為了避免單一 Query 執行時間過長，可以設定「最長執行時間」。

### PostgreSQL

```PostgreSQL
SET statement_timeout = <TIME_OUT>;
```

其中 `<TIME_OUT>` 若為數字 0，則代表沒有時間上限，其他有效時間上線皆為 string，可用的單位包括 us (微秒), ms (毫秒), s, min, h, 以及 d (天)，舉例而言：

```PosgreSQL
SET statement_timeout = '1min';
```

###### 查詢 statement_timeout

```PostgreSQL
SHOW statement_timeout;
```

---

### MySQL

> [!Note]
> MySQL 的 timeout 只能限制 `SELECT` statements。

```MySQL
SET <SCOPE> MAX_EXECUTION_TIME=<MS>;
```

其中 `<SCOPE>` 代表此設定的有效的期間，可以為 `GLOBAL`（直到下次更改前）或 `SESSION`（僅本次連線 session）；`<MS>` 為一個整數，單位為 ms（毫秒）。

e.g.

```MySQL
SET GLOBAL MAX_EXECUTION_TIME=2000;
```
