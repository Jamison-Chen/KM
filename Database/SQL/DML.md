# `SELECT`

### Keyword Order

```PostgreSQL
SELECT … (欄位) [required]

OVER (PARTITION BY … (欄位)) [optional]

FROM … (表) [optional]

JOIN … (表) ON … (條件) [optional]

WHERE … (條件) [optional]

GROUP BY … (欄位) [optional]

ORDER BY … (欄位) ASC | DESC [optional]

LIMIT … (數字) OFFSET … (數字) [optional]

HAVING … (條件) [optional]
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
- 可以用來實現 [[Pagination (分頁)#Offset Pagination|Pagination]]

e.g. `LIMIT 10 OFFSET 20`

# `INSERT`

```PostgreSQL
INSERT INTO <table_name>(<column_one>, <column_two>, ...)
VALUES
    (<value_for_column_one>, <value_for_column_two>, ...),
    …;
```

若要新增的資料是完整的（每個欄位都有值），則可以省略 column name 不寫：

```PostgreSQL
INSERT INTO <table_name>
VALUES
    (<value_for_column_one>, <value_for_column_two>, ...),
    …;
```

# `UPDATE`

```PostgreSQL
UPDATE <table_name> [required]

SET
    (欄位) = (值), [required]
    (欄位) = (值),
    …

WHERE … (條件) [optional]

RETURNING … (欄位) [optional]
```

若有 `RETUNING` 子句，則更新完資料後會回傳被更新的資料的指定欄位。

# `DELETE`

```PostgreSQL
DELETE FROM <table_name> [required]

WHERE … (條件) [optional]

RETURNING … (欄位) [optional]
```

- 若沒有 `WHERE` 子句，是刪除該表的所有資料
- 若有 `RETUNING` 子句，則刪完資料後會回傳被刪除的資料的指定欄位
