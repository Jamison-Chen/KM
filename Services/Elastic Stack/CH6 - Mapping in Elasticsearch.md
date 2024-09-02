Mapping 用來定義一個 index 中的所有 documents 必須擁有哪些 fields，以及這些 fields 必須是哪種資料型態，用 relational database 的語言來說：「mapping 就是 index 的 "schema"。」

正確地定義 mapping 可以縮短搜尋時間，並避免儲存空間的浪費：

- 有些 data type 比較適合 full-text search，有些比較適合拿來 sorting
- 有些 field 由於根本用不到，所以不需要建立 index

### 查看一個 Index 的 Mapping

```plaintext
GET <INDEX_NAME>/_mapping
```

Example output:（以 [CH5](</Services/Elastic Stack/CH5 - Aggregation in Elasticsearch.md>) 用到的 `ecommerce` index 為例）

```json
{
  "ecommerce": {
    "mappings": {
      "properties": {
        "CustomerID": {
          "type": "long"
        },
        "InvoiceDate": {
          "type": "date",
          "format": "M/d/yyyy H:m"
        },
        ...
      }
    }
  }
}
```

# Dynamic Mapping

若沒有事先定義一個 index 的 mapping 就直接 index 一個 document，則 Elasticsearch 會自動根據 document 中各 fields 的資料型態決定 mapping，此即 dynamic mapping。

# 與文字相關的資料型態

>[!Note]
>想知道所有的資料型態有哪些，請見[官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)，以下只列舉一些重要的。

### `text`

- 所有英文字母會被轉為小寫
- 標點符號會被去除
- 以空格為斷點將 phrase 切分成一個一個單字 (token)
- 使用 `text` 在 full-text search 會有較好的表現
- 用一種叫做 **Inverted Index** 的資料結構紀錄每個 token 在哪些 doucments 中出現過幾次

### `keyword`

- 將原文字直接記錄下來，不做任何加工
- 使用 `keyword` 在 exact search、aggregation 以及 sorting 時有較好的表現
- 用一種叫做 **doc values** 的資料結構紀錄每個 document 出現什麼值，其實就是一個對照表

在 dynamic mapping 的情況下，所有文字的 fields 都會分別被 map 為 `keyword` 以及 `text`，示意圖如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/keyword-text-double-mapping.png>)

# 自定義 Mapping

### 規則

- 一個 index 的 mapping 必須在「建立 index 時」定義，不能先有 document 在裡面才定義 mapping
- 一個 index 只會有一個 mapping，所以同一個 index 底下的所有 documents 的資料型態必須一致
- 當某個 field 的 data type 被定義好後，就不能修改，只能新增新的 field data type definition
- 如果真的要修改 index 的 mapping，只能另外建立一個 index（名字要與原本的不同）、另外定義一個新的 mapping，然後把 documents 從舊 index [#Reindex](</./Services/Elastic Stack/CH6 - Mapping in Elasticsearch.md#Reindex>) 到新的 index 上
- 用不到的 field 可以不額外使用任何資料結構儲存之
- 若 document 擁有 index 所沒有的 fields，則當該 document 被 index 時，會 dynamic mapping 那些 fields

### Example Query

```plaintext
PUT produce
{
  "mappings": {
    "properties": {
      "botanical_name": {
        "enabled": false
      },
      "country_of_origin": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "date_purchased": {
        "type": "date"
      },
      "description": {
        "type": "text"
      },
      "name": {
        "type": "text"
      },
      "produce_type": {
        "type": "keyword"
      },
      "quantity": {
        "type": "long"
      },
      "unit_price": {
        "type": "float"
      },
      "vendor_details": {
        "enabled": false
      }
    }
  }
}
```

# Reindex

將某個 index 的 documents 搬到另一個 index，通常會這麼做都是因為有改 mapping 的需求。

Example:

```plaintext
POST _reindex
{
  "source": {
    "index": "produce"
  },
  "dest": {
    "index": "produce_v2"
  }
}
```

# Runtime Field

透過對既有 field 進行加工，得到新的值，將此值用一個「新的 field」記錄在 document 上，以便後續使用，這個新 field 就叫做 runtime field。

比如 `produce` index 原本有 `unit_price` 與 `quantity` 兩個 field，可以將 `unit_price` 乘以 `quantity` 得到 `total`，以便未來計算每個月的 total expense：

```plaintext
PUT produce/_mapping
{
  "runtime": {
    "total": {
      "type": "double",
      "script": {
        "source": "emit(doc['unit_price'].value* doc['quantity'].value)"
      }
    }
  }
}
```

你會發現這裡出現的 `"script"` 與 `"source"`，在 [CH5 - Aggregation in Elasticsearch#Aggregation 組合技](</Services/Elastic Stack/CH5 - Aggregation in Elasticsearch.md#Aggregation 組合技>)也出現過，只是多了 `"runtime"` 與 `emit`。

新增成功後，再次查看 mapping 會得到像下面這樣的結果：

```json
{
  "produce": {
    "mappings": {
      "runtime": {
        "total": {
          "type": "double",
          "script": {
            "source": "emit(doc['unit_price'].value* doc['quantity'].value)",
            "lang": "painless"
          }
        }
      },
      "properties": {
        "quantity": {
          "type": "long"
        },
        "unit_price": {
          "type": "float"
        },
        ...
      }
    }
  }
}
```

- `"mappings"` 底下多了 `"runtime"`

Runtime field 可以像是一般 field 一樣用來計算 aggregation：

```plaintext
GET produce/_search
{
  "size": 0,
  "aggs": {
    "total_expense": {
      "sum": {
        "field": "total"
      }
    }
  }
}
```

### Runtime Field 的優點

可以把建立 runtime field 想像成建立一個 function，只有當需要使用到這個 field 時才會即時執行 function 得到結果，所以有以下優點：

- 平時 runtime field 並不像其他實體 field 一樣會佔據 disk 空間
- 即使被參照的 fields 的值有變動，runtime field 的值也不會過時，因為是即時算出來的

# 參考資料

- <https://dev.to/lisahjung/beginner-s-guide-understanding-mapping-with-elasticsearch-and-kibana-3646>
- <https://www.youtube.com/watch?v=FQAHDrVwfok>
