一個軟體／應用程式／服務的 Scalability 指的是其==面對預期或非預期的大量請求或大量工作時的應對能力==。

# Horizontal Scaling

^adeafe

又叫做 Scaling Out。透過「增加更多機器」來分擔工作量。

通常 Horizontal Scaling 會比複雜，因為原本連貫的程式邏輯可能會需要被拆解，然後佈置到各個不同的機器上，再使用 load balancing 的方式分配工作。

# Vertical Scaling

^21dd5e

又叫做 Scaling Up。透過「升級一部機器上的資源 (CPU, RAM...)」來使機器有能力在相同時間處理更多任務，不過把所有雞蛋都放在同一個籃子裡的缺點就是比較容易發生當機 (downtime and outages)。

Vertical Scaling 會較 Horizontal Scaling 簡單，原因是程式邏輯不用因此有任何變動。

一台 server 上的 CPU 與 RAM 並不可能無止盡地升級，因此 Vertical Scaling 會存在上限，通常會被中小規模的企業採用。

# 比較

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/horizontal-vs-vertical-scaling-diagram.png>)

| |Horizontal Scaling|Vertical Scaling|
|---|---|---|
|Database|[[Sharding vs. Partitioning#^75f2dd]]|多核心處理器|
|Concurrency|[[Distributed Programming]]|[[Actor Model]]|
|Message Passing|Server 間互傳資料|沒有此問題|

# 參考資料

<https://www.section.io/blog/scaling-horizontally-vs-vertically/>
