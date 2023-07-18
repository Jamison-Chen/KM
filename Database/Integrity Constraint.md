Integrity Constraint 包括下面四種：

- [Entity-Integrity Constraint](<#Entity-Integrity Constraint>)
- [Referential-Integrity Constraint](<#Referential-Integrity Constraint>)
- [Domain Constraint](<#Domain Constraint>)
- [User-Defined Constraint](<#User-Defined Constraint>)

# Entity-Integrity Constraint

一個 Relation 中的每一筆資料必須是獨一無二的，也就是說至少要有「一個」或「一組」欄位可以作為 primary key，使得每一筆資料都有唯一的 primary key，且所有資料的 primary key 的值都不可為 null。使用一個 relation 的 primary key 可以在該 relation 中找到恰好一筆資料。

# Referential-Integrity Constraint

Relational Database 中，若某個 relation R 的**某欄位 C1 reference 另一個欄位 C2**（同一個 relation 內的或不同 relation 的皆可），則除非 C1 的值為 null，否則都必須對應到「**剛好一筆**」在 C2 欄位具有相同值的資料。

在符合 Referential Integrity 的條件下，C1 在 R1 中就是 Foreign Key，C2 則必須是其所屬之 relation 的 Candidate Key。

### On-Delete Action

On-Delete Action 指的是當 referenced data 要被刪除時，referencing data 的 Foreign Key 要做什麼動作。On-Delete Action 有以下四種：

|Action|Description|
|---|---|
|`CASCADE`|將 referencing data 連同 referenced data 一起刪除。|
|`NO ACTION`|不刪除 referenced data 也不刪除 referencing data。|
|`SET NULL`|將 referencing data 的 Foreign Key 設為 `null`，</br>然後將 referenced data 刪除。|
|`SET DEFAULT`|將 referencing data 的 Foreign Key 設為預設值，</br>然後將 referenced data 刪除。|

# Domain Constraint

規範 Relation 中各個 Columns 可接受的資料型態、長度、範圍等，舉例而言：

```PostgreSQL
CREATE TABLE Employees (
    employee_id int PRIMARY KEY,
    full_name varchar(50) NOT NULL,
    hire_date date NOT NULL,
    salary decimal(10, 2) CHECK (Salary >= 0),
    email varchar(255) UNIQUE
    gender VARCHAR(6) NOT NULL CHECK (gender = 'M' OR gender = 'F'),
);
```

# User-Defined Constraint

一個簡單的 User-Defined Constraint 其實也是一種 Domain Constraint，不過 User-Defined Constraint 可以做到較複雜的限制，比如跨表或跨欄位的值的比較。

比如我希望設定一個「商品售價不得低於成本」的限制，那我可以在 database 層級加上下面這層限制：

```PostgreSQL
ALTER TABLE Product
ADD CONSTRAINT chk_price_greater_than_or_equal_to_cost
CHECK (price >= cost);
```

# 參考資料

- <https://en.wikipedia.org/wiki/Referential_integrity>
- <https://www.scaler.com/topics/dbms/integrity-constraints-in-dbms/>
