ICMP 是 internet control message protocol 的縮寫，屬於 [[OSI Model.draft|network layer]] protocol，主要功能是==用來診斷／測試 client 與 server 間的 network routing 是否正常==、封包是否有成功傳遞，比如當封包傳遞失敗時，失敗的那站 router 會回覆一個含有錯誤訊息的 ICMP packet 給 source host，讓 source host 知道封包傳失敗了。

# ICMPv4 vs. ICMPv6

ICMP 分為 ICMP for IPv4 與 ICMP for IPv6，或簡稱 ICMPv4 與 ICMPv6。通常討論 ICMP 時，我們指的都是 ICMP for IPv4（因為現在還是以 IPv4 為主流）對應到的是 [RFC 792](https://datatracker.ietf.org/doc/html/rfc792)；若討論 ICMP for IPv6 則會特別叫它 ICMPv6，對應到的是 [RFC 4443](https://datatracker.ietf.org/doc/html/rfc4443)。

# Connectionless

一個 ICMP packet 通常在 transport layer 會搭配 UDP 使用，所以不須要在送資料前先建立 TCP 連線（不須要進行 TCP three-way handshake）。

# ICMP Packet

一個 ICMP packet 包含 header 與 data 兩大部分：

- Header 中會有 ICMP type、ICMP code、checksum 等資訊
- Data 在 ICMP 出錯時會有值，其內容包括：
    - 整個 IP packet header
    - IP packet body 中，導致錯誤的 first 8 bytes

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/icmp-packet-structure.png>)

# ICMP Types & ICMP Codes

下表為常見的 ICMP types 及其對應的含義：

|ICMP Type|Message|Description|
|:-:|--|--|
|0|Echo reply|Server 收到 `ping` 後的回覆|
|3|Destination unreachable|Client 找不到 server|
|8|Echo|Clinet 主動發送的 `ping`|

其中當 type 為 3 時，還會有不同的 codes 代表不同的錯誤種類，下表為常見的 codes：

|ICMP Code for Type 3|Description|
|:-:|--|
|0|Destination network is unreachable|
|1|Destination host is unreachable|
|2|Destination protocol is unreachable|
|3|Destination port is unreachable|
|6|Destination network is unknown|
|7|Destination host is unknown|

# Network Layer above IP

雖然 ICMP 與 IP 同屬於 network layer protocol，但嚴格來說 ICMP 是在 IP 的上層，所以 ==ICMP packet 會被包在 IP packet payload 中==。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/icmp-ip-ethernet-packet-structure.png>)

# 與 ICMP 相關的指令

- `ping`
- `traceroute`

`ping` 與 `traceroute` 這兩個指令常被 client 用來診斷自己與 destination host 之間的網路狀況，它們使用的都是 ICMP。關於它們的詳細使用方式，請見[本文](</Operating System/Shell/與網路相關的指令.md>)。

# DDoS Attack: ICMP Flood

ICMP 有時候也會被拿來當作一種 [DDoS Attack](</Network/DDoS Attack.canvas>) 的手段，這種攻擊手段叫做 ICMP flood 或 ping flood，原理用極大量的 ICMP requests 使得 server 為了回覆這些 requests 就將資源耗盡，或者將 server 附近網路頻寬佔滿。

# 參考資料

- <https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol>
- <https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/>
- <https://networkdirection.net/articles/network-theory/icmpforipv4/>
