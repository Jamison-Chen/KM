就像其它程式語言一樣，我們也可以將常用的 SQL 打包成可重複利用的 function，只是 SQL 中的 function 有以下幾個特點：

- 可以細分為 function 與 procedure
- 會被存在 database 裡（所以叫做 stored function 跟 stored procedure）

# Function 與 Procedure 的差別

Function 與 procedure 的差別在不同 DBMS 也有細微的不同，但大的概念是：

>Function 通常負責純粹的運算，不會用來改動到資料（pure function, no side-effect）；procedure 則通常用來實現商業邏輯，所以會對資料做新增、刪除、修改。

### On PostgreSQL

- 雖然前面說 function 通常不會用來改動到資料，但 PostgreSQL 並沒有對 function 加上實質的限制，所以你真的要這麼做也沒有人攔得住你
- 我們不能在一個 function 中控制 [[淺談 Database#Database Transaction|transaction]] 的開始與結束，一個 function 如果執行失敗了，會是外層（呼叫這個 function 的地方）的那個 transaction 要 rollback。Procedure 則沒有這個限制，我們可以在一個 procedure 中開啟與結束多個 transaction
- PostgreSQL 的 procedure 沒有 output，但 function 可以 output result set。（"result set" 就是一包有 1 到多個 rows 的資料，用 `SELECT` 語法得到的資料就是一種 result set）
- 呼叫 procedure 的方法是 `CALL xxx(...)`；呼叫 function 的方法則是 `SELECT xxx(...)`

### On MySQL

- 在 MySQL 中，function 內不能對任何資料庫的 state 做更動，否則會報錯，所以如果要新增、修改、刪除資料，一定要用 procedure
- 定義 procedure 時可以定義 output parameters，用來接收 procedure 內的某些執行結果；function 則不能設置 output parameter
- 與 PostgreSQL 不同的是，PostgreSQL 的 procedure 沒有 output，但 MySQL 的 procedure 可以 output result set（但這個 output 不能被用在其它 `SELECT` statement 中）


# 建立

### 建立一個 Stored Function

##### On PostgreSQL

```SQL
```

##### On MySQL

```SQL
```

### 建立一個 Stored Procedure

##### On PostgreSQL

```SQL
```

##### On MySQL

```SQL
```

# 使用

### 呼叫 Function

```SQL
SELECT xxx(...);
```

### 呼叫 Procedure

```SQL
CALL xxx(...);
```

如果有 output parameter 的話，可以用 `SELECT` 讀取：

e.g.

```SQL
CALL xxx(..., @x);
SELECT @x;
```

# 刪除

### 刪除 Function

```SQL
```

### 刪除 Procedure

```SQL
DROP PROCEDURE [IF EXISTS] <PROCEDURE_NAME>;
```

# 參考資料

- [PostgreSQL 相關](https://www.red-gate.com/simple-talk/databases/postgresql/functions-and-procedures-learning-postgresql-with-grant/)
- [MySQL 相關](https://stackoverflow.com/questions/3744209/mysql-procedure-vs-function-which-would-i-use-when)
