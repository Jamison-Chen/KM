# Precision & Recall

### Precision 

Precision 的意義即「被選出來的資料中，有多少是真的與搜尋條件相關的？」

$$
Precision = {True Positive \over True Positive + False Positive}
$$

### Recall

Recall 的意義即「所有與搜尋條件相關的資料中，有多少被選出來？」

$$
Recall = {True Positive \over True Positive + False Negative}
$$

==Precision 與 recall 要一起看，單用其中一個做為指標都是不好的==，因為如過要讓 precision 很高，只要保留相關性極高的搜尋結果就可以做到，但這會使搜尋結果變太少；反之，若要讓 recall 很高，只要回傳「所有」資料，recall 就是 100%，但這就導致太多不相關的結果被回傳。

# 如何計算 Score？

### TF-IDF

TF-IDF 是用來衡量「在給定若干個 documents 中，一個 term 在各個 document 中的重要程度」的指標

$$
Term Frequency * Inverse Document Frequency
$$

其中 Term Frequency 代表一個 term 在一個 document 中出現的頻率；Document Frequency 則代表一個 term 在各個 documents 中出現的頻率。

### Query Context & Filter Context

Query context 會影響 score，進而影響搜尋結果的順序；filter context 則是直接將不符合條件的 document 過濾掉。

# Search Result

>[!Note]
>接下來示範的 query 都是 for Kibana dev tool ，所以不會有完整的網址。

假設現在有一個 index 叫`news`，我們可以下一個最簡單的 search query：

```plaintext
GET news/_search
```

這是一個沒有任何條件的 query，通常用來觀察資料的基本資訊，會得到如下結果：

```JSON
{
  "took": 1,
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
      {
        "_index": "news",
        "_id": "Dc_bu4kBhLg3wTOfFEjh",
        "_score": 1,
        "_source": {
          "date": "2022-09-23",
          "short_description": "Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.",
          "@timestamp": "2022-09-23T00:00:00.000+08:00",
          "link": "https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9",
          "category": "U.S. NEWS",
          "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters",
          "authors": "Carla K. Johnson, AP"
        }
      },
      ...
    ]
  }
}
```

### Hit

根據 query 搜尋出來的每一個 document 都被稱為一個 **hit**，所有 hits 會依照 **score** 由高至低排序，score 越高代表該 hit 與 query 越相關。

###### `hits.total`

- `hits.total.value` 代表搜尋結果的資料筆數，預設最多顯示 10000
- `hits.total.relation` 有兩種可能值：
    - `gte` (greater then or equal to)：代表實際符合的結果比 `hits.total.value` 還多
    - `eq` (equal to)：代表 `hits.total.value` 就是實際符合的結果數

- 若想強制讓 `hits.total.relation` 為 `eq`，則須加上額外的 query：

    ```plaintext
    GET news/_search
    {
      "track_total_hits": true
    }
    ```

###### `hits.hits`

- Array of hits，其中每個 hit 的 `_source` 就是原本餵入 ES 的 document 內容
- 這個 array 只包含部分的搜尋結果，預設顯示前 10 個

# Query

搜尋的方法主要有兩種：

- **Query String**

    ```plaintext
    GET <INDEX_NAME>/_search?q=<KEYWORD>
    ```

    - 可以使用 `*` 作為 wildcard

    - 可以使用 `<FIELD>:<VALUE>` 的方式指定要搜尋的 field

        e.g. `q=name:Amy`

    - 可以使用邏輯運算子

        e.g. `q=name:(Amy OR Bob)`, `q=(name:Amy AND gender:female)`

    - 可以使用 `""` 指定 query string 中各個 word 的出現順序

        e.g. `q="Amy Chen"` 代表 document 中一定要出現 Amy 與 Chen，且 Amy 一定要先出現，==否則就會直接被篩掉==

- **Query DSL (Domain Specific Language)**

    ```plaintext
    GET <INDEX_NAME>/_search
    {
        "query": {
            "<QUERY_TYPE>": {
                <CONDITIONS>
            }
        }
    }
    ```

    - `<CONDITIONS>` 的形式有很多種，可能是一個簡單的 key-value pair，有可能是數個，也有可能 value 又是另外一個 JSON object。

Query DSL 可以進行比較多樣的搜尋，這裡會著重介紹。

### `range` Query

e.g.

```plaintext
GET news/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "2022-06-20",
        "lte": "2022-09-22"
      }
    }
  }
}
```

### `match` Query

e.g.

```plaintext
GET news/_search
{
  "query": {
    "match": {
      "headline": "Khloe Kardashian Kendall Jenner"
    }
  }
}
```

當 match 中的字串包含空格時，預設是使用 OR 搜尋各個被空格分開的單字，以 `"headline": "Khloe Kardashian Kendall Jenner"` 為例，預設是搜尋所有 headline 中有 Khloe 或 Kardashian 或 Kendall 或 Jenner 的 news。

若要使用 AND，則須在 match query 中特別聲明 `operator`：

e.g.

```plaintext
GET news/_search
{
  "query": {
    "match": {
      "headline": {
        "query": "Khloe Kardashian Kendall Jenner",
        "operator": "and"
      }
    }
  }
}
```

須注意，即使使用 AND，也不保證字詞出現的順序相同，以上面的例子來說，搜尋出來的結果的 headline 雖然一定會有 "Khloe", "Kardashian", "Kendall" 和 "Jenner" 這四個字，但不一定會有 "Khloe Kardashian Kendall Jenner" 這個 phrase，若想要搜尋有這個 phrase 的結果，則應使用 [[#match_phrase Query]]。

###### 使用 `minimum_should_match` 控制 Hits 數量

e.g.

```plaintext
GET news/_search
{
  "query": {
    "match": {
      "headline": {
        "query": "Khloe Kardashian Kendall Jenner",
        "minimum_should_match": 3
      }
    }
  }
}
```

### `match_phrase` Query

`match_phrase` query 只會搜尋出與恰好包含指定字串的結果，指定字串不能被切割或調換順序。

e.g.

```plaintext
GET news/_search
{
  "query": {
    "match_phrase": {
      "headline": "Khloe Kardashian Kendall Jenner"
    }
  }
}
```

### `multi_match` Query

`multi_match` query 的功能是「把對不同 fields 搜尋相同關鍵字的 `match` queries 合併成一個 query」，其搜尋結果會等同於多個 `match` queries 的==聯集==，也就是說只要搜尋的字串有出現在 document 的任何一個 fields，該 document 就會被視為 hit。

e.g.

```plaintext
GET news/_search
{
  "query": {
    "multi_match": {
      "query": "Michelle Obama",
      "fields": [
        "headline",
        "short_description",
        "authors"
      ]
    }
  }
}
```

在 `multi_match` query 中，一個 document 是取其每個 fields 的 score 的最大值作為 document 的最終 score。

###### Per-Field Boosting

若想讓某些 fields 所獲得的 score 的權重調高，則可以在 fields 後面加上 `^<NUMBER>` 來調整，`<NUMBER>` 越大權重越高，比如：

```plaintext
GET news/_search
{
  "query": {
    "multi_match": {
      "query": "Michelle Obama",
      "fields": [
        "headline^2",
        "short_description",
        "authors"
      ]
    }
  }
}
```

###### The Phrase Type

加上 `"type": "phrase"` 後，`multi_match` query 的搜尋結果就會變成「多個 `match_phase` queries 的聯集」，比如：

```plaintext
GET news_headlines/_search
{
  "query": {
    "multi_match": {
      "query": "party planning",
      "fields": [
        "headline",
        "short_description"
      ],
      "type": "phrase"
    }
  }
}
```

### `bool` Query

`multi_match` query 雖然可以對不同 fields 搜尋，但其限制是對所有 field 所做的動作都是「搜尋某組關鍵字」，如果要對不同 field 有不同的搜尋條件，無法透過 `multi_match` query 做到，此時就是 `bool` query 派上用場的時候了。

一個 `bool` query 由四個 boolean clauses 組成，它們分別是：

- `must`
- `must_not`
- `should`
- `filter`

###### Pattern

```plaintext
GET name_of_index/_search
{
  "query": {
    "bool": {
      "must": [
        // document 必須完全符合所有列在這裡的條件，才會被視為 hit
      ],
      "must_not": [
        // document 「不完全符合」所有列在這裡的條件，才會被視為 hit
      ],
      "should": [
        // document 若有符合列在這裡的條件，其 score 會較高
      ],
      "filter": [
        // document 必須完全符合所有列在這裡的條件，才會被視為 hit
        // 與 must 的差別是「符合 must 會讓 score 變高，但符合 filter 不會」
      ]
    }
  }
}
```

- 四個 clauses 都是 optional，沒用到就不用特別寫出來
- 增加 should clause 中的條件並不會讓 hits 數量變少，但是會讓你想找的資料被排到更前面

e.g.

```plaintext
GET news/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "headline": "Michelle Obama"
          }
        },
        {
          "match": {
            "category": "POLITICS"
          }
        }
      ]
    }
  }
}
```

>[!Info]
>Query DSL 的種類還有很多，如 geo query, shape query, joining query, term-level query… 等，詳見[官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)。

# 參考資料

- <https://dev.to/lisahjung/beginner-s-guide-to-understanding-the-relevance-of-your-search-with-elasticsearch-and-kibana-29n6>
- <https://www.youtube.com/watch?v=CCTgroOcyfM>
- <https://www.youtube.com/watch?v=2KgJ6TQPIIA>
