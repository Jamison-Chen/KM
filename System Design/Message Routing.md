>[!Info]
>本篇屬於 [Message-Queuing System](</System Design/Message-Queuing System.md>) 的延伸閱讀，尤其建議先理解其中的 [Exchage](</System Design/Message-Queuing System.md#Exchange/Router>)，會比較知道本文在說什麼。

# Unicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Unicast.png>)

### 實現方式

Router/Exchange 透過 message 的 **routing key** 來決定該 message 要被送到哪個 message queue，這樣的 exchange 又叫做 **==Direct Exchange==**。

### 舉例

Web browser (client) 與 Web server 之間的溝通

# Multicast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/multicast.png>)

### 實現方式

可以和 Unicast 一樣使用 Direct Exchange，或者使用 **==Topic Exchange==**。

### 舉例

Facebook/YouTube 中的直播

# Broadcast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/broadcast.png>)

### 實現方式

Router/Exchange 收到 message 後，將 message 送給所有與自己相連的 queues，這樣的 exchange 叫做 **==Fanout Exchange==**。

### 舉例

[[MAC Address & ARP|ARP]]

# Anycast

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/anycast.png>)

### 舉例

[CDN](</Web Development/CDN.md>)

# 參考資料

- <https://www.redhat.com/architect/architectural-messaging-patterns>