# Partitioning

### Horizontal Partitioning

將一個有 n 筆資料的表拆分呈多個表 (partitions)，這些 partition 的資料筆數的總和為 n，每個 partition 的 schema 相同。

### Vertical Partitioning

將一個有 m 個 columns 的表拆分呈多個表 (partitions)，每個 partition 的資料筆數相同，但只會擁有原表的部分 columns。其實可以把 Vertical Partitioning 想像成多張一對一關係的表。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-vertical-partitioning.png>)

# Sharding

Sharding 與 Horizontal Partitioning 的概念較為接近，差別在於 Horizontal Partitioning 的各個 partitions 被存在同一個 database nodes，但 Sharding 的各個 shards 會被分散存在不同的 database nodes，這些 nodes 各自獨立、不會共用資源，被歸類為 [[Horizontal Scaling & Vertical Scaling#Horizontal Scaling|Horizontal Scaling]] 在 Database 端的實現手段之一。

通常，sharding 機制會被實作在 application level，開發人員透過 code 來決定要將哪些 users 的哪些 actions 導向哪個 database nodes，但也有些 DBMS 自己就可以做到 sharding。

### Sharding 的好處

- 加快 query 時間
- 分散風險

### Sharding 的缺點

- 一旦做了就很難回到 Sharding 前的樣子
- 後端設計變得更複雜，debug 也變得更複雜

### Sharding Architecture

- **Range-based Sharding**

    透過某欄位的值的大小來判斷該筆料應該被分配到哪個 shard。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-range-based-sharding.png>)

    **缺點**

    無法保證資料被平均地分配到各個 shards。

- **Directory-based Sharding**

    建一張對照表來紀錄每一個 shard key 應該對應到哪個 shard，分配的規則可以自己定義。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-directory-based-sharding.png>)

    **缺點**

    - 對照表會是 Single point of failure
    - 由於對照表非常頻繁地被存取，因此可能成為整個服務的 bottlenect

    **優點**

    - 可以避免各個 shard 中資料量不平均的現象

- **Key-based Sharding (Hash-based Sharding)**

    選定一張表的某個 column 做為 "Shard Key"，Shard Key 必須是靜態的，也就是說當資料被建立後，就不能再更動該資料的 Shard Key。

    選定一個 hash function，此 function 的 input 為 shard key，output 為 shard number，用來安排每一筆資料應被分發到哪個 shard。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-key-based-sharding.png>)

    **缺點**

    若決定「新增一個 database node」，則必須重新選擇 hash function，並且將所有既存的 shards 中的資料做一次大風吹。

    **優點**

    - 各個 shard 中的資料量平均
    - 無須另外用一張表紀錄每筆資料存在哪個 shard，因為只要知道 hash function 和 shard key 的值，就可以知道一筆資料會被分配到哪個 shard

### 該不該 Sharding

由於 sharding 會增加整個後端設計與 debug 的難度，因此非必要時應盡量避免。當以下情況出現時再考慮 sharding：

- 資料量大道單一個 database node 空間不夠儲存
- 存取資料庫頻繁到單一個 database node 無法 handle，進而導致 timeout

不過在 sharding 前，你還可以嘗試其他較簡單的手段，這些手段包括：

- Replicas for Read

    Primary Database 負責處理「寫入」的 queries，然後將被寫入的資料複製到 Secondary Databases，Secondary Databases 負責處理「讀取」的 queries。（但這麼做會導致 consistency 降低）

- Remote Database

    為 Database 配置一台專屬的機器，不要跟其他 app components 放在一起。（但這麼做會增加 app 與 database 的溝通時間）

- [[Horizontal Scaling & Vertical Scaling#Vertical Scaling|Vertical Scaling (Scaling Up)]]

- Database Caching

    將不久前 request 過的資料暫存在 memory（比如 Redis），以供短時間內再次存取。

# 參考資料

<https://www.digitalocean.com/community/tutorials/understanding-database-sharding>
