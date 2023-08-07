# `NUMERIC(p, s)`

一個 `NUMRIC` 的整數部位可以到 $2^{17}$ 「位數」，小數部位則可以到 $(2^{14})-1$ 「位數」。

請注意是「位數」，也就是說，在我們熟悉的 10 進制世界中，`NUMERIC` 可以存到 $10^{2^{17}+1}$ 這麼大的數字，小數點則可精細到 $10^{-2^{14}+1}$。

定義 `NUMERIC` 時，`p` (Precision) 表示「總共出現幾個數字」；`s` (Scale) 表示「小數點後出現幾個數字」。

$$
\Huge{\overbrace{173226.\underbrace{62}_{s}}^{p}}
$$

實際上定義 `NUMERIC` 型態的 column 時，`p` 最大只能到 1000。

### 優點：精確度極高

金融與物理領域中對數字精確度的要求極高，因此通常會使用 `NUMERIC` 作為儲存金融或物理相關數據的資料型態。

### 缺點

1. **無法**儲存 `Infinity`, `-Infinity`, `NaN` 這三種值
2. 運算上較耗效能

# `REAL`

`REAL` 又可以寫做 `FLOAT4`，可見是由 4 bytes (32 bits) 組成的，關於在計算機中如何利用這 32 bits 表示小數，詳見 [[如何表示浮點數]]。

### 優點

1. 可以儲存 `Infinity`, `-Infinity`, `NaN` 這三種值
2. 運算上相對而言最不耗效能

### 缺點：排擠效果

小數點後可表示的位數會因為整數部位越多位數而越少。

# `DOUBLE PRECISION`

`DOUBLE PRECISION` 又可以寫做 `FLOAT8`，可見是由 8 bytes (64 bits) 組成的，因此可以表示數字的總位數是 `REAL` 的兩倍。

### 優點

可以儲存 `Infinity`, `-Infinity`, `NaN` 這三種值

### 缺點：排擠效果

小數點後可表示的位數會因為整數部位越多位數而越少。

# 參考資料

- <https://learnsql.com/blog/postgresql-data-types/>
- <https://learnsql.com/blog/understanding-numerical-data-types-sql/>
