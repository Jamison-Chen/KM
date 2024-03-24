![[etl-vs-elt.png]]

E, T, L 三個字分別是 Extract、Transform 以及 Load 的縮寫，是三個對資料所做的動作，而 ETL 與 ELT 分別代表了兩個不同的處理資料的流程 (Data Integration Process)。

在解釋 E, T, L 三個動作具體是什麼，以及 ETL 與 ELT 兩個流程的差別之前，我們必須先瞭解一個根本的問題「為什麼要對資料做這些動作？」

「資料」之所以具有商業價值，原因其實不在於單一筆資料本身，而是在於將眾多資料集合在一起後，可以對它們進行分析，從分析的結果可以延伸出商業策略，這才是價值所在。因此我們需要找一個地方蒐集資料以供日後分析，而那個地方就叫做 Data Warehouse（資料倉儲）。

# Data Warehouse

你可能會問：「資料庫 (Database) 不就是存資料的地方嗎，為什麼不直接拿資料庫的資料來分析就好，還要額外搞一個 Data Warehouse？」確實，額外搞一個 Data Warehouse 需要另外花錢，也需要額外的人力來維護，當商業規模還小時的確沒什麼餘裕也沒什麼必要（甚至根本還沒有資料分析的團隊）。

然而，由於分析資料時，很可能會對資料庫中的「原始資料」進行「重組」，原始資料也未必都是分析時必要的，因此會做「過濾」，這些經過過濾與重組後的 schema 也會需要被存起來，如果把它們全部存在同一個資料庫中，除了命名、誤用等問題以外，也會使得資料庫同時要應付應用程式本身的流量以及分析資料所需的流量。

綜上所述，當商業規模到達一定程度後，通常會額外建制一個專門給分析團隊使用的 Data Warehouse，來將應用程式與分析用的資料做區隔。Data Warehouse 的資料來源會是應用程式所使用的資料庫，所以資料庫必須以「某種方式」將資料拋轉給 Data Warehouse，這裡所說的「方式」包括流程、頻率… 等，而 ETL 與 ELT 就是兩種常見的流程 (Data Integration Process)。

# Extract, Transform and Load

這裡我們將資料的來源稱為 **source system**，資料的去處稱為 **target system**。

### Extract

將資料從 source sysyem 取出，放到 staging area。[[CDC]] 就是一種 extraction 的手段。

### Transform

泛指資料過濾、重組等動作，目的是為了能將資料轉換為 target system 的使用者想要看的樣子。

### Load

將資料從 staging area 載入 target system。

---

### Data Pipeline

Load 之前的動作是由 Data Pipeline 負責執行，因此在 ETL 流程中，data pipeline 負責的就是 `E` + `T` + `L`；在 ELT 流程中，data pipiline 只負責 `E` + `L`。

# ETL

### 優點

- 減少浪費 target system 的儲存空間，因為存進去的都是已經經過清洗的資料
- 由於對使用者的資料進行分析前，需要先對資料進行「去識別化」才符合法規，這可以在 Transform 階段做好，使得 target system 的資料是合規的
- ETL 是相對於 ELT 更成熟（老）的 Data Integration Process，因此工具也比較完善

### 缺點

- 人工維護成本高，因為無論是 target system 要求的資料格式改變，或者 source system 產生的資料格式有變動，data pipeline 都需要進行微調
- Latency 高，因為傳統的 transform 是在 disk 裡執行

在現代的 ETL Data Integration Process 中，Transform 改為在 memory 裡執行，再搭配 [[Kafka]] 這類的 streamed-event platform，可以做到 real-time processing，幾乎完全擺脫了 high latency 這個缺點。

# ELT

在 ELT 中，有專門用來 transform 的工具，如 [dbt](https://docs.getdbt.com/docs/introduction)。

### 優點

- 由於 data pipline 少了 transform 這個工作，因此能夠更快速地將資料從 source system 拋轉到 target system
- 對於 target system 的使用者（通常是分析師）而言彈性比較大，因為幾乎所有資料都直接 load 進 target system 了，使用者可以自行決定要怎麼 transform

### 缺點

- 由於資料並經清洗就直接傳到 target system，因此 target system 的資料也尚未經過去識別化，分析前要記得做，否則不合規

# 參考資料

- <https://www.striim.com/blog/etl-vs-elt-differences/>
