# SQL 分類

SQL 依照功能可以分為 DML、DDL 與 DCL：

### DML

^146eea

DML 是 Data "Manipulation" Language 的縮寫，包含 `SELECT`、`INSERT`、`DELETE` 與 `UPDATE` … 等（雖然其實 `SELECT` 與 manipulation 無關）。

詳見 [[DML]]。

### DDL

^08460a

第二個 D for "Definition"，也就是與「定義」Database Schema 相關的 commands，如 `CREATE`、`ALTER`、`TRUNCATE` 與 `DROP` … 等。

詳見 [[DDL]]。

### DCL

C for "Control"，包含與 security, access control 相關的 commands，比如 `GRANT` 與 `REVOKE`。

# Aggregate Functions

凡是經過運算一堆 tuples (rows) 後 output 一個 scalar 的 function，就叫做 Aggregate Function，簡稱 Aggregates。

詳見 [[Aggregate Functions]]。

# String

### 字串在不同 RDBMS 中的差別

| **RDBMS** | **字串比對 (column value)** | **引號** |
| ---- | ---- | ---- |
| PostgreSQL | 可以比對大小寫| 只能用單引號 |
| MySQL | ==無法==比對大小寫 | 單雙皆可 |

### 模糊比對：`LIKE` 以及 Wildcard

**Wildcard: `%` & `_`**

字串模糊比對時，使用 `LIKE` 取代一般比對時的 `=`。並且使用 `%` 代表任意長度、任意字元；`_` 則代表長度為 1 的任意字元。

e.g.

```PostgreSQL
SELECT * FROM student AS s WHERE name LIKE 'K%';
```

### String Functions

常用的 String Functions 包括 `LOWER`、`UPPER`、`SUBSTRING`、`TRIM` … 等，另外還可以 `||` operator 串接兩個 strings。

String Functions 是 input 一個 scalar，output 一個 scalar，因此不屬於 aggregate function。

# Output Redirection

將 `SELECT` 出來的東西存成一張「新的表」，以 PostgreSQL 為例：

```PostgreSQL
SELECT DISTINCT(cid) INTO TABLE new_table FROM course;
```

也可以將 `SELECT` 出來的東西存進一張「已存在的表」，以 PostgreSQL 為例：

```PostgreSQL
INSERT INTO old_table (
    SELECT DISTINCT(cid) FROM course
);
```

# Nested Queries

一個 query 語句的 `SELECT` 子句或 `WHERE` 子句中若含有另一個 query，這樣的結構就稱為 nested query。

詳見 [[Nested Query]]。

# Window Functions

Window functions 與 [[Aggregate Functions]] 有相似也有相異之處，相似之處在於，window functions 也是運算一堆 tuples；相異之處在於，aggregate functions 只會為每個分組結果 (`GROUP BY`) output 一個 tuple 或者一個 scalar，window functions 則是把運算的結果依照分組結果 (`PARTITION BY`) 附加在每一個 tuple 上。

詳見 [[Window Functions]]。

# Common Table Expressions (CTE)

#TODO 

詳見 [[CTE]]。

# 參考資料

- <https://www.youtube.com/watch?v=6VCHuLqfmV8&list=PLSE8ODhjZXjbohkNBWQs_otTrBTrjyohi>
