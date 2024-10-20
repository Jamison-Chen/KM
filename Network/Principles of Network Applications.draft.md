# Socket

- Socket 完整的名稱是 network socket，有時候也被叫做 **endpoint**。
- Socket 直翻是插座，但在 network 中只是抽象的、用來接收與傳遞資料的出入口。
- ==Socket 由 OS 提供==，在 Linux OS 中，每個 socket 都是一個檔案，這個檔案的存取權限決定了誰可以透過這個 socket 傳遞資料。

### Socket Address

$$
\textnormal{socket address} = \textnormal{IP address} + \textnormal{port}
$$

### Unix Domain Socket vs. Internet Domain Socket

##### Unix Domain Socket

給同一個 host 內進行 **IPC** (inter-process communication) 用的，比如 Docker containers 之間就是透過 unix domain socket 溝通的，可以再細分為 **stream** 與 **datagram** 兩種：

- Stream: 用來傳送連續性的資料流。
- Datagram: 用來傳送離散的 data chunk。

##### Internet Domain Socket

給不同 hosts 間傳遞資料用的。

### Berkeley Socket Standard

Berkeley socket standard 定義了如何實做一個提供 network socket 服務的 API。

# Port

Port 在 network 中也是抽象的，一個 host 身上會有 65,536 個 ports，它們會從 0 開始被編號，每個 port 用來提供一種服務。

前面提到 socket 是由 IP + port 組成，因此對一個 host 來說，他有幾個 ports 就會有幾個 sockets。

有一些 ports 已經被 OS 拿來提供固定的服務（這些提供固定服務的 port number 都會小於 1,024）使用者如果要使用 port 來提供其它服務，只能使用還沒被佔領的。

下列為一些常見的服務以及其對應的 port number：

- 20: FTP file transfer
- 21: FTP command control
- 22: SSH
- 25: SMTP e-mail routing
- 53: DNS service
- 80: HTTP
- 443: HTTPS

# 參考資料

- <https://en.wikipedia.org/wiki/Network_socket>
- <https://en.wikipedia.org/wiki/Berkeley_sockets>
- <https://en.wikipedia.org/wiki/Unix_domain_socket>
