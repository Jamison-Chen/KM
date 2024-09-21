![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/kafka-setup.png>)

### Kafka 生態系

Kafka 是一套開源的「==事件串流平台==」，它提供大規模的 [Message Broker](</System Design/Message-Queuing System.md#Message Broker>) 服務，透過分散式應用程式的架構，每分鐘可處理多達數十億個串流事件，達到建置即時資料處理平台的效果，應用在 [CDC](</System Design/CDC.md>) 也是相當適合的場景。

#TODO 

### Protocol

Kafka 使用的 protocol 不是 [messaging protocols](</Network/Messaging Protocols.draft.md>) 中的任何一個，而是 Kafka 自己獨家的 protocol（也是建構在 TCP/IP 之上），因此你無法輕易使用其他服務取代 Kafka。

#TODO 

# 參考資料

- <https://www.cloudamqp.com/blog/when-to-use-rabbitmq-or-apache-kafka.html>
