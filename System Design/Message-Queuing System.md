一個完整的服務或應用程式背後中可能會有多個服務在運行，面對較複雜的任務時，這些服務通常須要互相合作／整合才能完成任務，常見的整合方式有以下四種：

### File-Based Integration

![[message-queue_file-based-integration.png]]

### Shared-Database Integration

![[message-queue_shared-db-integration.png]]

### Direct Connection

![[message-queue_direct-connection-integration.png]]

### Message-Queuing System

![[message-queue_message-broker-integration.png]]

本篇將著重講解 Message-Queuing System 這個正整合方法。

# Message-Queuing System 中的元素

在 [[Messaging Protocols|AMQP]] 中定義了一個 message-queuing system 必備的元素：

### Message

Message 是服務與服務之間要傳遞的資料，每一個 message 由兩大部分組成：

- Routing info
- Payload

其中 ==payload 必須為 serializable== 的資料型態，比如 JSON, protocol buffer… 等。

### Producer/Publisher

Producer（或者叫 publisher）負責製造 messages，並把 messages 交給 message broker。

### Message Broker

Message broker 收到來自 producer 的 message 後會送一個 [[#Acknowledgements|ACK]] 給 producer。

下方介紹的 message queue、exchange 都是 message broker 的一部份。

### Message Queue

Messages 排隊的地方就叫做 message queue，每個 queue 都會有自己的名字。

從 queue 中取 message 時，原則上採用 FIFO 策略，但也有會將 message 以特定 attribute 排序的 [[#Priority Queue]]。

Message queue 不算是 [[Singular Update Queue]]，因為==一個 message-queuing system 中可能有多個 queues==，一個 queue 也可能有不只一個 consumer。

### Exchange/Router

Exchange（或者叫 router）負責決定每一則 message 要被傳到哪個 queue，queue 與 exchange 之間的關係稱作 **binding**，示意圖如下：

![[message-queue_concept-binding.png]]

決定 message 去向的機制有很多種，詳見[[Message Routing|本文]]。

### Consumer/Worker

Consumer（或者叫 worker）負責處理 message queue 中的 messages。

決定 queue 裡的一則 message 要交給哪些／哪個 consumer(s) 的方法有兩種：

- 看看哪些 consumers 有 [[#Publish-Subscribe Pattern & Fanout Queue|subscribe]] 這個 queue，將 message 送給所有 subscribers
- 請 consumers 內部投票決定誰要來處理這個 message（這是比較沒效率的做法）

Consumer 會在收到 message 後，或者處理完 message 後，送一個 [[#Acknowledgements|ACK]] 給 message broker。

>[!Note]
>一個 application 可以同時是 producer 也是 consumer。

# 特色

### Asynchronous (Non-Blocking)

當 producer 把 message 交給 message broker 後，不會等 message 被 consumer 處理完才繼續做其他事，而是會直接繼續做其他事，這麼做的好處是使用者體驗變得比較好，但缺點是使用者無法單純透過 response 來確認任務是否執行成功。

### Acknowledgements

當 producer 把 message 交給 message broker 後，以及 message broker 把 message 交給 consumer 後，收到訊息的一方都會回覆一個「收到」(ACK)，若送訊息的一方沒有得到「收到」的回覆，就代表 message 沒有成功傳遞，這個機制可以確保每則 message 都有被處理到。

### 符合 [[SoC]] 精神

- Producer 與 consumer 不用知道彼此是誰，只要知道如何把 message 丟進 message queue 或者如何處理 queue 中的 message 即可，這點相對於 direct connection 是一個優勢
- 可以分開開發 producer, message broker 與 consumer，也可以各自依需求擴張或縮小

### 不怕任務被遺忘

大多數實作 message queue 的方法都是「使用 RAM 將等著被執行的任務依序存起來」，所以不會因為 producer 或 consumer 壞了，任務就丟失。但是相對於 file-based 以及 shared-database integration，message queue 的 reliability 還是比較低，因為 RAM 的資料在「message borker 自己重啟」後也會不見，反觀 file 與 database 都是存在 disk，資料不會因為重啟就不見。

# 各種 Message-Queue Models

### Point-to-Point Queue

這是最基本的 model，一個 message 只會交給一個 consumer。

### Publish-Subscribe Pattern & Fanout Queue

Publish-subscribe pattern 與 fanout queue 是兩種不一樣的 models，但由於它們長得很像所以放在一起比較好對比。

在 publish-subscribe pattern 中，consumer 又叫 **subscriber**，每個 subscriber 會有自己的 **inbox**，每個 subscriber 也可能會「訂閱」若干個 publishers，當 publisher 發送 message 時，message 會被送往所有有訂閱該 publisher 的 subscribers 的 inbox，如下方示意圖：

>[!Warning]
>下圖的 Topic 1 與 Topic 2 應該被理解為 inbox，一個 inbox 只屬於一個 subscriber。

![[PubSub.png]]

由此可見 pub/sub pattern 的特色就是一則 message 可能會被不只一個人收到，而這也是 Fanout Queue 與之相像的地方。

只是 ==fanout queue 不同於 pub/sub pattern 的地方在於：不是一個 subscriber 一個 inbox，而是多個 subscribers 共用一個 inbox，或者理解成多個 subscribers 共同觀測一個 **topic**==，示意圖如下：

![[fanout.png]]

舉實際的例子或許可以更容易理解兩者的差異：

在 YouTube 中，你可以訂閱若干個 channels，當這些 channels 發布新影片時，你會收到通知，也可以點開通知中心查看所有通知，每個人的通知中心會因為他訂閱的 channels 不同而有不同的通知，這就是 pub/sub pattern（YouTube channels 是 publishers，你是 subscriber，通知中心就是你的 inbox）。

而 fanout queue 最經典的例子就是聊天群組，當群組內有人發言時，群組內的其他所有人就會收到相同的訊息，所有人的在這個群組內所看到的所有訊息都是一模一樣的，而一個人可以加入多個群組。在這裡，一個群組就是一個 topic，發訊息的人是 publisher，其他人是 subscibers。

### Priority Queue

就如我們在資料結構中所學到的概念一樣，priority 較高的 message 會優先被送給 consumer。

# 相關的第三方服務

![[message-brokers.png]]

與其說是實現 message-aueuing system，其實更精確的說法是：上面這些服務扮演的角色就是 message borker。

- [[RabbitMQ]]
- [[Kafka]]

# 參考資料

- <https://godleon.github.io/blog/ChatOps/message-queue-concepts/>
- <https://www.redhat.com/architect/architectural-messaging-patterns>
- <https://www.rabbitmq.com/tutorials/amqp-concepts.html>
