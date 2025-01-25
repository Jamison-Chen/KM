#DNS 

DNS 的全名為 domain name system，domain name 即「網域名稱」。網路上每一台 server 的位置都是以 IP address 表示，就像是現實世界裡每個人的住處都有地址，所以 client 必須用 IP address 才能要找到 server，可是 IP address 對人們來說太難記了（想想看你會記得 `google.com` 還是 `142.251.42.228`？）所以後來發展出了一套可以將 IP addresses 對應到具有語意的英文單字 (domain name) 的系統，就是所謂的 DNS，如此一來，人們就可以透過 domain name 找到想訪問的網站。

# FQDN

FQDN 為 fully-qualified domain name 的縮寫，又叫做 absolute domain name，白話文就是「完整的 domain name」。比如 `facebook.com` 就是一個 FQDN，但 `*.com` 或 `*.google.com` 就不是 FQDN。

# DNS Server

Clients（比如瀏覽器）與大多數的 routers 並不會一開始就知道所有 IP address ↔ domain name 如何對應，它們必須問那些專門維護 IP address ↔ domain name map 的 DNS servers，DNS server 也常被簡稱為 **name server**。

如果你希望人們可以透過某個 domain name 找到你的網站，首先必須要購買該 domain name，然後還必須設定「哪些 DNS servers 負責記錄你的 server's IP address ↔ domain name map」（關於網域購買與設定的細節，請見[本文](</Web Development/在 GoDaddy 購買 Domain Nme 並指向 AWS EC2 Instance.md>)）。

# DNS Hierarchy

![[dns-hierarchy.png]]

為了應付來自全世界 clients 與 routers 的查詢請求，DNS 必須有很好的 scalibility 與 accessibility，因此 DNS 採用==分散式架構==，在世界各地建置 DNS servers，避免 SPoF (single point of failure)。

另外，DNS 透過==階層式架構==來達到「將查詢請求分流」與「分散資料儲存位置」的目的。不同層級的 DNS servers 負責解析 domain name 的不同區段，以 `www.google.com` 為例，會有專門解析 `*.com` 的 DNS server 與專門解析 `*.google.com` 的 DNS server。

以下將逐一介紹不同層級的 DNS servers：

### Root Name Servers

Root name servers 是整個 DNS hierarchy 的最頂層，全世界只有 13 個 IP addresses 可以找到 root name servers。最早期真的就只有 13 個 root name servers，大部分在美國境內，但後來發展成每個 IP address 後面都有一群 server clusters，且在美國、歐洲、日本都有，現在總計有 600 多台 root name servers。不過由於當初的設計，這個架構中最多還是只能有 13 個 IP addresses 可以作為查詢入口。

### TLD Servers

TLD 是 top-level domain 的縮寫，top-level domain 指的是 domain name 的最後一段，也就是最後一個 `.` 到第一個 `/` 前的字串。常見的 TLD 如 `.com`、`.org`、`.edu` 等。

每一個 TLD server 都有其專門負責解析的 TLD，比如有人不知道 `google.com` 的 IP address，就可以去問負責 `*.com` 的 TLD server"s"（不只一台），但這些負責 `*.com` 的 TLD servers 無法解析 `wikipedia.org`。

>[!Question] 我的 Domain Name 要用什麼 TLD？
>註冊 domain name 時，你會發現 TLD 並不能隨意取名，通常你必須從現有的 TLD 中選一個。
>
>目前有超過 1000 種不同的 TLD（列表[見此](https://data.iana.org/TLD/tlds-alpha-by-domain.txt)）。
>
>TLD 由 [ICANN](https://www.icann.org/) 負責維護，若想要有新的 TLD 也須向他們提出申請（通常要花很多時間跟錢）。

### Authoritative Name Servers

- Authoritative name servers 負責解析 domain name 末兩段，也就是倒數第二個 `.` 到第一個 `/` 前的字串
- 一個 authoritative name server 只負責一個 2LD (second-level domain) + TLD pair，所以負責解析 `*.google.com` 的 authoritative name server 就不知道 `*.facebook.com` 的 IP address；負責 `*.github.com` 的 authoritative name server 就不知道 `*.github.io` 的 IP address
- Authoritative name server 可能是由擁有它的組織自己維護，也可能是由 ISP (internet service provider) 所維護
- ==Authortative name server 是整個 DNS hierarchy 的最底層==，因此不論前面帶什麼 sub-domain，都會由同一個 authoritative name sever 負責解析，而不同 sub-domain 所對應的行為是由服務內部的 [reverse proxy](</System Design/Forward Proxy & Reverse Proxy.md>) 決定的

### Local DNS Servers

==Local DNS servers 其實不算在 DNS hierarchy 中==，只是它會參與 DNS lookup。所有源頭的 client（比如你使用的電腦）如果自己不知道 IP address，一定是去問離自己最近的那台 local DNS server，所以 local DNS server 又叫做 **default name server**。

一台 local DNS server 可能同時也是 authoritative name server，所以如果剛好 client 問的 2LD + TLD 是同一台 server 所維護的，就可以稍微省掉一點溝通時間。

# DNS Lookup

當 client 不知道某個 domain name 所對應的 IP address 時，就會到外部網路進行查詢，這個動作稱為 DNS lookup，或叫 DNS resolve。DNS lookup 分為 iterative 與 recursive 兩種進行方式。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/dns-recusive-vs-interative.png>)

### Iterative Approach

假設 local DNS server 要查詢 `mail.google.com` 的 IP address，首先它要去跟 root name server 拿「負責解析 `*.com` 的 TLD server 的 IP address」，得到答案後再去跟負責解析 `*.com` 的 TLD server 拿「負責解析 `*.google.com` 的 authoritative server 的 IP address」，得到答案後再去跟負責解析 `*.google.com` 的 authoritative server 拿「`mail.google.com` 的 IP address」。

### Recursive Approach

假設 local DNS server 要查詢 `mail.google.com` 的 IP address，它只須要去問 root name server 就可以拿到答案，可是其實 root name server 為了知道答案，會去問負責解析 `*.com` 的 TLD server；負責 `*.com` 的 TLD server 為了知道答案，會去問負責解析 `*.google.com` 的 authoritative server；負責解析 `*.google.com` 的 authoritative server 知道最終答案，所以回覆給負責 `*.com` 的 TLD server，負責 `*.com` 的 TLD server 再回覆 root name server，最後 root name server 再回覆 local DNS server。

### 比較

先講結論：「Iterative approach 優於 recursive approach。」主要有以下兩個原因：

- 是否有效利用 local DNS server 的 cache？

    以上面 `mail.google.com` 的例子來說，若採用 recursive approach，則 local DNS server 只能 cache 住 `mail.google.com` 的 IP address，下次若有人問 `drive.google.com` 的 IP address，local DNS server 就要再完整地走一次 DNS lookup 的流程。

    反之若採用 iterative approach，則 local DNS server 可以額外記住 TLD server 與 authoritative server 的 IP addresses，所以下次若有人問 `drive.google.com` 的 IP address，local DNS server 可以直接去問負責解析 `*.google.com` 的 authoritative server；同理，若有人問 `facebook.com` 的 IP address，local DNS server 也可以跳過 root name server，直接去跟負責解析 `*.com` 的 TLD server 拿「負責解析 `*.facebook.com` 的 authoritative server 的 IP address」。

    所以使用 iterative approach 可以減少 root name server 與 TLD server 的 loading。

- Pending requests

    若採用 recursive approach，則 root name server 在還沒拿到 TLD server 的回覆前都不會回覆給 local DNS server，所以這個 request 在這段期間就會一直佔用著 root name server 的一個 thread，類似的問題也會發生在 TLD server 上。

    反觀 iterative approach 就沒有 pending 的問題。

# DNS Records

DNS record 又叫做 DNS resource record，或者簡記為 RR，分為 **A record**、**CNAME record**、**NS record** 與 **MX record** 四種，細節請見 [DNS Record](</Network/DNS Record.md>)。

# DNS Server Cache

- 每一個層級的 DNS server 上都會有 cache，會將查詢的結果暫存，如果下次有人問相同的問題就可以直接使用 cache 裡的資料
- 在每個 DNS record 上都必須註明 TTL (time to live)，控制該 record 可以被 cache 多久
- 當一個 domain name 背後的 IP address 更動後，一開始會只有負責解析的 authoritative name server 知道這件事，並不是全世界的 DNS servers 都會馬上知道這件事，因為 DNS server 會持續使用 cache 裡的資料，直到它過期才會重新詢問 authoritative name server

# Protocol

### Port

DNS server 使用 port 53（小知識：這也是 AWS Route 53 服務名稱的由來。）

### Transport Layer Protocol

DNS 最初 (1983) 是使用 [[UDP]] 作為 transport layer 的 protocol，後來發展成也可以使用 [TCP](</Network/TCP.draft.md>)，使用 UDP 的好處是「低成本」、「快速」，但缺點就是「不安全」、「不穩定」。

### Message Format

DNS request 與 DNS response 的 format 長得一樣。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/dns-message-format.png>)

- Flags 區段記錄了包括：
    - QR：這是一個 query 還是 response
    - AA：DNS server 是否為 aurhoritative name server
    - RD：Client 是否希望這個請求使用 recursion approach
    - RA：DNS serever 是否可以使用 recursion approach
    - ...（其它此處略）

# Practice: DNS Lookup Using Code

- Python

    ```Python
    import socket
    
    socket.gethostbyname("google.com")
    ```

- Linux Command

    ```bash
    dig +short google.com
    ```

# DNS Lookup Tool (Website)

<https://www.whatsmydns.net/>

# 參考資料

- <https://www.ibm.com/topics/dns-protocol>
- <https://en.wikipedia.org/wiki/Domain_Name_System>
- <https://www.cloudflare.com/learning/dns/glossary/dns-root-server/>
- <https://medium.com/networks-security/cdb73e290299>
