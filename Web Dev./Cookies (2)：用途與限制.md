#Cookie

由於 HTTP protocol 是 **stateless** 的，在 client 不主動提供資訊的情況下，server 無法得知任何發出 request 的 client 以前的狀態。

在 [[從 Web 1.0 到 Web 3.0#Web 1.0|Web 1.0]] 的時代，是否 stateless 並不重要，然而隨著 [[從 Web 1.0 到 Web 3.0#Web 2.0|Web 2.0]] 在 20 世紀末萌芽，**會員／帳號** 的概念逐漸普及，「針對每個帳號提供專屬的資料與服務」也變得理所當然。而 cookies **最初**的用途，就是「儲存登入者的資訊（狀態）」，然後將這些資訊放進 request 中的 `Cookie` header，以讓 server 知道發出 request 的 client 是哪個帳號。

比如在一個網路商城中，未註冊會員的人的購物車內容就可以存在 Cookies（已註冊會員的人，其購物車商品通常已經被記錄在後端的資料庫）。

若想了解如何設置與存取 Cookies，請參考 [[Cookies (1)：設置與存取|此文]]。

# Cookies 須斟酌使用

1. Cookies 其實不適合拿來儲存「機敏」資料，比如 user 的帳號密碼，因為 cookies 會被塞進 **每一個** requests 中，這樣太容易被有心人士竊聽。

2. Cookies 也不適合拿來儲存大量資料，一樣是因為 cookies 會被塞進 **每一個** requests 中，太大或太多的 cookies 會使得溝通的過程變慢，進而影響使用者體驗。

# Cookies 的三種用途

基於上述兩個使用限制，現今的 cookies 逐漸演變成以下三種用途：

1. Authentication
2. Personalization
3. Tracking

### Authentication

如果 server 可以在用戶登入成功後產生一個 Session 用來記錄「這個使用者已經登入成功」這件事，同時為這個 Session 產生「具有唯一性」的 ID，那麼將這個 Session ID 交給 client，往後就可以透過「來自 client 的 request 的 `Cookie` header 的 Session ID」知道 client 背後的會員是誰，有需要時，再從資料庫撈取屬於該會員的必要資料，不須把會員的所有資料交給 client。

通常，server 會為每個 Session 設定有效期限，若 client 提供的 Session ID 所對應到的 Session 已過期，則 client 會被要求重新登入。

關於使用 Session ID 實現身份驗證的更多資訊，詳見 [[Cookie-Based Authentication vs. Token-Based Authentication#Cookie-Based Authentication|Cookie/Session Authentication]]。

### Personalization

Personalization 即「針對每個帳號提供專屬的資料與服務」，甚至是還沒有註冊帳號的 client，server 也可以透過 client 提供的 Cookie 來得知他的偏好設定，比如 Google 就曾經用 cookie 來紀錄一個 client 希望每一頁搜尋頁面要出現幾筆結果。

不過，由於 cookies 是存在 browser 裡，所以「完全依靠 cookie 來記錄」的資料是沒有辦法跨 browser 或者跨裝置共享的。必須在資料庫也儲存一份資料，並且在 server-side 額外實作一些機制，比如說「若看到已登入的 client 沒有提供 Cookie，就到資料庫去查詢，然後設置新的 cookie 到這個新的 client 上」，才有辦法實現「跨裝置共享使用者偏好」這個目的。

### Tracking

關於 Tracking 的方式，可以直接以例子來了解：

當某個 client 第一次造訪 A 網站時，server 即設置一個 unique identifier 在 client 的 Cookies 中，因為 cookies 會被塞進每一個對 A 網站發起的 requests 中，A 網站的 server 在回傳資料的同時也會在一個 log file 裡紀錄 unique indentifier 以及被呼叫的 API endpoint，日後可以透過分析這個 log file 來了解 client 的使用習慣（點擊順序、瀏覽時長、瀏覽紀錄...等）。

現今，「追蹤使用者的瀏覽紀錄以進行精準的廣告投放」已經是一項有專門的廣告行銷公司在經營的專業工作，其中，廣告行銷公司可以透過「第三方 cookie」讓不同客戶的網站間可以共享這些追蹤的結果，關於第三方 cookie 的更多內容，請見 [[Cookies (3)：從第一方到第三方|此文]]。

# 參考資料

<https://en.wikipedia.org/wiki/HTTP_cookie>
