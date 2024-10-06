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

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/sql-joins.png>)

---

最後還有一種現在比較少見的 JOIN 叫做 `NATURAL JOIN`：

# `NATURAL JOIN`

```SQL
SELECT table_a.*, table_b.*
FROM table_a
NATURAL JOIN table_b;
```

- `NATURAL JOIN` 是一種 `INNER JOIN`，它會將左右兩張表具有相同名稱的欄位作為 `ON` 的條件
    - 假設 table_a 與 table_b 都有一個欄位叫 id，則 `table_a NATURAL JOIN table_b` 就等同於 `table_a INNER JOIN table_b ON table_a.id = table_b.id`
    - 假設 table_a 與 table_b 有兩個相同名稱的欄位，分別叫 id 與 name，則 `table_a NATURAL JOIN table_b` 就等同於 `table_a INNER JOIN table_b ON table_a.id = table_b.id AND table_a.name = table_b.name`，有更多相同名稱的欄位就依此類推
- 因為 `NATURAL JOIN` 有一套自己的 `ON` 規則，所以不須要（也不能）手動寫 `ON` statement

# 用 `USING` 取代囉唆的 `ON`

#TODO 
