>[!Note]
>本文中的 SQL 語法為標準 SQL syntax。實務上，語法可能會因為在不同 DBMS 中而略有差異。

# `CREATE`

### 新增 Database

在 DBMS 中建立一個新的資料庫：

```SQL
CREATE DATABASE {DB_NAME};
```

### 新增 Schema (PostgreSQL)

在 [PostgreSQL 的架構](</Database/PostgreSQL/1 - Introduction.md#PostgreSQL 的架構>)中，可以在 database 與 table 間建立一層 schema：

```SQL
CREATE SCHEMA {SCHEMA_NAME};
```

### 新增 Table

在資料庫中建立新的表。

e.g.

```SQL
CREATE TABLE student(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    gender VARCHAR(16) NOT NULL CHECK (gender = 'M' OR gender = 'F'),
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

- 表中的每個欄位可以有各種 constraints，詳見 [Integrity Constraints](</Database/Integrity Constraints.md>)。

> [!Note]
>在 `course` table 中，雖然 `tid` 為 `teacher` table 的 foreign key: `id`，但 `tid` 的資料型態是 `BIGINT`，不同於 `teacher(id)` 的 `BIGSERIAL`，這是因為 `BIGSERIAL` 會自動 +1，但 foreign key 不需要（不能）自動 +1，所以只需要「可接受數字範圍與 `BIGSERIAL` 一樣」的 `BIGINT` 即可。

# `ALTER`

### 更動 Database Owner

```SQL
ALTER DATABASE {DB_NAME} OWNER TO {NEW_OWNER};
```

### 新增 Column

```SQL
ALTER TABLE {TABLE_NAME}
ADD [COLUMN] {COLUMN_NAME} {DATA_TYPE} [{CONSTRAINTS}];
```

e.g.

```SQL
ALTER TABLE teacher
ADD email VARCHAR(256) UNIQUE;
```

### 更改 Column 的 Schema

- 更改 data type

    ```SQL
    ALTER TABLE {TABLE_NAME}
    ALTER COLUMN {COLUMN_NAME} TYPE {NEW_DATA_TYPE};
    ```

- 更改 column name

    ```SQL
    ALTER TABLE {TABLE_NAME}
    RENAME COLUMN {OLD_COLUMN_NAME} TO {NEW_COLUMN_NAME};
    ```

- 加上 default value

    ```SQL
    ALTER TABLE {TABLE_NAME}
    ALTER COLUMN {COLUMN_NAME} SET DEFAULT {DEFAULT_VALUE};
    ```

- 移除 default value

    ```SQL
    ALTER TABLE {TABLE_NAME}
    ALTER COLUMN {COLUMN_NAME} DROP DEFAULT;
    ```

- 加上 `NOT NULL` constraint

    ```SQL
    ALTER TABLE {TABLE_NAME}
    ALTER COLUMN {COLUMN_NAME} SET NOT NULL;
    ```

- 移除 `NOT NULL` constraint

    ```SQL
    ALTER TABLE {TABLE_NAME}
    ALTER COLUMN {COLUMN_NAME} DROP NOT NULL;
    ```

### 移除 Column

```SQL
ALTER TABLE {TABLE_NAME}
DROP COLUMN {COLUMN_NAME};
```

### 🔥 移除 Primary-Key Column

#TODO 

### 移除 Integrity Constraint

- **移除 Primary Key Constraint**

    ```SQL
    ALTER TABLE {TABLE_NAME}
    DROP CONSTRAINT {TABLE_NAME}_pkey;
    ```

- **移除其它 Constraints**

    每一個 constraint 都會有它的名字，這個名字可能是在定義 constraint 時取的，也可能是 DBMS 自動給的，而若要移除 constraint，則聲明該 constraint 的名字即可（`{TABLE_NAME}_pkey` 就是其中一種 DBMS 自動給所有 primary key 的 constraint name）

    ```SQL
    ALTER TABLE {TABLE_NAME}
    DROP CONSTRAINT {CONSTRAINT_NAME};
    ```

# `DROP`

### 刪除 Database

#TODO 

### 刪除 Schema (PostgreSQL)

Schema 是 PostgreSQL 架構中，介於 database 與 table 間的一層（詳見[本文](</Database/PostgreSQL/1 - Introduction.md#PostgreSQL 的架構>)），可以使用 `DROP` 將其刪除：

```SQL
DROP SCHEMA {SCHEMA_NAME} CASCADE;
```

### 刪除 Table

#TODO 

# `TRUNCATE`

#TODO

### `TRUNCATE` vs. `DELETE`

`TRUNCATE {TABLE_NAME};` 的效果等同於 `DELETE FROM {TABLE_NAME};`，都是將指定表內的所有資料刪除（但不刪除 table 的 schema）不過 `TRUNCATE` 被歸類為 DDL；`DELETE` 則被歸類為 [DML](</Database/SQL/0 - Introduction.md#DML>)。
