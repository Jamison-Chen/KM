一個完整的服務或應用程式背後可能會有多個服務在運行，面對較複雜的任務時，這些服務通常須要互相合作／整合才能完成任務，服務間常見的整合方式有以下四種：

### File-Based Integration

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue-file-based-integration.png>)

### Shared-Database Integration

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue-shared-db-integration.png>)

### Direct Connection

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue-direct-connection-integration.png>)

### Message-Queuing System

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue-message-broker-integration.png>)

Message-queuing system 簡稱 MQ system，本篇將著重講解這個整合方法。

# Components of a MQ System

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/components-of-a-message-queuing-system.png>)

[AMQP](</Network/Messaging Protocols.draft.md>) 定義了一個 MQ system 必備的元素：

### Message

Message 是服務與服務之間要傳遞的資料，每一個 message 由兩大部分組成：

- Routing info
- Payload

其中 ==payload 必須為 serializable 的資料型態==，比如 JSON、protocol buffer… 等。

### Producer/Publisher

負責製造 messages，並把 messages 交給 message broker。

### Message Broker

Message broker 收到來自 producer 的 message 後會送一個 [ACK](</./System Design/Message-Queuing System.md#Acknowledgements>) 給 producer。

Message broker 可以再拆成 message queue、exchange 兩個部分：

##### Message Queue

Messages 排隊的地方就叫做 message queue，每個 queue 都有自己的名字。

從 queue 中取 message 時，原則上採用 FIFO 策略，但也有會將 message 以特定 attribute 排序的 [priority queue](</Data Structures & Algorithms/ADT.draft.md#Priority Queue>)。

Message queue 不算是 [Singular Update Queue](</System Design/Singular Update Queue.md>)，因為==一個 MQ system 中可能有多個 queues==，一個 queue 也可能有不只一個 consumer。

##### Exchange/Router

Exchange（或者叫 router）負責決定每一則 message 要被傳到哪個 queue，queue 與 exchange 之間的關係稱作 **binding**，示意圖如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue-binding.png>)

決定 message 去向的機制有很多種，詳見 [#Message Routing](</./System Design/Message-Queuing System.md#Message Routing>)。

### Consumer/Worker

Consumer（或者叫 worker）負責處理 message queue 中的 messages。

決定 queue 裡的一則 message 要交給哪些／哪個 consumer(s) 的方法有兩種：

- 看看哪些 consumers 有 [subscribe](</./System Design/Message-Queuing System.md#Publish-Subscribe (Pub-Sub)>) 這個 queue，將 message 送給所有 subscribers
- 請 consumers 內部投票決定誰要來處理這個 message（這是比較沒效率的做法）

Consumer 會在收到 message 後，或者處理完 message 後，送一個 [ACK](</./System Design/Message-Queuing System.md#Acknowledgements>) 給 message broker。

>[!Note]
>一個 node 可以同時是 producer 也是 consumer。

# MQ System 的特色

### Asynchronous (Non-Blocking)

當 producer 把 message 交給 message broker 後，不會等 message 被 consumer 處理完才繼續做其它事，而是會直接繼續做其它事。

- Pros：縮短使用者等待 response 的時間，讓體驗變得更好
- Cons：使用者無法單純透過 response 來確認任務是否執行成功

### Acknowledgements

當 producer 把 message 交給 message broker 後，以及 message broker 把 message 交給 consumer 後，收到訊息的一方都會回覆一個「收到」(**ACK**)，若送訊息的一方沒有收到 ACK，就代表 message 沒有成功傳遞。這個機制可以確保每則 message 都有被處理到。

### 符合 [SoC](</System Design/SoC.md>) 精神

- Producer 與 consumer 不用知道彼此是誰、數量有多少，只要認識 message queue 即可
- Producer、message broker 與 consumer 可以分開開發，也可以各自 scale on demand
- Producer and consumer are loosely coupled from each other. 其中一邊壞掉不至於造成整個系統 crash

### 不怕訊息被遺漏

大多數實作 message queue 的方法都是「使用 RAM 將等著被執行的任務依序存起來」，所以不會因為 producer 或 consumer 壞了任務就丟失。

但是相對於 file-based integration 與 shared-database integration，message queue 的 reliability 還是比較低，因為 RAM 的資料在「message borker 重啟」後還是會消失，反觀 file 與 database 都是存在 disk，資料不會因為重啟就不見。

# MQ Patterns

Message queue 主要有兩種模式：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/pub-sub-vs-ptp.png>)

### Publish-Subscribe (Pub-Sub)

在 publish-subscribe pattern 中，consumer 又叫 **subscriber**，每個 subscriber 會有自己的 **inbox**，每個 subscriber 可以「訂閱」若干個 publishers，當 publisher 發送 message 時，message 會被送往所有有訂閱他的 subscribers 的 inbox。

以 YouTube 為例，一個 user 可以訂閱若干個 channels，當這些 channels 發布新影片時，subscribers 會收到通知，每個 user 的通知中心會因為他訂閱的 channels 不同而有不同的通知。

- YouTube channels → publishers
- Users → subscribers
- 通知中心 → inbox

### Point-to-Point (PTP)

一個 message 只會交給一個 consumer（即使有多個 consumers 同時在監聽一個 queue）。大多數的 task queue 屬於 PTP。

# Message Routing

### Unicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/unicast.png>)

- 機制

    Router/exchange 透過 message 的 **routing key** 來決定該 message 要被送到哪個 queue。這樣的 exchange 叫 **==Direct Exchange==**

- 舉例
    - 網路中 client 與 server 間的溝通
    - 藍芽傳輸

### Multicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/multicast.png>)

- 機制

    Router/exchange 根據 topic key，同時將 message 丟給若干個有訂閱該 topic 的 queues。這樣的 exchange 叫 **==Topic Exchange==**

- 舉例
    - Facebook/YouTube 中的直播

### Broadcast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/broadcast.png>)

- 機制

    Router/exchange 將 message 送給所有與自己相連的 queues。這樣的 exchange 叫做 **==Fanout Exchange==**。

- 舉例
    - [ARP query](</Network/MAC Address & ARP.md>)
    - [DHCP discovery](</Network/IP & IP Address.md#DHCP>)

### Anycast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/anycast.png>)

- 機制

    根據某種規則（或隨機）將 message 送進某個 queue。

- 舉例
    - [CDN](</Web Development/CDN.md>) 會根據物理距離、各 server 忙碌程度等因素決定要將請求送給哪個 server
    - Load balancing mechanism

# 相關的第三方服務

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-brokers.png>)

- Nats
- Amazon SQS
- [[RabbitMQ.draft|RabbitMQ]]
- Google Pub/Sub
- [[Kafka.draft|Kafka]]
- Azure Service Bus

# 參考資料

- <https://godleon.github.io/blog/ChatOps/message-queue-concepts/>
- <https://www.redhat.com/architect/architectural-messaging-patterns>
- <https://www.rabbitmq.com/tutorials/amqp-concepts.html>
