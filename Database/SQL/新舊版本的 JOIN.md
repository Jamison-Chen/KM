假設現在資料庫有以下幾個表：

**company**

| id | name |
|---|---|
| 0 | Apple |
| 1 | Alphabet |
| 2 | Meta |
| ... | ... |

**team**

| id | name | cid |
|---|---|---|
| 0 | UX | 0 |
| 1 | Backend | 0 |
| 2 | QA | 0 |
| 3 | DevOps | 1 |
| ... | ... | ... |

**employee**

| id | name | tid |
|---|---|---|
| 0 | Alex | 0 |
| 1 | Bob | 2 |
| 2 | Chris | 5 |
| ... | ... | ... |

今天我想「列出一個有公司名稱、團隊名稱、員工名稱的總表」，則有以下兩種做法：

### FROM 多個表 WHERE … 的寫法

```SQL
SELECT c.name, t.name, e.name
FROM company AS c, team AS t, employee AS e
WHERE c.id = t.cid AND t.id = e.tid;
```

### JOIN … ON … 的寫法

```SQL
SELECT c.name, t.name, e.name
FROM company AS c JOIN (
    team AS t JOIN employee AS e ON t.id = e.tid
) ON c.id = t.cid;
```

# 比較

兩個做法可以得到一模一樣的結果，事實上，`FROM 多個表 WHERE ...` 就是比較老舊（或者說過時）的 join 方式，其中 `WHERE` 子句裡的 `=` 的意思是 inner join，`*=` 是 left join，`=*` 則是 right join。

更一般化的說法：

```SQL
SELECT * FROM A, B WHERE A.a = B.b;
-- 等價於：
SELECT * FROM A JOIN B ON A.a = B.b;
```

```SQL
SELECT * FROM A, B WHERE A.a *= B.b;
-- 等價於：
SELECT * FROM A LEFT JOIN B ON A.a = B.b;
```

```SQL
SELECT * FROM A, B WHERE A.a =* B.b;
-- 等價於：
SELECT * FROM A RIGHT JOIN B ON A.a = B.b;
```

# `FROM 多個表 WHERE ...` 過時了

當有三個以上的表相互 join 時，且有一些 left join 或 right join 存在其中，那 join 的順序就會影響結果。

你可以想像在 `WHERE` 子句中會出現類似 `c.id = t.cid AND t.id = e.tid` 這樣的「多個 join」的語句，這樣的語句在某些 DBMS 中是由左往右執行，在另一些 DBMS 中則是由右往左執行，容易造成誤解或誤用。

舉例而言，如果開頭的「列出一個有公司名稱、團隊名稱、員工名稱的總表」這個例子中，現在若我要把「沒有任何 team 的 comany 也列出來一次」，則 query 以 `JOIN ... ON ...` 來寫的話，會改成這樣：

```SQL
SELECT c.name, t.name, e.name
FROM company AS c LEFT JOIN (
    team AS t JOIN employee AS e ON t.id = e.tid
) ON c.id = t.cid;
```

以 `FROM 多個表 WHERE ...` 來寫的話：

```SQL
SELECT c.name, t.name, e.name
FROM company AS c, team AS t, employee AS e
WHERE c.id *= t.cid AND t.id = e.tid;
```

如果後者這個 query 的 `WHERE` 子句是由右往左執行，那結果就是我們想要的，但如果是由左往右執行，那我們還是看不到沒有任何 team 的 comany。而這就是不推薦使用這個寫法的原因。

# 參考資料

- <https://learnsql.com/blog/joins-vs-multiple-tables-in-from/>
- <https://stackoverflow.com/questions/5118562/inner-join-vs-multiple-table-names-in-from>
- <https://stackoverflow.com/questions/1018822/inner-join-on-vs-where-clause>
- <https://stackoverflow.com/questions/894490/sql-left-join-vs-multiple-tables-on-from-line>
