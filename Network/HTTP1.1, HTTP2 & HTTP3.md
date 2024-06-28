#HTTP

HTTP 是 Hypertext Transfer Protocol 的縮寫，在 [OSI Model](</Network/OSI Model.md>) 被歸類為 application layer。1991 年 HTTP 誕生，當時的版本是 HTTP/1；1997 年，HTTP/1 改版到 HTTP/1.1，而 HTTP/1.1 一出現就主宰了將近 20 年，一直到 2015 年才出現他的下一代：HTTP/2；2022 年又出現 HTTP/3。

# HTTP/2 相對於 HTTP/1.1 的優點

### Weighted Prioritization

在 HTTP/2，開發者可以控制網頁載入時哪些資料要優先下載，進而提升使用者體驗。

### Multiplexing

在 HTTP1.1，當 server 有很多東西要回給 client 時，只能一個一個送，如果中間有某個送失敗了，還會導致後面的都送不出去；但在 HTTP/2，server 可以「同時」把多筆資料透過多個 data stream 送給 client。（Transport layer 仍然只有一個 TCP connection！）

### Server Push

在 HTTP/1.1 中，一段對話的開始一定是由 client 先送 request 給 server，server 再回覆；但在 HTTP/2 中，server 可以主動 push 資料給 client。

### HPACK

從 HTTP/1.1 開始，就會對 HTTP packet 的 header 進行壓縮，讓傳輸快一點，而 HTTP/2 採用了更先進的 HPACK 壓縮技術（每個封包大概可以再少幾個 bytes）。

# HTTP/2 的其它特色

### Binary Framing Layer

HTTP/1.1 的 header 與 body 都是以明文傳輸，但 HTTP/2 則會先把它們都轉成 binary 在傳輸。

# HTTP/3 相對於 HTTP/2 的優點

HTTP/3 與前兩代 HTTP 最大的差別就是 HTTP/3 的 transport layer 使用的不是 TCP 而是 [QUIC](https://en.wikipedia.org/wiki/QUIC)。QUIC 比 TCP 來的更安全，且傳輸速度比 TCP 快，除此之外，QUIC 還有以下優點：

- 當手機的網路從 WiFi 切換成行動網路時更平順
- 當封包丟失時，不會出現 head-of-line blocking problem（當一個封包丟失時，後面的封包就不能繼續傳的問題）
- [TLS](</Network/SSL & TLS.md>) 版本協商與 transport layer 的 handshake 可以同時進行，進而縮短連線時間

# 參考資料

- <https://www.cloudflare.com/learning/performance/http2-vs-http1.1/>
- <https://www.cloudflare.com/learning/performance/what-is-http3/>
