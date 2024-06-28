# 學習資源

- [GitHub - season1](https://github.com/LisaHJung/Beginners-Crash-Course-to-Elastic-Stack-Series-Table-of-Contents)
- [YouTube - season1](https://www.youtube.com/playlist?list=PL_mJOmq4zsHZYAyK606y7wjQtC0aoE6Es)
- [GitHub - season2](https://github.com/LisaHJung/beginners-guide-to-creating-a-full-stack-Javascript-app-with-Elasticsearch)
- [YouTube - season2](https://www.youtube.com/playlist?list=PL_mJOmq4zsHbcdoeAwNWuhEWwDARMMBta)
- [官方文件](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

# The Elastic Stack

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/elastic-stack.png>)

### Elasticsearch 是 Elastic Stack 的核心

- 是一個提供 **Full-Text Search**（全文搜尋）功能的服務
- 建構在 **Apache Lucene** 之上，兩者都是用 **Java** 寫的
- 使用 [HTTP1.1, HTTP2 & HTTP3](</Network/HTTP1.1, HTTP2 & HTTP3.md>) 做為 application layer，並且使用 [REST API](</Web Development/REST API.md>)（詳見[此段](</./Services/Elastic Stack/CH1 - Intro to Elasticsearch.md#溝通方式>)）
- 接收 **JSON** 格式的 requests，大多時候也回傳 JSON 格式的 responses
- 給定搜尋條件後，可以找出與這些條件「相關」的資料並依相關性排序，不一定要完全相符才找得到（詳見 [CH4 - Search in Elasticsearch](</Services/Elastic Stack/CH4 - Search in Elasticsearch.md>)）

# Elasticsearch 核心概念

```mermaid
flowchart TD
    e1([Elasticsearch])
    i1(Index)
    i2(Index)
    i3(...)
    d1[Document]
    d2[Document]
    d3[...]
    e1 --- i1
    e1 --- i2
    e1 --- i3
    i1 --- d1
    i1 --- d2
    i1 --- d3
```

>如果把 Elasticsearch 類比成 relational database 的話，一個 document 就像是一張表中的一個 tuple；一個 index 就像是一個 relation。

### Document

- 一個 document 有若干個 **fields**，document 以 **JSON** (key-value pairs) 格式呈現
- 一個 document 就是一筆資料，是 indexing 以及 searching 的最小單位
- 每個 document 都有一個 unique ID（可以手動給或自動生成）

### Index

Index 會有一個 human-readable 的名字，比如：product。

>[!Note]
>其實在 Elasticsearch 7.0 前，index 與 document 中間還有一層 **Type**，一個 index 底下可以有若干個 types，type 之下才是 documents，但自 Elasticsearch 6.0 開始，一個 index 底下只能有一個 type，而在 Elasticsearch 7.0 以後，就已經移除 type 這個概念了，取而代之的是 [Mapping](</Services/Elastic Stack/CH6 - Mapping in Elasticsearch.md>)，用來定義一個 index 中的 documents 的每個 fields 應該是什麼資料型態。

# Scalability

### Cluster

一個 cluster 裡會有若干個 **nodes**（一個 node 就是一台 server），每個 cluster 會有一個 unique name 可以透過設定檔設定（預設叫 `elasticsearch`）。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/elastic-cluster-and-nodes.png>)

### Shard

一個 index 可以被分割成多個 shards，然後分散在不同的 nodes 上，會用一個 hash function 來決定每個 document 該去哪個 shard。

將一個 index 分散到多個 nodes（多個 shards）的好處包含：

- 不同 nodes 間可以平行運算，進而縮短搜尋時間
- 可以儲存更多資料
- 分散風險

Shard 可以細分為 **Primary Shard** 與 **Replica**，每個 primary shard 可以有若干個 replicas（預設是 1 個），primary shard 可以寫入與讀取，replica 只能讀取。

Replica 一方面可以提高服務對於 search requests 的吞吐量，也可以用來備援，也因為 replica 的其中一個功能是備援，所以==一個 primary shard 與它的 replicas 一定不會放在同一個 node 上==，不然若 node 掛了，replica 也無法發揮作用。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cluster-node-index-shard.png>)

>[!Note]
>Primary shard 的數量必須在建置 Elasticsearch cluster 的一開始就決定，且==不能修改==，若真的要增加或減少 primary shard，就只能重新建一個 cluster。

# 溝通方式

Elasticsearch 透過 [HTTP1.1, HTTP2 & HTTP3](</Network/HTTP1.1, HTTP2 & HTTP3.md>) 傳送，且使用的是 [REST API](</Web Development/REST API.md>)，預設使用 port 9200。

`curl` request pattern:

```sh
curl -X <REST_VERB> <NODE>:<PORT>/<INDEX>[/<TYPE>[/<ID>]] [<OPTION> ...]
```

e.g.

```bash
curl -X GET http://localhost:9200/person/employee/123

curl -X PUT http://localhost:9200/ecommerce -d '{...}'
```

>[!Note]
>需要對 Elastic server 進行一些設定才能在 local 使用 curl 呼叫 local 的 Elasticsearch API，詳見 [CH2 - 在本機建立 Elastic Service#Security](</Services/Elastic Stack/CH2 - 在本機建立 Elastic Service.md#Security>)。

# 參考資料

- <https://dev.to/lisahjung/beginner-s-guide-to-elasticsearch-4j2k>
- <https://www.youtube.com/watch?v=gS_nHTWZEJ8>
