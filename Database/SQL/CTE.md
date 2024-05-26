CTE 的全名是 Common Table Expression，功能與 [Nested Query](</Database/SQL/Nested Query.md>) 類似，都是用來將某個 query 的 output 暫存在 memory，供 query 中的其他子句使用，且 CTE 與 nested query 都只有在執行「其所在的 query」的當下被暫存，無法供後續其他 queries 使用。

一個基本的 CTE 會長得像這樣：

```SQL
WITH my_cte AS (
    SELECT …
    …
)
SELECT * FROM my_cte
…
```

上方範例中，`my_cte` 為 CTE 的名字，你可以想像他是一個「暫時」的 table name。

### 定義 CTE 中的 Column Name

e.g.

```SQL
WITH my_cte (time, score) AS (
    SELECT …
    …
)
SELECT time, score FROM my_cte
…
```

### 在一個 Query 中定義多個 CTEs

e.g.

```SQL
WITH temp1 AS (
    …
),
temp2 AS (
    …
)
SELECT * FROM temp1, temp2;
```

### Nested CTE

可以在 CTE 中出現其他 CTE，比如：

```SQL
WITH temp1 AS (
    …
),
temp2 AS (
    SELECT … FROM temp1
    …
)
SELECT * FROM temp1, temp2;
```

也可以在 CTE 中定義 CTE，比如：

```SQL
WITH temp1 AS (
    …
),
temp2 AS (
    WITH temp3 AS (
        …
    )
    SELECT … FROM temp1, temp3
    …
)
SELECT * FROM temp1, temp2
```

但 inner CTE 無法在 outer CTE 之外被存取，比如在上例中，無法在最後的 `SELECT` 子句中 `SELECT * FROM temp3`。

---

以下示範如何使用 CTE 與 nested query 處理相同的問題，現在有一個學生名單 (student) 與學生成績表 (enrollment) 如下：

**student**

|id|name|
|-|-|
|1|Alice|
|2|Bob|
|3|Cindy|
|4|Dorsey|
|5|Eric|
|6|Frank|

**enrollment**

|sid|cid|score|
|-|-|-|
|1|1|76|
|2|1|83|
|3|1|82|
|4|1|92|
|5|1|60|
|6|1|72|

現在我們要列出擁有最高分數的學生們的姓名與其得分：

**使用 Nested Query**

```SQL
select s.name, e.score
from student as s join enrollment as e on s.id = e.sid
where e.score = (
    select max(score) from enrollment
);
```

**使用 CTE**

```SQL
with temp (max_score) as (
    select max(score) from enrollment
)
select s.name, e.score
from
    student as s join enrollment as e on s.id = e.sid,
    temp
where e.score = temp.max_score;
```

# Recursion

CTE 可以做到一件 nested query 做不到的事，這件事就是 recursion，使用 `WITH RECURSIVE` 關鍵字可以讓一個普通的 CTE 變成 recursive CTE，範例如下：

```SQL
WITH RECURSIVE my_cte (counter) AS (
    (SELECT 1)
    UNION
    (SELECT counter * 2 FROM my_cte WHERE counter < 1024)
)
SELECT * FROM my_cte;
```

Output:

```plaintext
 counter 
---------
       1
       2
       4
       8
      16
      32
      64
     128
     256
     512
    1024
(11 rows)
```

> [!Note]
> 在執行 recursive CTE 前可以先 `SET statement_timeout = '10s'` 來避免 CTE 執行過久（10s 只是舉例）。
