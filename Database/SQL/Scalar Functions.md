Scalar function 可能有零到多個 arguments，輸出則必為一個 scalar。

# 常用的 Scalar Functions

### `NOW()`

取得現在的時間。

### `COALESCE(a, b, ...)`

依序看各個傳入的參數，直到看到不是 `null` 的為止，並回傳其值。

e.g. (1)

```SQL
SELECT COALESCE(null, null, 1, 2)
```

Output:

```plaintext
 coalesce 
----------
        1
(1 row)
```

e.g. (2)

```SQL
SELECT COALESCE(email, 'Email Not Exist') FROM student;
```

Output:

```plaintext
                coalesce                 
-----------------------------------------
 fmapstone0@goo.gl
 Email Not Exist
 Email Not Exist
 ndennett3@paginegialle.it
 lbrakespear4@thetimes.co.uk
 lgeraldi5@mapy.cz
 dgauvin6@senate.gov
 arisbridger7@symantec.com
 Email Not Exist
 nfish9@i2i.jp
 eswornea@shop-pro.jp
 ssalzbergb@pinterest.com
(12 rows)
```

---

### `NULLIF(a, b)`

若 a 等於 b，則回傳 `null`。

e.g. *(避免分母出現 0)*

```SQL
SELECT 1.0/NULLIF(COUNT(sid), 0)
FROM student
WHERE name LIKE 'Jami%';
```

---

### `LEFT(<STR>, <N>)` & `RIGHT(<STR>, <N>)`

對字串 `<STR>` 取開頭／結尾的 `<N>` 個字元。

e.g.

```SQL
SELECT user, credit_card_number
FROM credit_card
WHERE LEFT(credit_card_number, 6) IN ('470538', '622688');
```

`LEFT` 與 `RIGHT` 可以用來取代 `LIKE`：

```SQL
SELECT user, credit_card_number
FROM credit_card
WHERE
    credit_card_number LIKE '470538%'
    OR credit_card_number LIKE '622688%';
```

---
