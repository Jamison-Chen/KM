凡是經過運算一堆 tuples (rows) 後輸出一個值的 function，就叫做 aggregate function，簡稱 aggregates。

SQL standard 中的 aggregate functions 包括：`avg()`、`count()`、`max()`、`min()` 以及 `sum()`。

# Aggregates 與 `GROUP BY` 是好朋友

當 aggregate functions 與其它「非 aggregate function 的欄位」共同出現在 `SELECT` 子句中時，「非 aggregate function 的欄位」必須是「分組依據」，所以必須要有 `GROUP BY` 子句來說明如何用這些「非 aggregate function 的欄位」來分組。

e.g.

```SQL
SELECT max(score), cid
FROM enrollment
GROUP BY cid;
```

上例的意思是要「以班為單位，選出成績最高者」，`GROUP BY cid` 不能省略。

### Aggregates Outputs as a Column

由於上述限制，若我們想將 `max(score)` 當作一個 column 加在 `enrollment` 的後面，就不能直接寫 `SELECT *, max(score) FROM enrollment;`。那該怎麼做呢？其實有兩種方法可以做到：

- **法一：`JOIN`**

    ```SQL
    SELECT e.*, sub.max_score
    FROM enrollment AS e
        JOIN (
            SELECT max(score) AS max_score, cid
            FROM enrollment
            GROUP BY cid
        ) AS sub
        ON e.cid = sub.cid;
    ```

    既然不能任意把其他 columns 寫在有 aggregate function 的 `SELECT` clause，那就使用 `JOIN` 將這些想加入的 columns 加進去。

- **法二：`OVER`**

    ```SQL
    SELECT *, max(score) OVER (PARTITION BY cid) FROM enrollment;
    ```

    - 這個做法的原理是將 `max` 這個 aggregate function 轉化成 [Window Functions](</Database/SQL/Window Functions.md>)
    - 無論是語法的簡潔度還是執行效率，這個方法皆較佳
    - 若沒有要 `PARTITION BY` 任何東西，那就寫 `OVER ()` 即可

# Aggregates 只能出現在 `SELECT` 與 `HAVING`

e.g.

```SQL
SELECT sum(quantity) AS q_sum, sid
FROM trade_record
GROUP BY sid
HAVING sum(quantity) > 0;
```

>執行順序較後面的 clause 才能修飾執行順序較前面的 clause。

- ==`HAVING` 不能以 `WHERE` 取代，因為 aggregate function 的執行順位在 `WHERE` clause 之後、`HAVING` clause 之前==

- 在 `HAVING` clause 中，不能拿 aggregate function 的 output 與一般的 column 值做比較，正確的做法是使用 `WHERE` + subquery

    ```SQL
    -- this won't work
    SELECT * FROM car HAVING max(price) = price;

    -- the right way
    SELECT * FROM cars
    WHERE price = (
        SELECT max(price) FROM cars
    );
    ```

- `HAVING` clause 中「不能」使用 `SELECT` clause 中的變數，比如上例中的 `q_sum`

# 參考資料

- <https://www.postgresqltutorial.com/postgresql-aggregate-functions/>
