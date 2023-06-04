### Exchange/Router

Exchange 負責決定每一則 message 要被傳到哪個 queue。

Exchange 其實並不存在於 messaging system model 中，這是因為最基本的 messaging system model 假設只有一個 message queue，所以不需要 exchange，然而在 RabbitMQ 的架構中，exchange 已經成為了 producer 與 message queue 之間的必要角色。

示意圖如下：

![[message-queue_concept-binding.png]]

#TODO 
