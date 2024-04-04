#Caching #WebDevBackend #WebDevFrontend 

# 目的

- 縮短使用者的等待時間，提升使用體驗
- 降低 server 負擔

# 種類

### 依照影響範圍

- **Public Caching Mechanism**

    由某個人觸發 caching mechanism 後所產生的 cache data 會給很多人用。

- **Private Caching Mechanism**

    某人觸發 caching mechanism 後所產生的 cache data 就專屬於他。

### 依照實作位置

- **Client-Side Caching**

  - [[#Client-Side Memory Cache|Memory cache]]
  - [[HTTP Cache (Disk Cache)]]
  - [[Service Worker#Service-Worker Cache|Service-Worker Cache]]

- **Server-Side Caching**

  - [[CDN]]
  - Reverse-Proxy Cache
  - Application Cache
      - 常見的第三方服務如 Memcached、[[Database/Redis/Introduction|Redis]]
  - Database Cache

# 優先順序

`Memory Cache` > `Service-Worker Cache` > `HTTP (Disk) Cache` > `Server-Side Caching`

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/caching mechanism.png>)

# 其它

- 若網路斷線，則即使有 HTTP cache 也無法取得，但可以拿到 service-worker cache。

### Client-Side Memory Cache

幾乎所有 browser 都會實作這種 caching mechanism（但並非所有），目前沒有明確定義 browser 要怎麼決定哪些資源要放到 memory cache。

- Pros
    - 理論上存取速度比 HTTP (disk) cache 快很多
- Cons
    - 關閉瀏覽器後 cache 就會被清空

# 參考資料

- <https://oldmo860617.medium.com/3c7a9c4241de>
