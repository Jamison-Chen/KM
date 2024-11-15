定義 database relation schema 時，我們可以為 relation 中的每個 columns 加上一些「限制」，比如可填入的資料型態、長度、資料的唯一性... 等，適當的限制可以讓資料庫更好管理。這些限制又叫做 integrity constraints，integrity constraint 可以分成下面三類：

1. [Entity-Integrity Constraint](<#Entity-Integrity Constraint>)
2. [Referential-Integrity Constraint](<#Referential-Integrity Constraint>)
3. [Domain-Integrity Constraint](<#Domain-Integrity Constraint>)

# Entity-Integrity Constraint

如果一張表中有「一個」或「一組」column(s) 的值在整張表中具有「唯一性」，那我們就可以利用這個特性精準地找到每一筆我們想找的資料，因此通常我們會為每張表定義一個／組這樣的欄位，當然，一張表中也可以有不只一個／組欄位具有唯一性。

在定義 relation 時，通常為找到其中一個／組具有唯一性的 column(s) 將其設定為這個 relation 的 **Primary Key**，而「定義 primary key」這個動作就是在為這個 relation 建立一個 entity-integrity constraint。

### SQL Example

- 在建表時為某個欄位加上 entity-integrity constraint：
    - Single-column primary key

        ```SQL
        CREATE TABLE users (
            user_id INT PRIMARY KEY,  -- This is the entity-integrity constraint
            first_name VARCHAR(50),
            last_name VARCHAR(50)
        );
        ```

    - Multi-column primary key

        ```SQL
        CREATE TABLE orders (
            order_id INT,
            product_id INT,
            quantity INT,
            PRIMARY KEY (order_id, product_id)  -- Multi-column primary key
        );
        ```

- 為已經存在的表的某個欄位加上 entity-integrity constraint：
    - Single-column primary key

        ```SQL
        ALTER TABLE users
        ADD CONSTRAINT pk_user_id PRIMARY KEY (user_id);
        ```

    - Multi-column primary key

        ```SQL
        ALTER TABLE orders
        ADD CONSTRAINT pk_orders PRIMARY KEY (order_id, product_id);
        ```

# Referential-Integrity Constraint

在 relational database 中，若某個 relation R 的某欄位 C1 reference 另一個欄位 C2（同一個 relation 內的或不同 relation 的皆可）則除非 C1 的值為 null，否則都必須對應到「剛好一筆」在 C2 欄位具有相同值的資料。

在符合 referential integrity 的條件下，C1 在 R 中就是 **Foreign Key**，C2 則必須是其所屬之 relation 的 **Candidate Key**。

### `REFERENCES` Constraint

用來聲明一個作為 **foreign key** 的 column 是參照哪個 table 的哪個 column。

### On-Delete Action

On-delete action 指的是當 referenced data 要被刪除時，referencing data 的 foreign key 要做什麼動作。On-delete action 有以下四種：

|Action|Description|
|---|---|
|`CASCADE`|將 referencing data 連同 referenced data 一起刪除。|
|`NO ACTION`|不刪除 referenced data 也不刪除 referencing data。|
|`SET NULL`|將 referencing data 的 foreign key 設為 `null`，</br>然後將 referenced data 刪除。|
|`SET DEFAULT`|將 referencing data 的 foreign key 設為預設值，</br>然後將 referenced data 刪除。|

- `ON DELETE` 要寫在一行的最後面

### SQL Example

- 在建表時為某個欄位加上 referencial-integrity constraint：

    ```SQL
    CREATE TABLE orders (
        ...,
        customer_id INT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
    );
    ```

- 為已經存在的表的某個欄位加上 referencial-integrity constraint：

    ```SQL
    ALTER TABLE orders
    ADD CONSTRAINT fk_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;
    ```

# Domain-Integrity Constraint

規範 relation 中各個 columns 可接受的資料型態、長度、範圍等，可以細分為以下幾種：

### `NOT NULL` Constraint

有此 constraint 的 column 不得出現 `null`，否則可以。

### `UNIQUE` Constraint

有此 constraint 的 column 不得出現重複的資料，否則可以。

與 `PRIMARY KEY` constraint 類似，`UNIQUE` constraint 可以加在單一 column 或者是一組 columns 上，當加在單一 column 上時，通常會與 column 的其它定義寫在同一行；若是一組 columns 則須另外寫一行，並用 `()` 包住 columns。

```SQL
email VARCHAR(256) UNIQUE

UNIQUE (a, b)
```

>[!Note]
>`UNIQUE` constraint implies `NOT NULL` constraint.

### `CHECK` Constraint

比如我希望設定一個「商品售價不得低於成本」的限制，那我可以在 database 層級加上下面這層限制：

```SQL
ALTER TABLE Product
ADD CONSTRAINT chk_price_greater_than_or_equal_to_cost
CHECK (price >= cost);
```

其他範例：

```SQL
CHECK (gender = 'M' OR gender = 'F')
```

---

### SQL Example

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

>[!Note]
>定義 table schema 時，若一個 column 有設定 `DEFAULT {VALUE}`，則若 insert data 時沒有給該 column 值，RDBMS 會自動填上 default value：
>
>e.g.
>
>```SQL
>...
>name VARCHAR(32) NOT NULL DEFAULT ''
>...
>```

# 延伸閱讀

- [DDL](</Database/SQL/DDL.draft.md>)

# 參考資料

- <https://en.wikipedia.org/wiki/Referential_integrity>
- <https://www.scaler.com/topics/dbms/integrity-constraints-in-dbms/>
