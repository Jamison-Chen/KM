# `SELECT`

### Keyword Order

```SQL
SELECT <欄位>, …  -- [required]

OVER (PARTITION BY <欄位>)  -- [optional]

FROM <表>  -- [optional]

JOIN <表> ON <條件>  -- [optional]

WHERE <條件>  -- [optional]

GROUP BY <欄位>  -- [optional]

ORDER BY <欄位> [ASC | DESC]  -- [optional]

LIMIT <數字> OFFSET <數字>  -- [optional]

HAVING <條件>  -- [optional]
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
INSERT INTO <表>(<欄位1>, <欄位2>, …)
VALUES
    (<值1>, <值1>, …),
    …;
```

若要新增的資料是完整的（每個欄位都有值），則可以省略 column name 不寫：

```SQL
INSERT INTO <表>
VALUES
    (<值1>, <值2>, …),
    …;
```

# `UPDATE`

```SQL
UPDATE <表>  -- [required]

SET
    <欄位> = <值>,  -- [required]
    <欄位> = <值>,
    …

WHERE <條件>  -- [optional]

RETURNING <欄位>  -- [optional]
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
DELETE FROM <表>  -- [required]

WHERE <條件>  -- [optional]

RETURNING <欄位>  -- [optional]
```

- 若沒有 `WHERE` 子句，是刪除該表的所有資料
- 若有 `RETUNING` 子句，則刪完資料後會回傳被刪除的資料的指定欄位
