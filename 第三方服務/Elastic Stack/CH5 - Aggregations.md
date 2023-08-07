>Query 用來搜尋資料；Aggregation 則用來「描述」資料。

Aggregation 分為 [[#Metric Aggregation]] 與 [[#Bucket Aggregation]]，無論是哪種 aggreagation，他們都有相同的 pattern：

```plaintext
GET <INDEX_NAME>/_search
{
    "aggs": {
        "<NAME>": {
            "<AGGREGATION_TYPE>": {
                "field": "<FIELD_OF_DOCUMENT>",
                ...
            }
        }
    }
}
```

- `"aggs"` 也可以寫成 `"aggregations"`

# Metric Aggregation

Metric aggregation 用來計算資料的統計數字，包括 `sum`, `min`, `max`, `avg` 與 `cardinality` (unique count)。

e.g.

```plaintext
GET ecommerce/_search
{
  "aggs": {
    "sum_unit_price": {
      "sum": {
        "field": "UnitPrice"
      }
    }
  }
}
```

Output 現在除了 `hits` 外，還多了一個 `aggregations`：

```json
{
  "took": 27,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": 1,
    "hits": [
      ...
    ]
  },
  "aggregations": {
    "sum_unit_price": {
      "value": 1946449.894
    }
  }
}
```

由於 output 預設都會有 10 個 hits，如果不想要看到 hits，可以在 `"aggs"` 的同一層加上 `"size": 0`：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "sum_unit_price": {
      "sum": {
        "field": "UnitPrice"
      }
    }
  }
}
```

### 使用 `stats` 一次取得所有統計數字

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "all_stats_unit_price": {
      "stats": {
        "field": "UnitPrice"
      }
    }
  }
}
```

Outputs:

```json
{
  ...,
  "aggregations": {
    "all_stats_unit_price": {
      "count": 539137,
      "min": 0.001,
      "max": 498.79,
      "avg": 3.6103066456206867,
      "sum": 1946449.894
    }
  }
}
```

>[!Note]
>`stats` 的統計數字不包括 `cardinality`。

# Query 與 Aggregation 併用

很多時候我們並不只想知道所有資料的統計數字，也會想針對某些特定資料做統計，此時可以先用 query 將範圍縮小，再用 aggregation 做統計。

以 `ecommerce` index 為例，若想知道「所有來自德國的訂單中，最高的商品單價是多少」，可以這樣寫：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "query": {
    "match": {
      "Country": "Germany"
    }
  },
  "aggregations": {
    "germany_max_unit_price": {
      "max": {
        "field": "UnitPrice"
      }
    }
  }
}
```

# Bucket Aggregation

Bucket Aggregation 用來將資料「先分組，再統計」，包括：

### `date_histogram` Aggregation

將資料依時間（不一定是 date）分組。

```plaintext
GET <INDEX>/_search
{
  "size": 0,
  "aggs": {
    "<AGG_NAME>": {
      "date_histogram": {
        "field":"<FIELD_NAME>",
        "<INTERVAL_TYPE>": "<VALUE>",
        "order": {
          "_key": "desc"
        }
      }
    }
  }
}
```

###### Interval Type

其中 `<INTERVAL_TYPE>` 分為分種（詳見[官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html#calendar_and_fixed_intervals)）：

|Interval Type|Description|Example Value|
|---|---|---|
|`fixed_interval`|每一組的時長是固定的|`8hr`, `19m`|
|`calendar_interval`|每一組的時長可能會變動|`1M`|

###### Bucket Order

`"order"` field 用來控制 output 的順序，可不寫，預設為 `"_key": "asc"`。

e.g.

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "transactions_by_8_hrs": {
      "date_histogram": {
        "field": "InvoiceDate",
        "fixed_interval": "14D"
      }
    }
  }
}
```

Output:

```json
{
  ...,
  "aggregations": {
    "transactions_by_14_days": {
      "buckets": [
        {
          "key_as_string": "11/25/2010 0:0",
          "key": 1290643200000,
          "doc_count": 19478
        },
        {
          "key_as_string": "12/9/2010 0:0",
          "key": 1291852800000,
          "doc_count": 21731
        },
        ...
      ]
    }
  }
}
```

### `histogram` Aggregation

將資料依任何 numeric-typed field 分組，例如：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "transactions_per_price_interval": {
      "histogram": {
        "field": "UnitPrice",
        "interval": 10,
        "order": {
          "_key": "desc"
        }
      }
    }
  }
}
```

- `"order"` field 可省略，預設為 `"_key": "asc"`

### `range` Aggregation

無論是 `date_histogram` 或者 `histogram`，都只能以固定「組距」區分每一組，如果想要讓每一組的組距不同，就必須使用 `range` aggregation，例如：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "transactions_per_custom_price_ranges": {
      "range": {
        "field": "UnitPrice",
        "ranges": [
          {
            "to": 50
          },
          {
            "from": 50,
            "to": 200
          },
          {
            "from": 200
          }
        ]
      }
    }
  }
}
```

>[!Note]
>定義 range 的順序決定了 output 的順序（不能使用 `"order"` 排）。

### `terms` Aggregation

`term` aggregation 的功能是「統計某 field 所有的值出現的次數，並由多至少列出」，比如若想知道 `ecommerce` index 中，消費次數前五名的 customer，則可以這樣寫：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "top_5_customers": {
      "terms": {
        "field": "CustomerID",
        "size": 5,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```

- `"order"` field 可不寫，預設為 `"_count": "desc"`，也就是列出前 n 名，若改為 `"_count": "asc"` 則會列出最後 n 名

# Aggregation 組合技

很多時候我們知道的資訊不是單一個的 metric aggregation 或 bucket aggregation 可以回答的，此時會需要疊加多個 aggregations。

比如當我想知道 `ecommerce` index 中，daily total revenue 是多少，以及每天有幾個不同的客人，此時就會須要進行以下幾的步驟：

1. 先使用 `date_histogram` aggregation 將資料分成一天一組
2. 再使用 `sum` 將每天的 (`UnitPrice` * `Quantity`) 加總
3. 以及使用 `cardinality` 取得 `CustomerID` 的 unique count

Aggregation 寫起來會像這樣：

```plaintext
GET ecommerce/_search
{
  "size": 0,
  "aggs": {
    "transactions_per_day": {
      "date_histogram": {
        "field": "InvoiceDate",
        "calendar_interval": "day",
        "order": {
          "daily_revenue": "desc"
        }
      },
      "aggs": {
        "daily_revenue": {
          "sum": {
            "script": {
              "source": "doc['UnitPrice'].value * doc['Quantity'].value"
            }
          }
        },
        "number_of_unique_customers_per_day": {
          "cardinality": {
            "field": "CustomerID"
          }
        }
      }
    }
  }
}
```

- 請注意 `"aggs"` 是巢狀地出現
- 第一層 `"aggs"` 的 `"order"` 可以是第二層 `"aggs"` 的其中一個
- 請注意 `"script"` 與 `"scouce"` 的出現時機
    - `"script"` 用來建立臨時的 data field，以這個例子而言就是建立一個 field 儲存每一筆資料的 (`UnitPrice` * `Quantity`)
    - `"source"` 的 value 也是 string，要記得用 `""` 包起來
    - 關於 script 的寫法教學，請見[官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html)
- 請注意 `doc['UnitPrice'].value` 這類的取值方式
    - `doc` 代表每一筆資料
    - 使用 `[]` 聲明要找的 field
    - 使用 `.value` 取該 filed 的值

Output:

```json
{
  ...,
  "aggregations": {
    "transactions_per_day": {
      "buckets": [
        {
          "key_as_string": "12/1/2010 0:0",
          "key": 1291161600000,
          "doc_count": 3096,
          "number_of_unique_customers_per_day": {
            "value": 98
          },
          "daily_revenue": {
            "value": 57458.3
          }
        },
        {
          "key_as_string": "12/2/2010 0:0",
          "key": 1291248000000,
          "doc_count": 2107,
          "number_of_unique_customers_per_day": {
            "value": 117
          },
          "daily_revenue": {
            "value": 46207.28
          }
        },
        ...
      ]
    }
  }
}
```

# 參考資料

- <https://dev.to/elastic/running-aggregations-with-elasticsearch-and-kibana-lni>
- <https://www.youtube.com/watch?v=iGKOdep1Iss>
