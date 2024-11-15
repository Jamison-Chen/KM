Window functions 與 [Aggregate Functions](</Database/SQL/Aggregate Functions.md>) 有相似也有相異之處，相似之處在於 window functions 也是運算一堆 tuples；相異之處在於 aggregate functions 只會為每個分組結果 (`GROUP BY`) 輸出一個 tuple 或者一個 scalar，window functions 則是會把運算的結果依照分組結果 (`PARTITION BY`) 附加在每一個 tuple 上。

舉例：

```SQL
SELECT
    depname,
    empno,
    salary,
    avg(salary) OVER (PARTITION BY depname)
FROM empsalary;
```

Output:

```plaintext
  depname  | empno | salary |          avg
-----------+-------+--------+-----------------------
 develop   |    11 |   5200 | 5020.0000000000000000
 develop   |     7 |   4200 | 5020.0000000000000000
 develop   |     9 |   4500 | 5020.0000000000000000
 develop   |     8 |   6000 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     3 |   4800 | 4866.6666666666666667
 sales     |     1 |   5000 | 4866.6666666666666667
 sales     |     4 |   4800 | 4866.6666666666666667
(10 rows)
```

# Window Function 須搭配 `OVER` 子句

若一個 function 被呼叫時，後面跟著 `OVER` 子句，則該 function 就是一個 window function，反之則不是。

### Window Definition

`OVER` 子句中的內容又叫做 **window definition**，其用途在描述「資料被 apply 進這個 window function 前要如何前處理」，**前處理**泛指分組 ([PARTITION BY](</./Database/SQL/Window Functions.md#以 PARTITION BY 分組>))、排序 (`ORDER BY`) 等，比如前面例子中的 `OVER (PARTITION BY depname)`。

如果資料無須前處理，則 `OVER` 子句中以空值 `()` 表示，比如：

```SQL
SELECT *, ROW_NUMBER() OVER () FROM student;
```

### `WINDOW` 子句

一個 query 中可以有多個 window functions，每個 window function 都必須有各自的 window definition，然而，如果有多個 window functions 的 window definition 長地一模一樣，則可以將 window definition 定義在 `WINDOW` 子句中，並取一個名字來代表這個 window definition，達到重複使用的目的，比如下例中的 `w`：

```SQL
SELECT sum(salary) OVER w, avg(salary) OVER w
FROM empsalary
WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

若一個 query 中有多個 window functions 共用同一個 window function，則這些 window functions 的值會在「同一個對 data 的 loop」中被計算出來。

# 以 `ORDER BY` 排序

舉例：

```SQL
SELECT *, ROW_NUMBER() OVER (ORDER BY date_of_birth) FROM student;
```

Output:

```plaintext
 id |  name   | gender | date_of_birth | row_number 
----+---------+--------+---------------+------------
  6 | Fiona   | Female | 1998-11-01    |          1
  2 | Bob     | Male   | 1998-12-12    |          2
  4 | Dora    | Female | 1999-01-08    |          3
  1 | Alice   | Female | 1999-01-20    |          4
  3 | Candice | Female | 1999-04-20    |          5
  7 | Gina    | Female | 1999-05-20    |          6
  8 | Harry   | Male   | 1999-06-30    |          7
  5 | Eric    | Male   | 1999-08-08    |          8
(8 rows)
```

> [!Note]
>在 window definition 中使用 `ORDER BY` 的效果與在 `FROM` 子句後使用 `ORDER BY` 不同，前者的效果是「先排序，後計算」，後者則是「先計算，後排序」，因此雖然兩種方法得到的資料都是排序好的，但 window function 計算出來的值會不同。
>
>以上例而言，如果 query 改成 `SELECT *, ROW_NUMBER() OVER () FROM student ORDER BY date_of_birth;`，則輸出會變成：
>
>```plaintext
>id |  name   | gender | date_of_birth | row_number 
>---+---------+--------+---------------+------------
>  6 | Fiona   | Female | 1998-11-01    |          6
>  2 | Bob     | Male   | 1998-12-12    |          2
>  4 | Dora    | Female | 1999-01-08    |          4
>  1 | Alice   | Female | 1999-01-20    |          1
>  3 | Candice | Female | 1999-04-20    |          3
>  7 | Gina    | Female | 1999-05-20    |          7
>  8 | Harry   | Male   | 1999-06-30    |          8
>  5 | Eric    | Male   | 1999-08-08    |          5
>(8 rows)
>```

# 以 `PARTITION BY` 分組

在 [Aggregate Functions](</Database/SQL/Aggregate Functions.md>) 以及一般的 query 中，我們使用 `GROUP BY` 來分組，但在 window functions 中我本使用的是 `PARTITION BY`：

```SQL
SELECT *, ROW_NUMBER() OVER (PARTITION BY gender) FROM student;
```

Output:

```plaintext
 id |  name   | gender | date_of_birth | row_number 
----+---------+--------+---------------+------------
  6 | Fiona   | Female | 1998-11-01    |          1
  7 | Gina    | Female | 1999-05-20    |          2
  1 | Alice   | Female | 1999-01-20    |          3
  4 | Dora    | Female | 1999-01-08    |          4
  3 | Candice | Female | 1999-04-20    |          5
  8 | Harry   | Male   | 1999-06-30    |          1
  2 | Bob     | Male   | 1998-12-12    |          2
  5 | Eric    | Male   | 1999-08-08    |          3
(8 rows)
```

若沒有特別聲明 `PARTITION BY`，那預設就是取整個 table 來運算。

然而，其實還有比 partition 更小的分組單位：**window frame**，而==每次呼叫 window function 時的 input rows 其實是 window frame 內的 rows 而非 partition 內的所有 rows==。在沒有 `ORDER BY` 的情況下，window frame 的範圍等於 partition 的範圍；但若有 `ORDER BY`，則 window frame 的範圍會是「從 partition 的開頭，到目前 row 的位置，以及後續所有的 **peer rows**（跟目前的 row 擁有相同值的 rows）」，舉例如下：

```SQL
SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
```

Output:

```plaintext
 salary |  sum
--------+-------
   3500 |  3500
   3900 |  7400
   4200 | 11600
   4500 | 16100
   4800 | 25700
   4800 | 25700
   5000 | 30700
   5200 | 41100
   5200 | 41100
   6000 | 47100
(10 rows)
```

你會發現，並不是所有的 sum 都等於整個 table 的 salary 的總和，由於有 `ORDER BY`，所以比如在計算 row 5 的 sum 時，就只會計算「row 1 ~ row 5 以及所有 salay 等於 4800 的其它 rows」的總和。

關於 window frame customization，由於較少用到因此有興趣者請見 [官方文件](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)，簡單的摘要是：

- 在 window definition 中的最後加上 frame clause
- Frame clause 中可以定義 frame start, frame end 以及 frame exclusion

# Window Functions 的執行順位

Window functions 可以讀取到的 rows 是經過 `WHERE`, `GROUP BY`, `HAVING` 篩選／分組過後的 rows，其執行順位就像其它被 SELECT 的 columns 一樣，幾乎是最後。

也因為如此，==window functions 只能出現在 `SELECT` 子句中==作為其中一個 output column，==以及出現在 `ORDER BY` 子句中==作為 filter condition，其它地方像是 `GROUP BY`, `HAVING`, `WHERE` 子句中都不能出現 window functions。

Window functions 的執行順位甚至在 aggregate functions 之後，這意味著你可以將 aggregate function 的輸出值放在一個 window function 中做為參數，但不能將 window function 的輸出值放在一個 aggregate function 中做為參數。

若想要拿 window function 的輸出值做為篩選條件，只能將 window function 先放在一個 subquery 的 `SELECT` 子句，然後將這個 subquery 放到 outer query 的 `WHERE` 子句或 `FROM` 子句中，舉例如下：

```SQL
SELECT * FROM (
    SELECT cid, sid, score,
    rank() OVER (
        PARTITION BY cid ORDER BY score DESC NULLS LAST
    ) AS rank
    FROM enrollment
) AS sub
WHERE sub.rank <= 2 AND sub.score IS NOT NULL;
```

上例中，outer query 裡的 `sub.rank` 就是在 inner query 中透過的 window function 計算出來的。

Output:

```plaintext
 cid | sid | score | rank 
-----+-----+-------+------
   1 |   6 | 92.00 |    1
   1 |   1 | 90.50 |    2
   2 |   8 | 89.00 |    1
   2 |   6 | 79.90 |    2
   4 |   6 | 99.99 |    1
   4 |   2 | 99.99 |    1
   5 |   2 | 88.00 |    1
   5 |   1 | 87.00 |    2
   6 |   8 | 92.50 |    1
   6 |   2 | 89.50 |    2
(10 rows)
```

# 常見的 Built-In Window Functions

### `row_number()`

依照 `OVER` 子句中的規則，從 1 開始給予每個 row 編號（遞增）。

e.g.

```SQL
SELECT *, row_number() OVER (ORDER BY score DESC) AS row_num
FROM enrollment;
```

Output:

```plaintext
 sid | score | row_num 
-----+-------+---------
  2  | 99.99 |       1
  6  | 99.99 |       2
  1  | 99.00 |       3
  4  | 97.00 |       4
  8  | 92.00 |       5
(5 rows)
```

### `rank()`

在 `OVER` 子句搭配 `ORDER BY` 使用可以達到類似 `row_number()` 的效果，差別是 `rank()` 會給予相同排名者同樣的編號，並且依照編號重複次數跳過後續的號碼。

e.g.

```SQL
SELECT *, rank() OVER (ORDER BY score DESC) AS rank
FROM enrollment;
```

Output:

```plaintext
 sid | score | rank 
-----+-------+------
  2  | 99.99 |    1
  6  | 99.99 |    1
  1  | 99.00 |    3
  4  | 97.00 |    4
  8  | 92.00 |    5
(5 rows)
```

### `dense_rank()`

類似 `rank()`，但不會跳號。

e.g.

```SQL
SELECT *, dense_rank() OVER (ORDER BY score DESC) AS rank
FROM enrollment;
```

Output:

```plaintext
 sid | score | rank 
-----+-------+------
  2  | 99.99 |    1
  6  | 99.99 |    1
  1  | 99.00 |    2
  4  | 97.00 |    3
  8  | 92.00 |    4
(5 rows)
```

> [!Note]
>[Aggregate Functions](</Database/SQL/Aggregate Functions.md>) 加上 `OVER` 後也會變成 window functions，但原本可以放在 `HAVING` 子句中的 aggregate functions 在變成 window functions 後就不能放在 `HAVING` 子句了。

想了解更多 built-in window functions，請參考 [官方文件](https://www.postgresql.org/docs/current/functions-window.html)

# 總結

一個 window function 的結構可以是下面的其中一種：

```plaintext
function_name (
    [expression, [expression, ...]]
) [FILTER (WHERE filter_clause)]
OVER window_name
```

```plaintext
function_name (
    [expression, [expression, ...]]
) [FILTER (WHERE filter_clause)]
OVER (window_definition)
```

```plaintext
function_name (*) [FILTER (WHERE filter_clause)] OVER window_name
```

```plaintext
function_name (*) [FILTER (WHERE filter_clause)] OVER (window_definition)
```

其中，window_definition 的結構如下：

```plaintext
[existing_window_name]
[PARTITION BY expression [, ...]]
[ORDER BY expression [, ...]]
[frame_clause]
```

# 參考資料

- <https://www.postgresql.org/docs/current/tutorial-window.html>
- <https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS>
