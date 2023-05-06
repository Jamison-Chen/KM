#Caching

# 目的

- 縮短使用者的等待時間，提升使用體驗
- 降低 server 負擔

# 種類

### 依照影響範圍

- **Public Caching Mechanism**

    由某個人觸發 caching mechanism，但那一份 cache data 會給很多人用。

- **Private Caching Mechanism**

    某人觸發 caching mechanism 後所產生的 cache data 就專屬於他。

### 依照實作位置

- **Client-side Caching Mechanism**

  - [[HTTP Cache (Disk Cache)]]
  - [[#^d63548|Memory Cache]]
  - [[Service Worker#^1a979e|Service-Worker Cache]]

- **Server-side Caching Mechanism**

  - CDN Cache
  - Application Cache
  - Database Cache

# 優先順序

>Memory Cache > Service-Worker Cache > HTTP Cache > Server-side Caching

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/caching mechanism.png>)

# 其它

- 若網路斷線，則即使有 HTTP Cache 也無法取得，但可以拿到 Service-Worker Cache。

### Client-Side Memory Cache

^d63548

Client-Side Memory cahce 顧名思義是把資源存在 browser 的 RAM 裡。

並不是所有 browser 都會實作這種 Caching Mechanism（Chrome 有實作），目前也沒有明確定義 browser 要怎麼決定哪些資源要放到 Memory Cache。

Memory Cache 的優點是存取速度比 Disk Cache 快（其實感覺不太出來），缺點是關閉瀏覽器後 cache 就會被清空。

# 參考資料

<https://oldmo860617.medium.com/%E6%A5%B5%E9%99%90%E5%8A%A0%E9%80%9F-web-%E9%96%8B%E7%99%BC%E8%80%85%E4%B8%8D%E8%83%BD%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84-cache-%E5%A4%A7%E8%A3%9C%E5%B8%96-3c7a9c4241de>
