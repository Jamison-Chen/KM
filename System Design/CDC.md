![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cdc.webp>)

CDC 即 Change Data Capture。

當一個應用程式的使用者達到一定數量後，為了確保服務穩定，常常會使用到 [Database Replication](</System Design/Database Replication.md>)；或者有些組織會另外建置專門用來做資料分析的 [Data Warehouse](</System Design/ETL vs. ELT.md#Data Warehouse>) ，上述兩個例子都會需要將資料從一個資料庫 (source database) 同步到另一個資料庫，而 ==CDC 即「source database 捕捉新舊資料的差異、而後將變動的部分拋轉到其他資料庫，使雙方皆保持在最新狀態」的過程==。

# CDC 的實現方式

### Timestamp-Based

根據 source data 的 `created_time` 與 `update_time` 來決定哪些資料該被同步到其他資料庫。

**優點**

- 容易實作、無須其他 tool

**缺點**

- 無法處理與 delete 相關的變動（如刪除單筆資料、刪除 table… 等），需要使用其他方式實作
- 由於必須定期檢查所有資料的 `created_time` 與 `updated_time`，會給資料庫帶來額外負擔
- 有可能不精準，尤其當 `created_time` 與 `updated_time` 可以被手動更改時

### Table Deltas

定期使用 SQL 找出同一個 table 在 source database 與其他資料庫間的差異。

[範例 SQL](https://www.mssqltips.com/sqlservertip/2779/ways-to-compare-and-find-differences-for-sql-server-tables-and-data/)

**優點**

- 能精準捕捉到所有資料的變動（包括 deletion）

**缺點**

- 當資料量夠大時，「找出 tables 間的差異」這件事是相對耗 CPU 資源的

### Trigger-Based

在執行 `UPDATE`, `INSERT`, `DELETE` 等 SQL 後，直接在 SQL 底層觸發同步機制，將同樣的動作也在其他資料庫執行。

**優點**

- 有些 DBMS 有原生的 SQL API 可以達到這個效果

**缺點**

- 每一個 transaction 的時間都會被拉長，以失敗收場的機率也會隨著 replicas 的數量倍數增加

### Log-Based

使用 log files 紀錄每一個 database transaction，這些 log files 中的資料一旦出現了就不會被刪掉，一方面可以在 database 的資料遺失時用來做災害復原，另一方面則可以拿來建置一組一模一樣的資料在其他 database 上。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/log-based-cdc.png>)

Log files 扮演的角色就像是 Message-Queuing System 中的 [Message Queue](</System Design/Message-Queuing System.md#Message Queue>)，事實上，==Log-Based CDC 通常會搭配 Message-Queuing System==（如 [Kafka](</Services/Kafka.draft.md>)），以確保所有 transaction 都有執行在其他 database 上。

**優點**

- 不會像 Trigger-Base CDC 一樣增加 rollback 的機率
- 無須額外的 CPU 資源來檢查每一筆資料的某些欄位，或者檢查兩個 tables 間的差異

**缺點**

- Log 的紀錄方式沒有規定，因此將 log files 裡的資料轉換成 database 看得懂的資訊（通常是 SQL）的難度不一

# 使用 Kafka + Debezium 實現 CDC

[Kafka](</Services/Kafka.draft.md>) 是「事件串流平台」，Debezium 則是「資料流輸出工具」，透過 Debezium Connector 可以串接不同的前台資料源，將數據資料餵進 Kafka Cluster 裡，再引導或調度資料到 Greenplum、Elasticsearch、MongoDB… 等後端資料庫，達到資料同步或數據整合的效果。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/debezium-arch.png>)

# 延伸閱讀

- [運用 Kafka 實現 CDC 資料同步 – 以 MongoDB 為例](https://www.omniwaresoft.com.tw/techcolumn/kafka-techcolumn/using-kafka-for-cdc-with-mongodb/)

# 參考資料

- <https://www.confluent.io/learn/change-data-capture/>
- <https://www.omniwaresoft.com.tw/techcolumn/kafka-techcolumn/what-is-cdc/>
- <https://www.striim.com/blog/change-data-capture-cdc-what-it-is-and-how-it-works/>
