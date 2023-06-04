一個完整的服務或應用程式中可能會有多個 programs 在運行，面對較複雜的任務時，這些 programs 通常須要互相合作（整合）才能完成任務，常見的整合方式有以下四種：

### File-Based Integration

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue_file-based-integration.png>)

### Shared-Database Integration

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue_shared-db-integration.png>)

### Direct Connection

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue_direct-connection-integration.png>)

### Messaging

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/message-queue_message-broker-integration.png>)

本篇將著重講解 Messaging 這個方法（Message Queue 只是其中的一個 component，所以其實篇名叫 Message Queue 有一點偏頗），以及一些可以用來讓你的應用程式也有 Messaging 機制的服務。

# Messaging System 中的元素

### Message

Program 與 program 之間要傳遞的資料，有時候又被叫做任務、task 或 job，每一個 message 由兩大部分組成：

- Routing info
- Payload

### Producer/Publisher

負責製造 messages，並把 messages 交給 message broker。

### Message Queue

存放 messages 的地方，採用 FIFO 策略，==一個 messaging system 中可能有多個 queues==（所以 message queue 不算是 [[Singular Update Queue]]）。

### Message Broker

負責將 message queue 中的 messages 分配給各個 workers。

### Consumer/Worker

負責處理 message queue 中的 messages。

>[!Note]
>其實在 Producer 與 Message Queue 之間有時候還會有一個叫做 Exchange 的角色，但它並不是基本元素，詳見 [[RabbitMQ 筆記#Exchange/Router]]

# Messaging 機制的特色

### Asynchronous

當 producer 把 message 丟進 message queue 後，不會等 message 被 consumer 處理完才繼續做他事，而是會直接繼續做其他事，這麼做的好處是使用者體驗變得比較好，但缺點是使用者無法單純透過 response 來確認任務是否執行成功。

### 符合 [[SoC]] 精神

- Producer 與 consumer 不用知道彼此是誰，只要知道如何把 message 丟進 message queue 或者如何處理 queue 中的 message 即可，這點相對於 Direct Connection 是一個優勢
- 可以分開開發 Producer, message broker 與 consumer，也可以各自依需求擴張或縮小

### 不怕任務被遺忘

大多數實作 message queue 的方法都是「使用 RAM 將等著被執行的任務依序存起來」，所以不會因為 producer 或 consumer 壞了任務就丟失。但是相對於 file-based 以及 shared-database integration，message queue 的 reliability 還是比較低，因為 RAM 的資料在「queue 自己重啟」後也會不見，反觀 file 與 database 都是存在 disk，資料不會因為重啟就不見。

# AMQP

AMQP 是 Advanced Message Queue Protocol 的縮寫，裡面定義了 Message Queue 應該具備哪些條件，以及[[#各種 Message Queue Models]]。

# 各種 Message Queue Models

### Point-to-Point Queue

這是最基本的 model，一個 message 由一個 consumer 負責。

### Publish-Subscribe Pattern & Fanout Queue

Publish-Subscribe Pattern 與 Fanout Queue 是兩種不一樣的 models，但由於它們長得很像所以放在一起比較好對比。

在 Publish-Subscribe Pattern 中，consumer 又叫 **subscriber**，每個 subscriber 會有自己的 **inbox**，每個 subscriber 也可能會「訂閱」若干個 publishers，當 publisher 發送 message 時，message 會被送往所有有訂閱該 publisher 的 subscribers 的 inbox，如下方示意圖：

>[!Warning]
>下圖的兩個 topic queues 其實有點誤導人，應該理解為 inbox，一個 inbox 只屬於一個 subscriber。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/PubSub.png>)

由此可見 Pub/Sub Pattern 的特色就是一則 message 可能會被不只一個人收到，而這也是 Fanout Queue 與之相像的地方。

只是 ==Fanout Queue 不同於 Pub/Sub Pattern 的地方在於：不是一個 subscriber 一個 inbox，而是多個 subscribers 共用一個 inbox，或者理解成多個 subscribers 共同觀測一個 **topic**==，示意圖如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Fanout.png>)

舉實際的例子或許可以更容易理解兩個的差異：

在 YouTube 中，你可以訂閱若干個 channels，當這些 channels 發布新影片時，你會收到通知，你也可以點開通知中心查看所有通知，每個人的通知中心會因為他訂閱的 channel 不同而有不同的通知，這就是 Pub/Sub Pattern（YouTube channels 是 publishers，你是 subscriber，通知中心就是你的 inbox）。

而 Fanout Queue 最經典的例子就是聊天群組，無論是在 LINE 群組、Slack Channel 或者任何一款遊戲的多人聊天室中，當聊天室內有人發言時，該聊天室內的其他所有人就會收到相同的訊息，所有人的在這個聊天室內所看到的所有訊息都是一模一樣的，一個人可以加入不同的聊天室。在這裡，一個聊天室（群組）就是一個 topic，發訊息的人是 publisher，其他人是 subscibers。

### Priority Queue

就如我們在[[常見的資料結構與 ADT#Priority Queue|資料結構中所學到的概念]]一樣，priority 較高的 message 會優先被送給 consumer。

# Celery + RabbitMQ

Celery 是一個 Python package，它讓你可以用 Python 來「製造 message」以及「處理 message」（在 Celery 中使用的名詞是 **task**），如此一來你的 Python program 就可以同時扮演 producer 以及 consumer；而 RabbitMQ 則是眾多可以用來作為 message broker 服務的其中一個（其他服務如 Kafka），因此 Celery + RabbitMQ 恰好組成了一個完整的 messaging 機制。

>[!Info]
>其實單用 RabbitMQ 就可以完整實現 messaging 機制了，詳情請見 [[RabbitMQ 筆記]]。

# 參考資料

- <https://godleon.github.io/blog/ChatOps/message-queue-concepts/>
- <https://www.redhat.com/architect/architectural-messaging-patterns>
- https://www.rabbitmq.com/tutorials/amqp-concepts.html
