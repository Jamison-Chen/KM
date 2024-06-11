一個 query 語句的 `SELECT`、`FROM` 或 `WHERE` 子句中若含有另一個 query，這樣的結構就稱為 nested query，其中裡面的 query 稱為 subquery 或 inner query；外面的則稱為 outer query：

```SQL
SELECT column_name [, column_name, ... ]
FROM table1 [, table2, ... ]
WHERE column_name <operator> (
    SELECT column_name [, column_name, ... ]
    FROM table1 [, table2, ... ]
    [WHERE <condition>]
)
```

除了 `SELECT` 以外，nested query 還可以被用在 `INSERT`, `UPDATE` 以及 `DELETE` 語句中，其作用皆是扮演「篩選條件」的角色。

# Nested Query 的使用規則

- Subquery 必須用 `()` 包起來
- 出現在 `SELECT` 字句中的 subquery 必須是 [#Scalar Subquery](</./Database/SQL/Nested Query.md#Scalar Subquery>)
- Subquery 中不能出現 `ORDER BY` 子句，但可以用 `GROUP BY` 來達到 `ORDER BY` 的效果
- Subquery 的 output 只有一個 tuple (row) 時，outer query 只能用 `=`, `<`, `>`, `>=`, `<=`, `<>`, `<=>` 等 single-row operators 來進行比較運算
- Subquery 的 output 不只一個 tuple 時，outer query 只能用 `IN`, `EXISTS`, `NOT IN`, `ANY`, `ALL` 等 multi-row operators 來進行比較運算
- `BETWEEN` operator 不可以在 outer query 的 `WHERE` 子句中與 subquery 並用

### `EXISTS` Operator

`EXISTS` 用來判斷 subquery 中是否含有任何 tuple (row)，若有則 return true，否則 return false，由於 tuple 的內容是什麼並不重要，因此常常只在 subquery 的 `SELECT` 子句中寫一個數字 1，不回傳任何實際的 column 以節省記憶體，像是下面這樣：

```SQL
SELECT ... FROM ...
WHERE EXISTS (
    SELECT 1 FROM tbl
    WHERE ...
);
```

# Scalar Subquery

若 subquery 的 output 只有一個 tuple (row)，且該 tuple 有只有一個 column，則其實該 output 就是一個 scalar，這個 scalar 可以在 outer query 中使用 single-row operators (`>`, `<`, `=` …) 來做比較，舉例如下：

```SQL
SELECT employee_id, salary FROM employees
WHERE salary > (
    SELECT AVG(SALARY) FROM employees
);
```

Scalar subquery 也可以出現在 `SELECT` 字句中：

```SQL
SELECT
    name,
    (
        SELECT max(pop) FROM cities
        WHERE cities.state = states.name
    )
FROM states;
```

# Row Subquery

若 subquery 的 output 只有一個 tuple (row)，且該 tuple 有不只一個 column，則稱該 subquery 為 row subquery，搭配 row subquery 所使用的 operators 必須是 single-row operators，且 operator 的左手邊也必須是一個 `ROW`，舉例如下：

```SQL
SELECT first_name FROM employees
WHERE ROW(department_id, manager_id) = (
    SELECT department_id, manager_id FROM departments
    WHERE location_id = 1800
);
```

# 變數的 Refer

Subquery 裡可以 refer outer query 的變數 ，比如下例中的 `s`：

```SQL
SELECT * FROM student AS s
WHERE NOT EXISTS (
    SELECT sid FROM enrollment AS e
    WHERE e.cid = 1 AND e.sid = s.id
);
```

但==在 outer query 中不可 refer subquery 中的變數==，因為每一個 outer query 的 tuple 都是在 subquery 執行完畢後才被 select 出來。

# 執行效率

PostgreSQL 碰到 nested query 時，為了提高效率，只會執行 subquery 一次，將這個 result 暫存起來重複使用，再將 result 交給 outer query，最後才執行 outer query。

==Nested query 的效率某些時候會比 single-layer query 低==，因此建議能免則免。關於 Nested Query 與 single-layer Query 執行效能的差異，可以參考 [IN vs EXISTS vs ANY vs JOIN](</Database/SQL/IN vs EXISTS vs ANY vs JOIN.md>) 這篇文章。

# 參考資料

- <https://www.tutorialspoint.com/postgresql/postgresql_sub_queries.htm>
- <https://www.w3resource.com/PostgreSQL/postgresql-subqueries.php>
