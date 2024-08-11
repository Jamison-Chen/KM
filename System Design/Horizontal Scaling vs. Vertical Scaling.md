![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/horizontal-scaling-vs-vertical-scaling.png>)

一個服務的 scalability 指的是其面對大量請求／任務時的應對能力，而 scaling 就是指「擴展 server 應對能力」這個動作。Scaling 的方式分為 horizontal scaling 與 veritcal scaling 兩種。

# Horizontal Scaling

- 又叫做 scaling out
- 透過「增加更多機器」來分擔工作量

Horizontal scaling 勢必會讓系統架構變成分散式系統 (distributed system)，因此設計上會比複雜，原本連貫的程式邏輯可能會須要被拆解 (decouple) 然後佈置到各個不同的機器上，再使用 load balancing 機制來分散流量，機器之間也須要互相溝通。

# Vertical Scaling

- 又叫做 scaling up
- 透過「升級一部機器上的資源 (CPU, RAM...)」使其有能力處理更多任務

Vertical scaling 會較 horizontal scaling 簡單，原因是程式邏輯不用因此有任何變動。不過把雞蛋放在同一個籃子裡的缺點就是比較容易形成 SPoF (single point of failure)。

另外，一台 server 上的 CPU 與 RAM 並不能無止盡地升級，因此 vertical scaling 有上限，通常只適合中小型的服務採用。

# 比較

| |Horizontal Scaling|Vertical Scaling|
|---|---|---|
|Database|[Sharding](</Database/Partitioning & Sharding.md#Sharding>)|多核心處理器|
|Concurrency|[Distributed Programming](</System Design/Distributed Programming.md>)|[Actor Model](</System Design/Actor Model.md>)|
|Messaging|Server 間須互傳資料|沒有此問題|

# 參考資料

- <https://www.section.io/blog/scaling-horizontally-vs-vertically/>
