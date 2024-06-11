# SQL 的種類

SQL 依照功能可以分為 DML、DDL 與 DCL：

### DML

DML 是 Data "Manipulation" Language 的縮寫，包含 `SELECT`、`INSERT`、`DELETE` 與 `UPDATE` … 等（雖然其實 `SELECT` 與 manipulation 無關）。

>[!Note]
>完整介紹請見 [[DML]]。

### DDL

第二個 D for "Definition"，也就是與「定義」database schema 相關的 commands，如 `CREATE`、`ALTER`、`TRUNCATE` 與 `DROP` … 等。

>[!Note]
>完整介紹請見 [[DDL]]。

### DCL

C for "Control"，包含與 security, access control 相關的 commands，比如 `GRANT` 與 `REVOKE`。

# Functions

### Scalar Functions

>[!Note]
>完整介紹請見 [[Scalar Functions]]。

### Aggregate Functions

凡是經過運算一堆 tuples (rows) 後輸出一個值的 function，就叫做 aggregate function，簡稱 aggregates。

>[!Note]
>完整介紹請見 [[Aggregate Functions]]。

### Window Functions

Window functions 與 aggregate functions 有相似也有相異之處，相似之處在於，window functions 也是運算一堆 tuples；相異之處在於，aggregate functions 只會為每個分組結果 (`GROUP BY`) output 一個 tuple 或者一個 scalar，window functions 則是把運算的結果依照分組結果 (`PARTITION BY`) 附加在每一個 tuple 上。

>[!Note]
>完整介紹請見 [[Window Functions]]。

### Stored Function & Stored Procedure

就像其它程式語言一樣，我們也可以將常用的 SQL 打包成可重複利用的 function，只是 SQL 中的 function 有以下幾個特點：

- 可以細分為 function 與 procedure
- 會被存在 database 裡（所以叫做 stored function 跟 stored procedure）

>[!Note]
>完整介紹請見 [[Stored Function & Stored Procedure]]。

# String

### 字串在不同 RDBMS 中的差別

| **RDBMS** | **字串比對 (column value)** | **引號** |
| ---- | ---- | ---- |
| PostgreSQL | 可以比對大小寫| 只能用單引號 |
| MySQL | ==無法==比對大小寫 | 單雙皆可 |

### 模糊比對：`LIKE` 以及 Wildcard

**Wildcard: `%` & `_`**

字串模糊比對時，使用 `LIKE` operator 取代一般比對時的 `=`。並且使用 `%` 代表任意長度的任意字元；`_` 代表長度為 1 的任意字元。

e.g.

```SQL
SELECT * FROM student AS s WHERE name LIKE 'K%';
```

### String Functions

常用的 string functions 包括 `LOWER`、`UPPER`、`SUBSTRING`、`TRIM` … 等，另外還可以 `||` operator 串接兩個 strings。

String functions 是 input 一個 scalar，output 一個 scalar，因此不屬於 aggregate function。

# Output Redirection

將 `SELECT` 出來的東西存成一張「新的表」。

以 PostgreSQL 為例：

```SQL
SELECT DISTINCT(cid) INTO TABLE new_table FROM course;
```

也可以將 `SELECT` 出來的東西存進一張「已存在的表」。

以 PostgreSQL 為例：

```SQL
INSERT INTO old_table (
    SELECT DISTINCT(cid) FROM course
);
```

# Nested Queries

一個 query 語句的 `SELECT`、`FROM` 或 `WHERE` 子句中若含有另一個 query，這樣的結構就稱為 nested query，其中裡面的 query 稱為 subquery 或 inner query；外面的則稱為 outer query。

>[!Note]
>完整介紹請見 [[Nested Query]]。

# Common Table Expressions (CTE)

CTE 的全名是 Common Table Expression，功能與 nested query 類似，都是用來將某個 query 的 output 暫存在 memory，供 query 中的其他子句使用，且 CTE 與 nested query 都只有在執行「其所在的 query」的當下被暫存，無法供後續其他 queries 使用。

>[!Note]
>完整介紹請見 [[CTE]]。

# 參考資料

- <https://www.youtube.com/watch?v=6VCHuLqfmV8>
