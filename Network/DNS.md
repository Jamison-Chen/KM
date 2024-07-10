#DNS 

DNS 的全名為 domain name system。

網路上每一台 server 的位置都是以 IP address 表示，就像是現實世界裡每個人的住處都有地址，所以 client 必須用 IP address 才能要找到 server，可是 IP address 對人們來說太難記了（想想看，你會記得 `www.google.com` 還是 `142.251.42.228`？）所以後來發展出了一套可以將 IP address 映射到具有語意的英文單字 (domain name) 的系統，就是所謂的 DNS。如此一來，人們就可以透過 domain name 找到想訪問的網站。

# DNS Server

Clients（比如瀏覽器）與大多數的 routers 並不會一開始就知道所有 IP address ↔ domain name 如何 mapping，它們必須問那些專門維護 IP address ↔ domain name map 的 DNS servers，DNS servers 又叫做 **name servers**。

如果你希望人們可以透過某個 domain name 找到你的網站，首先必須要購買該 domain name，然後還必須設定「哪些 DNS servers 負責記錄你的 server's IP address ↔ domain name map」（細節請見[本文](</Web Development/在 GoDaddy 購買 Domain Nme 並指向 AWS EC2 Instance.md>)）。

### DNS 採用分散式、階層式服務架構

為了應付來自全世界 clients 與 routers 的查詢請求，DNS 必須有很好的 scalibility 與 accessibility，因此 DNS 採用分散式的服務架構，在世界各地建置 DNS servers，這可以避免 SPoF (single point of failure)。

另外，DNS 透過階層式架構 (hierarchical) 來達到「將查詢請求分流」與「分散資料儲存位置」的目的。不同層級的 DNS servers 負責解析 domain name 的不同區段，以 `www.google.com` 為例，會有專門解析 `xxx.com` 的 DNS server 與專門解析 `xxx.google.com` 的 DNS server。關於 DNS hierarchy 的細節請見。

# DNS Hierarchy

# DNS Records

DNS record 又叫做 DNS resource record，或者簡記為 RR，分為 **A record**、**CNAME record**、**NS record** 與 **MX record** 四種，細節請見 [DNS Record](</Network/DNS Record.md>)。
