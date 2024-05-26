本篇主要討論標題的四種方法在效能上的差異，現在假設資料庫有以下三個表：

**course**

|id|name|
|--|--|
|1|Math|
|2|Science|
|…|…|

**student**

| id | name | gender | date_of_birth |
|---|---|---|---|
| 1 | Alice | Female | 1999-01-20 |
| 2 | Bob | Male | 1998-12-12 |
| 3 | Candice | Female | 1999-04-20 |
| … | … | … | … |

**enrollment**

| cid | sid | score |
|---|---|---|
| 1 | 1 | 90.50 |
| 1 | 2 | 79.00 |
| 1 | 3 | 88.00 |
| 1 | 4 | 88.50 |
| 2 | 5 |*null*|
| 2 | 6 | 79.90 |
| … | … | … |

# Inclusion Queries

當要篩選出「包含某值」的資料時，這樣的 query 稱為 inclusion queries。

比如若想取得所有有參與「課堂 1」學生的資料，可以分別以 `IN`, `ANY`, `EXISTS` 以及 `JOIN` 四種做法得到相同的結果：

- **使用 `IN`**

    ```SQL
    SELECT * FROM student
    WHERE id IN (
        SELECT sid FROM enrollment
        WHERE cid = 1
    );
    ```

- **使用 `= ANY`**

    ```SQL
    SELECT * FROM student
    WHERE id = ANY(
        SELECT sid FROM enrollment
        WHERE cid = 1
    );
    ```

- **使用 `EXISTS`**

    ```SQL
    SELECT * FROM student AS s
    WHERE EXISTS (
        SELECT sid FROM enrollment
        WHERE cid = 1 AND sid = s.id
    );
    ```

- **使用 `JOIN`**

    ```SQL
    SELECT s.* FROM student AS s
    JOIN enrollment AS e ON s.id = e.sid
    WHERE e.cid = 1;
    ```

傳統上會認為 `EXIST` 與 `JOIN` 兩種做法較有效率，不過這些年來大部分的 RDBMS 在 `IN` 與 `ANY` 的演算上都做了許多改善，因此其實在處理 inclusion queries 時，上面四個做法的演算效率是一模一樣的。

我們可以用 `EXPLAIN ANALYZE` 產生的 query plan（詳見[EXPLAIN](</Database/SQL/EXPLAIN.md>)）來驗證這個說法，你會發現四種做法的 query plan 都相同如下：

```plaintext
                                                                       QUERY PLAN                                                                       
--------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join  (cost=460.41..918.92 rows=10004 width=14) (actual time=5.063..14.325 rows=9915 loops=1)
   Hash Cond: (s.id = e.sid)
   ->  Seq Scan on student s  (cost=0.00..406.00 rows=20000 width=22) (actual time=0.019..3.037 rows=20000 loops=1)
   ->  Hash  (cost=335.36..335.36 rows=10004 width=8) (actual time=4.960..4.962 rows=9915 loops=1)
         Buckets: 16384  Batches: 1  Memory Usage: 516kB
         ->  Index Only Scan using enrollment_pkey on enrollment e  (cost=0.29..335.36 rows=10004 width=8) (actual time=0.045..2.530 rows=9915 loops=1)
               Index Cond: (cid = 1)
               Heap Fetches: 0
 Planning Time: 0.480 ms
 Execution Time: 14.989 ms
(10 rows)
```

其中，因為 `IN` 版本與 `ANY` 版本連 subquery 都長得一樣，因此我們會說 ==`IN (subquery)` 與 `= ANY (subquery)` 是等價的==。

可是請別高興得太早！我們接著來看 exclusion queries…

# Exclusion Queries

當要篩選出「不包含某值」的資料時，這樣的 query 稱為 exclusion queries。

比如我今天想要取得所有**沒有**參與「課堂 1」的學生的基本資料，一樣有四種做法可以得到相同的 output：

- **使用 `NOT IN`**

    ```SQL
    SELECT * FROM student
    WHERE id NOT IN (
        SELECT sid FROM enrollment
        WHERE cid = 1
    );
    ```

- **使用 `<> ALL`**

    ```SQL
    SELECT * FROM student
    WHERE id <> ALL(
        SELECT sid FROM enrollment
        WHERE cid = 1
    );
    ```

- **使用 `NOT EXISTS`**

    ```SQL
    SELECT * FROM student AS s
    WHERE NOT EXISTS (
        SELECT sid FROM enrollment
        WHERE cid = 1 AND sid = s.id
    );
    ```

- **使用 `LEFT JOIN` +  `IS NULL`**

    ```SQL
    SELECT s.* FROM student AS s
    LEFT JOIN enrollment AS e
    ON s.id = e.sid AND e.cid = 1
    WHERE e.* IS NULL;
    ```

這次 `EXPLAIN ANALYZE` 產生的 query plan 就不同了：

```SQL
EXPLAIN ANALYZE SELECT * FROM student
WHERE id NOT IN (
    SELECT sid FROM enrollment
    WHERE cid = 1
);
```

Output:

```plaintext
                                                           QUERY PLAN                                                           
--------------------------------------------------------------------------------------------------------------------------------
 Seq Scan on student  (cost=14.37..30.24 rows=235 width=144) (actual time=0.032..0.034 rows=3 loops=1)
   Filter: (NOT (hashed SubPlan 1))
   Rows Removed by Filter: 5
   SubPlan 1
     ->  Bitmap Heap Scan on enrollment  (cost=4.21..14.35 rows=7 width=8) (actual time=0.008..0.009 rows=5 loops=1)
           Recheck Cond: (cid = 1)
           Heap Blocks: exact=1
           ->  Bitmap Index Scan on enrollment_pkey  (cost=0.00..4.21 rows=7 width=0) (actual time=0.005..0.005 rows=5 loops=1)
                 Index Cond: (cid = 1)
 Planning Time: 0.073 ms
 Execution Time: 0.051 ms
(11 rows)
```

---

```SQL
EXPLAIN ANALYZE SELECT * FROM student
WHERE id <> ALL(
    SELECT sid FROM enrollment
    WHERE cid = 1
);
```

Output:

```plaintext
                                                              QUERY PLAN                                                              
--------------------------------------------------------------------------------------------------------------------------------------
 Seq Scan on student  (cost=4.21..2416.44 rows=235 width=144) (actual time=0.022..0.026 rows=3 loops=1)
   Filter: (SubPlan 1)
   Rows Removed by Filter: 5
   SubPlan 1
     ->  Materialize  (cost=4.21..14.39 rows=7 width=8) (actual time=0.001..0.002 rows=4 loops=8)
           ->  Bitmap Heap Scan on enrollment  (cost=4.21..14.35 rows=7 width=8) (actual time=0.008..0.009 rows=5 loops=1)
                 Recheck Cond: (cid = 1)
                 Heap Blocks: exact=1
                 ->  Bitmap Index Scan on enrollment_pkey  (cost=0.00..4.21 rows=7 width=0) (actual time=0.006..0.006 rows=5 loops=1)
                       Index Cond: (cid = 1)
 Planning Time: 0.102 ms
 Execution Time: 0.062 ms
(12 rows)
```

---

```SQL
EXPLAIN ANALYZE SELECT * FROM student AS s
WHERE NOT EXISTS (
    SELECT sid FROM enrollment
    WHERE cid = 1 AND sid = s.id
);
```

Output:

```plaintext
                                                             QUERY PLAN                                                             
------------------------------------------------------------------------------------------------------------------------------------
 Hash Anti Join  (cost=14.44..35.01 rows=463 width=144) (actual time=0.047..0.050 rows=3 loops=1)
   Hash Cond: (s.id = enrollment.sid)
   ->  Seq Scan on student s  (cost=0.00..14.70 rows=470 width=144) (actual time=0.006..0.007 rows=8 loops=1)
   ->  Hash  (cost=14.35..14.35 rows=7 width=8) (actual time=0.031..0.032 rows=5 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 9kB
         ->  Bitmap Heap Scan on enrollment  (cost=4.21..14.35 rows=7 width=8) (actual time=0.027..0.028 rows=5 loops=1)
               Recheck Cond: (cid = 1)
               Heap Blocks: exact=1
               ->  Bitmap Index Scan on enrollment_pkey  (cost=0.00..4.21 rows=7 width=0) (actual time=0.022..0.022 rows=5 loops=1)
                     Index Cond: (cid = 1)
 Planning Time: 0.101 ms
 Execution Time: 0.089 ms
(12 rows)
```

---

```SQL
EXPLAIN ANALYZE SELECT s.* FROM student AS s
LEFT JOIN enrollment AS e
ON s.id = e.sid AND e.cid = 1
WHERE e.* IS NULL;
```

Output:

```plaintext
 Hash Left Join  (cost=14.44..30.38 rows=2 width=144) (actual time=0.091..0.094 rows=3 loops=1)
   Hash Cond: (s.id = e.sid)
   Filter: (e.* IS NULL)
   Rows Removed by Filter: 5
   ->  Seq Scan on student s  (cost=0.00..14.70 rows=470 width=144) (actual time=0.062..0.064 rows=8 loops=1)
   ->  Hash  (cost=14.35..14.35 rows=7 width=60) (actual time=0.018..0.019 rows=5 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 9kB
         ->  Bitmap Heap Scan on enrollment e  (cost=4.21..14.35 rows=7 width=60) (actual time=0.013..0.015 rows=5 loops=1)
               Recheck Cond: (cid = 1)
               Heap Blocks: exact=1
               ->  Bitmap Index Scan on enrollment_pkey  (cost=0.00..4.21 rows=7 width=0) (actual time=0.006..0.006 rows=5 loops=1)
                     Index Cond: (cid = 1)
 Planning Time: 0.293 ms
 Execution Time: 0.317 ms
(14 rows)
```

我們發現，`NOT IN` 與 `<> ALL` 的 `EXPLAIN ANALYZE` 結果中都出現了 SubPlan，而 `NOT EXISTS` 與 `LEFT JOIN` 則沒有。已知==含有越少層 SubPlan 的 query 越有效率==，因此可以初步得到以下結論：

>`NOT EXISTS` 與 `LEFT JOIN` 在處理 Exclusion Queries 時比較有效率。

然而觀察 Execution Time 時我們又會發現，`NOT IN` 所花的時間才是最少的，其實這是因為 PostgreSQL 在 `NOT IN` 之中使用了 **hashed SubPlan**，運算效率因此得到提升，PostgreSQL 會在這部分下功夫，也是因為 `NOT IN` 這種寫法對人們而言是很直覺的。

不過，當 SubPlan 產出的 rows 太多時，PostgreSQL 的 `NOT IN` 又會回到沒有 hash 的做法，效率就又變低了。

# 參考資料

- <https://www.percona.com/blog/2020/04/16/sql-optimizations-in-postgresql-in-vs-exists-vs-any-all-vs-join/>
