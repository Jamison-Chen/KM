# Create an Index

```plaintext
PUT {INDEX_NAME}
```

# Index a Document

>[!Note]
>這裡使用 "index" 當作動詞，其實就是 "create" 的意思。

有兩種方式可以新增 document：

- `POST`：由 Elasticsearch 自動生成 document ID
- `PUT`：手動指定 document ID

### `POST`

```plaintext
POST {INDEX_NAME}/_doc
{
    "{FIELD}": {VALUE},
    ...
}
```

### `PUT`

```plaintext
PUT <INDEX_NAME>/_doc/<ID>
{
    "{FIELD}": {VALUE},
    ...
}
```

### 可以重複 `PUT` 給相同的 ID 嗎？

當我們成功 index 一個 document 時，會收到像下面這樣的 response：

```JSON
{
  "_index": "produt",
  "_id": "J69vqYkBL8M9hEWCGggE",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```

可以注意到 `"_version": 1` 與 `"result": "created"`。若使用 `PUT` 再次指派值給相同的 ID，則會被視為在==覆寫資料==，且會看到 `_version` 的值變大，同時 `result` 變為 `updated`：

```JSON
{
  "_index": "product",
  "_id": "J69vqYkBL8M9hEWCGggE",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 1
}
```

若要避免上述情況發生，可以使用 `_create` endpoint。

### The `_create` Endpoint

一樣使用 `PUT` method，但 path 使用 `_create` 取代原本的 `_doc`：

```plaintext
PUT {INDEX_NAME}/_created/{ID}
{
    "{FIELD}": {VALUE},
    ...
}
```

此時若 `{ID}` 已經存在，就會無法 index，並得到錯誤訊息：

```JSON
{
  "error": {
    "root_cause": [
      {
        "type": "version_conflict_engine_exception",
        "reason": "[J69vqYkBL8M9hEWCGggE]: version conflict, document already exists (current version [1])",
        "index_uuid": "dwzUmSrWRh-SX8JTi-nojw",
        "shard": "0",
        "index": "product"
      }
    ],
    "type": "version_conflict_engine_exception",
    "reason": "[J69vqYkBL8M9hEWCGggE]: version conflict, document already exists (current version [1])",
    "index_uuid": "dwzUmSrWRh-SX8JTi-nojw",
    "shard": "0",
    "index": "product"
  },
  "status": 409
}
```

# Read a Document

```plaintext
GET {INDEX_NAME}/_doc/{ID}
```

Example output:

```JSON
{
  "_index": "product",
  "_id": "J69vqYkBL8M9hEWCGggE",
  "_version": 1,
  "_seq_no": 2,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "name": "Test Product",
    "price": 300,
  }
}
```

# Update a Document

```plaintext
POST {INDEX_NAME}/_update/{ID}
{
    "doc": {
        "{FIELD}": {VALUE},
        ...
    }
}
```

- 可以只更改部分欄位，沒聲明到的欄位不會因此消失（與[[#可以重複 PUT 給相同的 ID 嗎？|覆寫]]不同）
- 若指定的 `{ID}` 不存在，則無法 update
- 若指定的 `{ID}` 存在，但指定的欄位原本不存在於該筆資料，則視為為該筆資料新增一個欄位
- 可以指派與目標欄位原值型別不同的資料，比如指派 string 給一個原本是 number 的欄位
- Update 成功後，該筆資料的 `_version` 會 +1，但若 update 前後的資料內容完全相同就不會 +1

# Delete a Document

```plaintext
DELETE {INDEX_NAME}/_doc/{ID}
```

- Delete 一個 ID 後，該 ID 的 `_version` 會 +1
- 若 delete 一個不存在的 ID，則 response 的 HTTP code 會是 404，但是該 ID 的 `_version` 還是會 +1

# List All Indices

```plaintext
GET /_cat/indices?v
```

Example output:

```plaintext
health status index                                                        uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .internal.alerts-observability.metrics.alerts-default-000001 F8YET_tfQmyuhDPaMmZPJw   1   0          0            0       247b           247b
yellow open   product                                                      dwzUmSrWRh-SX8JTi-nojw   1   1          1            0        5kb            5kb
green  open   .internal.alerts-observability.logs.alerts-default-000001    b_sKoaPYQDCU9MCN2m2Fng   1   0          0            0       247b           247b
green  open   .internal.alerts-observability.uptime.alerts-default-000001  OK6HF3FkRlSL2Kz5-ENyqw   1   0          0            0       247b           247b
green  open   .fleet-file-data-agent-000001                                I3QLviiYSgWMbx4Zc_onCw   1   0          0            0       247b           247b
green  open   .fleet-files-agent-000001                                    2DWK1XubQziS9G_1R80qZw   1   0          0            0       247b           247b
green  open   .internal.alerts-security.alerts-default-000001              Cdi56EDTTrSFxO_jZWypIA   1   0          0            0       247b           247b
green  open   .internal.alerts-observability.slo.alerts-default-000001     FnkdMkCHTWC0pZHfsrl9FA   1   0          0            0       247b           247b
green  open   .internal.alerts-observability.apm.alerts-default-000001     3yIar2zBSSuLfOCyGXOefA   1   0          0            0       247b           247b
```

- 這個 endpoint 回傳的資料不是 JSON
- `pri` 這個 column 代表 primary shard，`rep` 則代表 replica shard
- 以 `.` 開頭的 indices 是 hidden indices

# Delete an Index

```plaintext
DELETE {INDEX_NAME}
```

# 參考資料

- <https://dev.to/lisahjung/beginner-s-guide-to-performing-crud-operations-with-elasticsearch-kibana-1h0n>
- <https://www.youtube.com/watch?v=gS_nHTWZEJ8>
