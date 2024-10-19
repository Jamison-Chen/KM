`table_a JOIN table_b` 的效果是「把 table_a 的欄位跟 table_b 的欄位合起來成為另一張新表」。了解這個定義後我們很清楚這張 JOIN 出來新的表會有哪些 columns 了，但還有一個問題是：這張表會有哪些 rows 呢？

有一種做法是對左右兩張表的 rows 做 [Cartesian product (笛卡兒乘積)](https://en.wikipedia.org/wiki/Cartesian_product)，這樣如果左表有 m 個 rows，右表有 n 個 rows，JOIN 後就會得到 $m \times n$ 個 rows，這種 JOIN 方法在 SQL 語法裡叫 `CROSS JOIN`：

# `CROSS JOIN`

```SQL
SELECT table_a.*, table_b.*
FROM table_a
CROSS JOIN table_b;
```

---

然而有時後我們會希望只把符合特定條件的 rows 做組合，最常見的就是 table_a 的 column_a 是 table_b 的 column_b 的 foreign key，我們希望只把所有 table_a.column_a 等於 table_b.column_b 的 rows 組合起來就好。這時候就會須要搭配 `ON` statement 來使用，`ON` statement 會定義「在什麼條件下可以把左表跟右表的欄位合併」，比如前面的例子用 SQL 寫就會是：

```SQL
SELECT table_a.*, table_b.*
FROM table_a
INNER JOIN table_b ON table_a.id = table_b.id;
```

請注意，上面這個例子中已經不再是使用 `CROSS JOIN` 了，而是使用 `INNER JOIN`，`CROSS JOIN` 因為只有 Cartesian product 這個功能，所以不能搭配 `ON` 使用。而可以搭配 `ON` 使用的 JOIN 除了 `INNER JOIN` 以外，還有 `LEFT JOIN`、`RIGHT JOIN`與 `FULL OUTER JOIN`，它們的差別如下：

# `INNER JOIN`

- `INNER JOIN` 可以直接簡寫為 `JOIN`
- 只會回傳符合 `ON` statement 的規則的 rows，換句話說就是「取兩張表的交集」

# `LEFT JOIN`

只要 `ON` statement 裡提到的所有「左邊的表的欄位」在左邊的表都有值就會回傳，所以結果可能是某些 rows 的「右邊的表的欄位」是 null

# `RIGHT JOIN`

只要 `ON` statement 裡提到的所有「右邊的表的欄位」在右邊的表都有值就會回傳，所以結果可能是某些 rows 的「左邊的表的欄位」是 null

# `FULL OUTER JOIN`

左右兩邊的所有 rows 都拿出來，沒有配對到的就在另一邊表的欄位填入 null，所以結果可能是某些 rows 的「左邊的表的欄位」是 null、某些 rows 的「右邊的表的欄位」是 null。換句話說就是「取兩張表的聯集」。

---

下面這張圖展示了如何搭配使用 `LEFT/RIGHT/INNER/FULL OUTER JOIN`、`ON`、`WHERE` 取得各種不同的集合：

![[sql-joins.png]]

---

最後還有一種現在比較少見的 JOIN 叫做 `NATURAL JOIN`：

# `NATURAL JOIN`

```SQL
SELECT table_a.*, table_b.*
FROM table_a
NATURAL JOIN table_b;
```

`NATURAL JOIN` 是一種 `INNER JOIN`，它會將左右兩張表具有相同名稱的欄位作為 `ON` 的條件。

- 假設 table_a 與 table_b 都有一個欄位叫 id，則 `table_a NATURAL JOIN table_b` 就等同於 `table_a INNER JOIN table_b ON table_a.id = table_b.id`
- 若兩個 tables 有多個相同名稱的欄位，則這些欄位會被用 `AND` 串接起來。比如假設 table_a 與 table_b 有兩個相同名稱的欄位，分別叫 id 與 name，則 `table_a NATURAL JOIN table_b` 就等同於 `table_a INNER JOIN table_b ON table_a.id = table_b.id AND table_a.name = table_b.name`，有更多相同名稱的欄位就依此類推

因為 `NATURAL JOIN` 有一套自己的 `ON` 規則，所以不須要（也不能）手動寫 `ON` statement。

# 用 `USING` 取代囉唆的 `ON`

當 `ON` statement 裡左右兩張表的欄位名稱相同，就可以用比較簡潔的 `USING` 取代 `ON` 的寫法。

e.g.

```SQL
SELECT student.first_name, enrollment.class_name
FROM student
JOIN enrollment ON student.student_id = enrollment.student_id;
```

因為當作條件的欄位在兩張表的名字都叫做 student_id，所以可以用下方 SQL 替代之：

```SQL
SELECT student.first_name, enrollment.class_name
FROM student
JOIN enrollment USING (student_id);
```

請注意，`USING` 後方的欄位名稱一定要用 `()` 包起來！

# 新舊版本的 JOIN

假設現在資料庫有以下幾個表：

**company**

| id | name |
|---|---|
| 0 | Apple |
| 1 | Alphabet |
| ... | ... |

**team**

| id | name | cid |
|---|---|---|
| 0 | UX | 0 |
| 1 | Backend | 1 |
| ... | ... | ... |

**employee**

| id | name | tid |
|---|---|---|
| 0 | Alex | 0 |
| 1 | Bob | 2 |
| ... | ... | ... |

今天若想「列出一個有公司名稱、團隊名稱、員工名稱的總表」，則有以下兩種做法：

### FROM 多個表 WHERE …

```SQL
SELECT c.name, t.name, e.name
FROM company AS c, team AS t, employee AS e
WHERE c.id = t.cid AND t.id = e.tid;
```

### JOIN … ON …

```SQL
SELECT c.name, t.name, e.name
FROM company AS c JOIN (
    team AS t JOIN employee AS e ON t.id = e.tid
) ON c.id = t.cid;
```

### 比較

兩個做法可以得到一模一樣的結果，事實上，`FROM 多個表 WHERE ...` 就是比較老舊（或者說過時）的 join 方式，其中 `WHERE` 子句裡的 `=` 的意思是 inner join，`*=` 是 left join，`=*` 則是 right join。

更一般化的說法：

```SQL
SELECT * FROM A, B WHERE A.a = B.b;
-- 等價於：
SELECT * FROM A JOIN B ON A.a = B.b;

--

SELECT * FROM A, B WHERE A.a *= B.b;
-- 等價於：
SELECT * FROM A LEFT JOIN B ON A.a = B.b;

--

SELECT * FROM A, B WHERE A.a =* B.b;
-- 等價於：
SELECT * FROM A RIGHT JOIN B ON A.a = B.b;
```

### `FROM 多個表 WHERE ...` 過時了

當有三個以上的表相互 join 時，且有一些 left join 或 right join 存在其中，那 join 的順序就會影響結果。

此時在 `WHERE` 子句中會出現類似 `c.id = t.cid AND t.id = e.tid` 這樣「複數條件」的語句，而==不同 DMBS 執行複數條件時的順序不盡相同==，某些 DBMS 會是由左往右執行，某些則會由右往左執行，容易造成誤解或誤用。

舉例而言，如果開頭的「列出一個有公司名稱、團隊名稱、員工名稱的總表」這個例子中，現在若我要把「沒有任何 team 的 comany 也列出來一次」，則 query 以 `JOIN ... ON ...` 來寫的話，會改成這樣：

```SQL
SELECT c.name, t.name, e.name
FROM company AS c
LEFT JOIN (
    team AS t
    JOIN employee AS e
    ON t.id = e.tid
) ON c.id = t.cid;
```

以 `FROM 多個表 WHERE ...` 來寫的話：

```SQL
SELECT c.name, t.name, e.name
FROM company AS c, team AS t, employee AS e
WHERE c.id *= t.cid AND t.id = e.tid;
```

如果後者這個 query 的 `WHERE` 子句是由右往左執行，那結果就是我們想要的，但如果是由左往右執行，那我們還是看不到沒有任何 team 的 comany，而這就是不推薦使用這種寫法的原因。

# 延伸閱讀

- [[IN vs EXISTS vs ANY vs JOIN]]

# 參考資料

- <https://learnsql.com/blog/joins-vs-multiple-tables-in-from/>
- <https://stackoverflow.com/questions/5118562/inner-join-vs-multiple-table-names-in-from>
- <https://stackoverflow.com/questions/1018822/inner-join-on-vs-where-clause>
- <https://stackoverflow.com/questions/894490/sql-left-join-vs-multiple-tables-on-from-line>
