# Socket

- Socket 有時候也被叫做 **endpoint**。
- Socket 直翻是插座，但在 network 中只是抽象的、用來接收與傳遞資料的出入口。
- ==Socket 由 OS 提供，是一種 [file descriptor](</Operating System/File System.md#File Descriptors (FD)>)==。
- 主動發起連線的一方會被稱為 client，被連線的一方則稱為 server，雙方透過彼此的 socket address 找到彼此。
- 依傳送資料的方式，可以將 socket 分為 stream socket 與 datagram socket 兩種。
- 依對內或對外，可以將 socket 分為 **Unix domain socket** 與 **Internet domain socket** 兩種。
- Berkeley socket standard 定義了如何實做一個提供 socket 服務的 API。

### Stream Socket vs. Datagram Socket

- **Stream Socket**: 用來傳送連續性的資料流
- **Datagram Socket**: 用來傳送離散的 data chunk

### Unix Domain Socket vs. Internet Domain Socket

##### Unix Domain Socket

給同一個 host 內進行 [[Process.draft#Unix Signal (IPC)|IPC]] (inter-process communication) 用的，比如 Docker containers 之間就是透過 unix domain socket 溝通的。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/unix-domain-socket.png>)

Unix domain socket 的優點：無論 stream 或者 datagram 都是 ==always reliable==。

##### Internet Domain Socket

又叫 network socket，是給不同 hosts 間傳遞資料用的。

在 [OSI model](</Network/OSI Model.draft.md>) 中，socket 是介於 application layer 與 transport layer 間的介面，如下圖：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/socket-in-the-osi-model.png>)

如果 transport layer 使用的是 [TCP](</Network/TCP.draft.md>)，則該 socket 屬於 stream socket；如果 transport layer 使用的是 UDP，則該 socket 屬於 datagram socket，詳見下表：

| |TCP Socket|UDP Socket|
|:-:|:-:|:-:|
|**Socket Type**|Stream|Datagram|
|**Reliable**|✅|❌|

### Socket Address

Client 透過 socket address 指定要與哪個 socket 建立連線，Unix domain socket 與 Internet domain socket 的 address 格式不太一樣：

- Unix Domain Socket: `/path/filename`
- Internet Domain Socket: `ip.address:port`

### Berkeley Socket Standard

Berkeley socket standard 定義了如何實做一個提供 socket 服務的 API。

##### 常見的 Socket API Functions

|Function|Description|Side|
|---|---|--:|
|`socket()`|建立一個 socket|server/client|
|`bind()`|給 socket 一個 socket address|server|
|`listen()`|TCP socket 才需要的 function，等待 client 建立連線|server|
|`connect()`|TCP socket 才需要的 function，與 server 建立連線|client|
|`accept()`|TCP socket 才需要的 function，同意 client 的 `connect()` 請求|server|
|`send()`/`sendto()`/`write()`|送出資料|server/client|
|`recv()`/`recvfrom()`/`read()`|接收資料|server/client|
|`close()`|結束連線，OS 會釋放原本分配給 socket 的資源|server/client|

# Port

Port 在 network 中也是抽象的，一個 host 身上會有 **65,536** 個 ports，它們會從 0 開始被編號，每個 port 用來提供一種服務。

前面提到 Internet domain socket 是由 IP address + port 組成，因此對一個 host 來說，他有幾個 ports 就會有幾個 sockets。

有一些 ports 已經被 OS 拿來提供固定的服務，這些提供固定服務的 port number 都會小於 1,024，下列為一些常見的服務以及其對應的 port number：

- 0: wildcard port，當看到 port 0 時，OS 會自動導向合適的 port
- 20: FTP file transfer
- 21: FTP command control
- 22: SSH
- 25: SMTP e-mail routing
- 53: DNS service
- 67: DHCP server
- 68: DHCP client
- 80: HTTP
- 443: HTTPS

>[!Note]
>使用者如果要使用 port 來提供其它服務，只能使用還沒被佔領的，。

在 Linux 與 MacOS 中，可以查看 /etc/services 這個檔案來看所有 ports。（不是即時狀態，只是一份文件）

# 參考資料

- <https://en.wikipedia.org/wiki/Network_socket>
- <https://en.wikipedia.org/wiki/Berkeley_sockets>
- <https://en.wikipedia.org/wiki/Unix_domain_socket>
- <https://en.wikipedia.org/wiki/Port_(computer_networking)>
