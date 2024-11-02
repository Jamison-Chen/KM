# `SELECT`

### Keyword Order

```SQL
SELECT {COLUMN_NAME}, …  -- [required]

OVER (PARTITION BY {COLUMN_NAME})  -- [optional]

FROM {TABLE_NAME}  -- [optional]

JOIN {TABLE_NAME} ON {CONDITION}  -- [optional]

WHERE {CONDITION}  -- [optional]

GROUP BY {COLUMN_NAME}  -- [optional]

ORDER BY {COLUMN_NAME} [ASC | DESC]  -- [optional]

LIMIT {N} OFFSET {M}  -- [optional]

HAVING {CONDITION}  -- [optional]
```

### 使用 `ORDER BY` 排序

- 可以遞增 (`ASC`) 或遞減 (`DESC`)
- 可以聲明 `null` 要一律放最前面還是一律放最後面
- 可以設定多順位
- 可以先經過運算再排序

e.g. `ORDER BY grade DESC, sid ASC, UPPER(name) ASC`

### 使用 `LIMIT` 限制數量

- 通常要搭配 `ORDER BY` 出現
- 可以指定起始位置 (`OFFSET`)
- 可以用來實現 [Pagination](</Database/Pagination.md#Offset Pagination>)

e.g. `LIMIT 10 OFFSET 20`

# `INSERT`

```SQL
INSERT INTO {TABLE_NAME}({COLUMN1}, {COLUMN2}, …)
VALUES
    ({VALUE1}, {VALUE2}, …),
    …;
```

若要新增的資料是完整的（每個欄位都有值），則可以省略 column name 不寫：

```SQL
INSERT INTO {TABLE_NAME}
VALUES
    ({VALUE1}, {VALUE2}, …),
    …;
```

### `INSERT IGNORE INTO`

在 MySQL 可以用 `INSERT IGNORE INTO` 來避免 insert 到一半因為踩到 constraint 而被打斷：

```SQL
INSERT IGNORE INTO {TABLE_NAME}
VALUES
    ({VALUE1}, {VALUE2}, …),
    …;
```

在 PostgreSQL 沒有 `INSERT IGNORE INTO` 的用法，但有 `ON CONFLICT DO NOTHING`：

```SQL
INSERT INTO {TABLE_NAME}
VALUES
    ({VALUE1}, {VALUE2}, …),
    …
ON CONFLICT DO NOTHING;
```

# `UPDATE`

```SQL
UPDATE {TABLE_NAME}  -- [required]

SET
    {COLUMN1} = {VALUE1},  -- [required]
    {COLUMN2} = {VALUE2},
    …

WHERE {CONDITION}  -- [optional]

RETURNING {COLUMN_NAME}  -- [optional]
```

若有 `RETUNING` 子句，則更新完資料後會回傳被更新的資料的指定欄位。

### Update 可以搭配 JOIN 使用

e.g.

```SQL
UPDATE table_a
    JOIN table_b
        ON table_a.id = table_b.aid
SET
    table_b.column_c = table_a.column_d,
    table_b.column_e = 0;
WHERE table_b.column_c IS NULL;
```

# `DELETE`

```SQL
DELETE FROM {TABLE_NAME}  -- [required]

WHERE {CONDITION}  -- [optional]

RETURNING {COLUMN_NAME}  -- [optional]
```

- 若沒有 `WHERE` 子句，是刪除該表的所有資料
- 若有 `RETUNING` 子句，則刪完資料後會回傳被刪除的資料的指定欄位
