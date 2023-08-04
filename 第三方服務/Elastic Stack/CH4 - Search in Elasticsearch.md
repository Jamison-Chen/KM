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

# Hit

根據 query 搜尋出來的每一個 document 都被稱為一個 **hit**，所有 hits 會依照 **score** 由高至低排序，score 越高代表該 hit 與 query 越相關。

# 如何計算 Score？

### TF-IDF

TF-IDF 是用來衡量「在給定若干個 documents 中，一個 term 在各個 document 中的重要程度」的指標

$$
Term Frequency * Inverse Document Frequency
$$

其中 Term Frequency 代表一個 term 在一個 document 中出現的頻率；Document Frequency 則代表一個 term 在各個 documents 中出現的頻率。

### Query Context & Filter Context

Query context 會影響 score，進而影響搜尋結果的順序；filter context 則是直接將不符合條件的 document 過濾掉。

# Searching

>[!Note]
>接下來示範的 query 都是 for Kibana dev tool ，所以不會有完整的網址。

### Example

假設現在有一個 index 叫`news`，我們可以下一個最簡單的 search query：

```plaintext
GET news/_search
```

會得到像下面這樣的結果：

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

- Array of hits，其中每個 hit 的 `_source` 就是餵入 ES 的 document 的原始值
- 這個 array 只包含部分的搜尋結果，不會等於 `hits.total.value`

---

搜尋的方法主要有兩種：query string 以及 query DSL (Domain Specific Language)。

### Query String

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

### Query DSL (Domain Specific Language)

```plaintext
GET <INDEX_NAME>/_search
{
    "query": {
        "<QUERY_TYPE>": {
            "<FIELD>": <VALUE>
        }
    }
}
```

###### Leaf/Compound Query

以上面的例子來說，`"name": "Amy"` 是 leaf query；compound query 則是由多個 leaf queries 組成。

###### 各式各樣的 Query DSL

Query DSL 的種類有很多，如 full-text query, geo query, shape query, joining query, term-level query… 等，詳見[官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)。

# 參考資料

- <https://dev.to/lisahjung/beginner-s-guide-to-understanding-the-relevance-of-your-search-with-elasticsearch-and-kibana-29n6>
- <https://www.youtube.com/watch?v=CCTgroOcyfM>
