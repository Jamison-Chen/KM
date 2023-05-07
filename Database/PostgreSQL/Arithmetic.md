### 運算子

運算子包括 `+` (加法)、`-` (減法)、`*` (乘法)、`/` (除法)、`^` (次方)、`%` (模數)、`|/` (平方根)、`@` (絕對值)、`&` (bitwise and)、`|` (bitwise or)、`~` (bitwise not)、`#` (bitwise exclusive or)、`<<` (bitwise shift left)、`>>` (bitwise shift right)

### 整數相除如何得到完整（包括小數）的結果

須先將分母或分子至少一個化為浮點數。

**法一：加 `.0`**

```PostgreSQL
SELECT 2.0/5;
```

**法二：加 `::float`**

```PostgreSQL
SELECT COUNT(DISTINCT gender)::float/COUNT(1) FROM student;
```

---

### Math Functions

常用的 Math Functions 包括：`ceil(x)`、`exp(x)`、`factorial(x)`、`floor(x)`、`gcd(a, b)`、`lcm(a, b)`、`log(b, x)`、`round(v, s)`

# 參考資料

- <https://www.postgresql.org/docs/current/functions-math.html>