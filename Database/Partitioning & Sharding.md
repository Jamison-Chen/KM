# Partitioning

### Horizontal Partitioning

將一個有 n 筆資料的表拆分呈多個表 (partitions)，這些 partition 的資料筆數的總和為 n，每個 partition 的 schema 相同。

### Vertical Partitioning

將一個有 m 個 columns 的表拆分呈多個表 (partitions)，每個 partition 的資料筆數相同，但只會擁有原表的部分 columns。其實可以把 vertical partitioning 想像成多張一對一關係的表。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-vertical-partitioning.png>)

# Sharding

Sharding 算是一種 horizontal partitioning，差別在於 sharding 時，會將各個 partitions (shards) 分散存在不同的 nodes/instances/servers。

通常 sharding 機制會被實作在 application level，開發人員透過 code 來決定要將哪些 users 的哪些 actions 導向哪個 nodes，但也有些 DBMS 自己就可以做到 sharding（比如 MySQL Cluster）。

### Pros & Cons

- Pros
    - 加快 database 存取時間
    - 分散風險
- Cons
    - 系統設計變得更複雜，出問題時也會更難 debug
    - 當涉及的資料分散在不止一個 shards 時，SQL 會變複雜
    - 「JOIN 不同 shards 的資料」這種操作的成本很大，因為必須將要 JOIN 的資料全部拉下來才能 JOIN

# Types of Sharding

### Range-Based Sharding

透過某欄位的值的大小來判斷該筆料應該被分配到哪個 shard。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-range-based-sharding.png>)

- 缺點
    - 無法保證資料被平均地分配到各個 shards
    - 當一筆資料該欄位的值改動，以致於超出該 shard 所接受的範圍時，要將資料搬到其它 shard 嗎？

### Directory-Based Sharding

建一張對照表來紀錄每一個 shard key 應該對應到哪個 shard，分配的規則可以自己定義，通常對照表本身會是一個服務。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-directory-based-sharding.png>)

- 缺點
    - 對照表會是 single point of failure，由於對照表非常頻繁地被存取，因此可能成為整個服務的 bottleneck
- 優點
    - 可以避免各個 shards 中資料量不平均的現象

### Key-Based Sharding (Hash-based Sharding)

選定一張表的某個 column 做為 **shard key**，shard key 必須是靜態的，也就是說當資料被建立後，就不能再更動該資料的 shard key。

選定一個 hash function，此 function 的輸入值為 shard key，輸出值為 shard number，用來安排每一筆資料應被分發到哪個 shard。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-key-based-sharding.png>)

- 缺點
    - 若決定新增一個 node，則必須重新選擇 hash function，並且將所有既存的 shards 中的資料做一次大風吹 (rebalancing)
        - Directory-based sharding 沒有這個問題
- 優點
    - 各個 shard 中的資料量平均
    - 無須另外用一張表紀錄每筆資料存在哪個 shard，因為只要知道 hash function 和 shard key 的值，就可以知道一筆資料會被分配到哪個 shard

# 該不該 Sharding？

由於 sharding 會增加整個後端設計與 debug 的難度，因此非必要時應盡量避免。當以下情況出現時再考慮 sharding：

- 資料量大到單一個 node 空間不夠儲存
- 存取資料庫頻繁到單一個 node 無法 handle，進而導致 timeout

在 sharding 前，你還可以嘗試其它較簡單的手段，這些手段包括：

- [Replicas](</System Design/Database Replication.md>) for read

    Primary database 負責處理「寫入」的 queries，然後將被寫入的資料複製到 secondary databases，secondary databases 負責處理「讀取」的 queries。（但這麼做會導致 consistency 降低）

- Remote Database

    為 database 配置一台專屬的機器，不要跟其它 app components 放在一起。（但這麼做會增加 app 與 database 的溝通時間）

- [Vertical Scaling (Scaling Up)](</System Design/Horizontal Scaling vs. Vertical Scaling.md#Vertical Scaling>)

- Application-Level Caching

    將不久前請求過的資料暫存在 memory（比如 Redis），以供短時間內再次存取。

---

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/db-partitioning-and-sharding.png>)

# 參考資料

- <https://www.digitalocean.com/community/tutorials/understanding-database-sharding>
