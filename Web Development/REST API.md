#WebDevBackend #WebDevFrontend 

REST 是 **RE**presentational **S**tate **T**ransfer 的縮寫。REST API 是架構在 HTTP 上的通訊風格，善用了 HTTP 的 GET、PUT、POST 與 DELETE methods 來對資料做 CRUD。

# Constraints of REST Architecture

### Uniform Interface

##### Resource Identification in Requests

Client 可以透過不同 URI 指定它所需要的不同資源。

##### Resource Manipulation Through Representations

當 client 透過 REST API 拿到一筆資料後，就必須有辦法透過他拿到的資料組成「修改或刪除該筆資料的 request」。

##### Self-Descriptive Messages

URL path、request 與 response 的欄位名稱要可以讓人知道它代表什麼意思。

##### Hypermedia as the Engine of Application State ([HATEOAS](https://en.wikipedia.org/wiki/HATEOAS))

當 client 呼叫某個 REST API 後，它拿到的 response 應該要讓他知道其它所有可以對這筆資料／這類資源做其它操作的 API endpoints

### Client-Server Architecture

Client 與 server 必須分離／獨立，詳見 [Client-Server Model](</System Design/Client-Server Model.canvas>)。

### Statelessness

Server 不會記錄或知道任兩個 requests 是否來自於同一個或不同個 clients，也不會知道這個 client 剛剛做了什麼，所以 client 的每個 requests 都須要有完整的資訊告訴 server 它是誰、要做什麼。

### Cacheability of Resources

Server 須告訴 client 每個資源是 cacheable 或 non-cacheable，client（或中間的 proxy）再根據這個資訊決定是否將該資源 cache。

### Layered System

Server side 收到 client side 的 request 後，可能不是單一台 server 完成所有工作，而是多種服務協作而成，服務跟服務間可以互相溝通，而 client 不會知道 server side 的架構長怎樣。

### Code on Demand (Optional)

Server 不只能回一般的純文字資料，也可以回覆一些 client-side 可以直接執行的程式碼或執行檔，client 就不用自己實作該功能／該部分的程式邏輯。

# REST API 的缺點

在 [REST API](</Web Development/REST API.md>) 中，client 只能透過 server 定義好的 endpoints，搭配指定的 HTTP method，來索取結構固定的資料，這樣會有兩個問題：

### Under Fetching

有可能既有 API 回傳的資料欄位無法滿足 client side 的需求，此時 client 必須透過呼叫多個 API 才能拼湊成完整的資料，有些時候甚至沒辦法用既有 APIs 湊出 client side 要的資料，這時候就須要 server side 另開 API 或調整既有的 API。

### Over Fetching

有可能 API 回傳的資料欄位過多，此時對傳輸速度與 server 計算量都會造成不必要的負面影響。

一言以蔽之，REST API 欠缺靈活性。

# 參考資料

- <https://en.wikipedia.org/wiki/REST>