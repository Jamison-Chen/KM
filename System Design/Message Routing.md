>[!Info]
>本篇屬於 [Message-Queuing System](</System Design/Message-Queuing System.md>) 的延伸閱讀，尤其建議先理解其中的 [exchage](</System Design/Message-Queuing System.md#Exchange/Router>)，會比較知道本文在說什麼。

# Unicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Unicast.png>)

### 機制

Router/exchange 透過 message 的 **routing key** 來決定該 message 要被送到哪個 queue。這樣的 exchange 叫 **==Direct Exchange==**

### 舉例

- 網路中 client 與 server 間的溝通
- 藍芽傳輸

# Multicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/multicast.png>)

### 機制

Router/exchange 根據 topic key，同時將 message 丟給若干個有訂閱該 topic 的 queues。這樣的 exchange 叫 **==Topic Exchange==**

### 舉例

- Facebook/YouTube 中的直播

# Broadcast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/broadcast.png>)

### 機制

Router/exchange 將 message 送給所有與自己相連的 queues。這樣的 exchange 叫做 **==Fanout Exchange==**。

### 舉例

- [ARP query](</Network/MAC Address & ARP.md>)

# Anycast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/anycast.png>)

### 機制

根據某種規則（或隨機）將 message 送進某個 queue。

### 舉例

- [CDN](</Web Development/CDN.md>) 會根據物理距離、各 server 忙碌程度等因素決定要將請求送給哪個 server
- Load balancing mechanism

# 參考資料

- <https://www.redhat.com/architect/architectural-messaging-patterns>