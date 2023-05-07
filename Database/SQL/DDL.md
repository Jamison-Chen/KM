# `CREATE`

### `NOT NULL` Constraint

有此 constraint 的 column 不得出現 `null`，否則可以。

### `PRIMARY KEY` Constraint

Primary Key 可以是單一 column 或者是一組 columns，當是單一個 column 時，通常會與 column 的其他定義寫在同一行；若是一組 columns 則須另外寫一行，並用 `()` 包住 columns。

e.g. `id BIGSERIAL NOT NULL PRIMARY KEY`, `PRIMARY KEY (a, b)`

### `UNIQUE` Constraint

有此 constraint 的 column 不得出現重複的資料，否則可以。

與 `PRIMARY KEY` constraint 類似地，`UNIQUE` constraint 可以加在單一 column 或者是一組 columns 上，當加在單一 column 上時，通常會與 column 的其他定義寫在同一行；若是一組 columns 則須另外寫一行，並用 `()` 包住 columns。

`UNIQUE` constraint 隱含了對指定 column 加上 `NOT NULL` constraint。

e.g. `email VARCHAR(256) NOT NULL UNIQUE`, `UNIQUE (a, b)`

### `DEFAULT <VALUE>`

若一個 column 有設定 `DEFAULT <VALUE>`，則當 insert data 時沒有給該 column 值時，RDBMS 會自動填上 default value。

### `REFERENCES` Constraint

用來聲明一個作為 foreign key 的 column 是參照哪個 table 的哪個 column。

### `ON DELETE <ACTION>`

當一個 column 為 foreign key 時，需要聲明當其參照的原始資料被刪除時，要怎麼處理這個參照的資料。處理的方法有很多種，包括 `CASCADE`、`SET NULL`、`NO ACTION`、`SET DEFAULT`… 等，詳見 [[Integrity Constraint#On-Delete Action]]。

`ON DELETE <ACTION>` 要寫在一行的最後面：

e.g. `REFERENCES teacher(id) ON DELETE CASCADE`

### 其它 Constraints

e.g. `CHECK (gender = 'Male' OR gender = 'Female')`

### 完整範例

```PostgreSQL
CREATE TABLE student(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    gender VARCHAR(16) NOT NULL CHECK (gender = 'Male' OR gender = 'Female'),
    date_of_birth DATE NOT NULL
);

CREATE TABLE teacher(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(32) NOT NULL
);

CREATE TABLE course(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    tid BIGINT NOT NULL REFERENCES teacher(id) ON DELETE CASCADE
);

CREATE TABLE enrolled(
    cid BIGINT NOT NULL REFERENCES course(id) ON DELETE CASCADE,
    sid BIGINT NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    score NUMERIC(5, 2) CHECK (score >= 0.00 AND score <= 100.00),
    PRIMARY KEY (cid, sid)
);
```

> [!Note]
>在 `course` table 中，雖然 `tid` 為 `teacher` table 的 foreign key: `id`，但 `tid` 的資料型態是 `BIGINT`，不同於 `teacher(id)` 的 `BIGSERIAL`，這是因為 `BIGSERIAL` 會自動 +1，但 foreign key 不需要（不能）自動 +1，所以只需要「可接受數字範圍與 `BIGSERIAL` 一樣」的 `BIGINT` 即可。

# `ALTER`

### 更動 Database 的 Owner

```PostgreSQL
ALTER DATABASE <database_name> OWNER TO <new_owner>;
```

### 新增 Column

```PostgreSQL
ALTER TABLE <table_name> ADD <column_name> <data_type> [<constraints>];
```

e.g.

```PostgreSQL
ALTER TABLE teacher ADD email VARCHAR(256) UNIQUE NOT NULL;
```

### 移除 Column

```PostgreSQL
ALTER TABLE <table_name> DROP COLUMN <column_name>;
```

### 移除 Constraint

- **移除 Primary Key Constraint**

    ```PostgreSQL
    ALTER TABLE <table_name> DROP CONSTRAINT <table_name>_pkey;
    ```

- **移除其他 Constraints**

    每一個 constraint 都會有它的名字，這個名字可能是在定義 constraint 時取的，也可能是 DBMS 自動給的，而若要移除 constraint，則聲明該 constraint 的名字即可（`<table_name>_pkey_` 就是其中一種 DBMS 自動給所有 primary key 的 constraint name）

    ```PostgreSQL
    ALTER TABLE <table_name> DROP CONSTRAINT <constraint_name>;
    ```

# `DROP`

### 刪除 Database Schema

```PostgreSQL
DROP SCHEMA <schema_name> CASCADE;
```

#TODO

# `TRUNCATE`

#TODO

### `TRUNCATE` vs. `DELETE`

`TRUNCATE <table_name>` 的效果等同於 `DELETE FROM <table_name>`，都是將指定表內的所有資料刪除（但不刪除 table 的 schema）。只是 `TRUNCATE` 被歸類為 DDL；`DELETE` 則被歸類為 [[淺談 SQL#^146eea|DML]]。
