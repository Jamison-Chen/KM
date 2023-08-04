![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/elasticsearch-kibana.png>)

>[!Note]
>若想了解如何在雲端建立 Elastic Service 請參考[另一篇文章](https://dev.to/lisahjung/beginner-s-guide-to-setting-up-elasticsearch-and-kibana-with-elastic-cloud-1joh)。

# 安裝與啟動

### Step1: 安裝 [Java](https://www.java.com/en/download/)

由於 Elasticsearch 建構在 Apache Lucene 之上，而 Apache Lucene 是用 Java 寫的，因此要運行 Elasticsearch 就必須先安裝 Java。

### Step2: 下載 [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) 與 [Kibana](https://www.elastic.co/downloads/kibana)

下載的都是壓縮檔，解壓縮後會分別得到名為 `elasticsearch-<VERSION>` 與 `kibana-<VERSION>` 的資料夾。

### Step3: 啟動

###### 啟動 Elasticsearch Server

```bash
cd path/to/elasticsearch
bin/elasticsearch
```

首次啟動時請注意，會有幾項重要資訊列在 terminal 的最後，大概長得像這樣：

```plaintext
ℹ️  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  <PASSWORD>

ℹ️  HTTP CA certificate SHA-256 fingerprint:
  <FINGERPRINT>

ℹ️  Configure Kibana to use this cluster:
• Run Kibana and click the configuration link in the terminal when Kibana starts.
• Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  <TOKEN>
```

>[!Warning]
>上面這些資訊在只有在首次啟動 ES Server 時會出現，因此一定要記錄下來。

###### 啟動 Kibana Server

```bash
cd path/to/kibana
bin/kibana
```

>[!Note]
>Kibana 預設使用 port 5601，Elasticsearch 預設使用 port 9200。

### Step4: 使用瀏覽器開啟 Kibana

URL: <http://localhost:5601>

# Configuration

### 設定檔位置

*（從 elasticsearch 專案根目錄出發）*

./config/elasticsearch.yml

### 更改設定後若要套用，必須重啟 ES Server

### Security

預設狀態下，在 local 開啟 server 後，直接用 `curl`、Postman 或 browser 等工具打 API 到 `localhost:9200` 會得到 empty response，只有透過 Kibana dev tool 才能得到完整的 response，這並不是你的 server 壞了，而是 elasticsearch 在安全性上的一個設定。

若想直接打 localhost 與 ES server 溝通，必須將設定檔中的 `xpack.security.enabled` 設為 `false`（但這樣一來 Kibana dev tool 就不能用了，所以通常不會這麼做）。

# 幾個簡單的 APIs

試試看在 Kibana dev tool 裡呼叫下面這些 APIs，確保 server 有正常運作：

```bash
# Check server health
GET _cluster/health

# List all nodes and their details
GET _nodes/stats

# List all nodes
GET /_cat/nodes?v
```

# 參考資料

- <https://discuss.elastic.co/t/dec-11th-2022-en-running-elasticsearch-and-kibana-v8-locally-macos-linux-and-windows/320174>
- <https://dev.to/lisahjung/beginner-s-guide-to-elasticsearch-4j2k>
