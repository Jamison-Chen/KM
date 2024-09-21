### 連線 MongoDB

```bash
mongosh <db_name>

# 若沒有寫 db_name 就連到預設的 db
mongosh
```

---

### 離開 Mongosh

```bash
exit
```

---

### 查看所有 Databases

```mongosh
show dbs
```

---

### 切換 Database

```bash
use <database_name>
```

---

### 查看所有 Collections

>在 MongoDB 中，collection 取代了 SQL 中 table 的角色。

```mongosh
show collections
```

---

### 選擇指定 Collection 中的所有資料

```mongosh
db.<collection_name>.find()
```

---

### 刪除指定 Collection

```mongosh
db.<collection_name>.drop()
```

---
