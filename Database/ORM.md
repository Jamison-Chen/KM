![[orm.png]]

ORM 是 object-relational mapping 的縮寫，顧名思義，就是將 relational database 的概念 mapping 到 OOP (object-oriented programming)，讓開發者可以用操作物件的方式取代寫 SQL。

# Pros & Cons

### 優點

- 在撰寫與資料庫溝通相關的 application code 時，可以用更具語意（更好理解）的方式撰寫
- ORM 會幫你做好 SQL injection 的預防
- 降低 codebase 與資料庫的相依性，當底層的資料庫抽換時，application code 不用跟著改，因為 ORM 會根據不同連接的資料庫執行該資料庫專用的語法

### 缺點

- 因為 SQL 不是自己寫的，所以須要時時注意有沒有產生 N+1 query
- 要額外花時間學習 ORM 的使用方法，同時還不能忘記怎麼寫 SQL
- 並非所有 SQL 都可以找到對應的 ORM 語法

# 參考資料

- [Object–relational impedance mismatch (WikiPedia)](https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch)
