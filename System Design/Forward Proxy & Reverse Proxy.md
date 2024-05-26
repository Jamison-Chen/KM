![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/forward -proxy-vs-reverse-proxy.jpg>)

# Forward Proxy

### Pros

- 隱藏 client 身份

    Server 無法得知 client 的真實 IP address，只知道 forward-proxy server 的 IP address。

- 可過濾、加工 requests 與 responses

- 減少等待時間

    Proxy server 可以 cache 剛訪問過網站的資料，當短時間內有其他 client 要訪問同樣的網站時，可以直接回覆 cache data。

# Reverse Proxy

### Pros

- 隱藏 server cluster 存在的事實

    Client 無法得知它現在是直接在跟 server 溝通還是在跟 reverse-proxy server 溝通。

- 提高訪問速度

    針對靜態內容以及短時間內有大量訪問請求的動態內容提供 cache。

- 為背後的 server cluster 取得 SSL 憑證、提供統一的 SSL 加解密

- 實現 **Load Balance**

    根據所有 server 的負載情況，reverse-proxy server 可以將 clients 的請求分發到不同的 server 上。

- 實現 [Canary Deployment](</System Design/Canary Deployment.md>)

# 參考資料

- <https://www.theserverside.com/feature/Forward-proxy-vs-reverse-proxy-Whats-the-difference>
- <https://www.jscape.com/blog/forward-proxy-vs-reverse-proxy>
- <https://www.jyt0532.com/2019/11/18/proxy-reverse-proxy/>
