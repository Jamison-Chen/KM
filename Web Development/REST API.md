#WebDevBackend #WebDevFrontend 

REST 是 **RE**presentational **S**tate **T**ransfer 的縮寫，是在西元 2000 年由 Roy Fielding 在他的博士論文中提出。REST API 有時候也被叫做 RESTful API，是一種 API endpoint 的風格，它主張善用 HTTP 的 `GET`、`PUT`、`POST` 與 `DELETE` methods 來對資料做 **CRUD**（新增、讀取、更新、刪除）。

# REST Architecture 的要素

### Uniform Interface

- **Resource Identification in Requests**

    Client 可以透過不同 URI 來指定它所需要的資源。

- **Resource Manipulation Through Representations**

    當 client 可以透過某個 URI 取得某筆資料的 "representation" 時，他就應該要有足夠的資訊知道要如何修改與刪除那筆資料。

    "Representation" 在這裡的意思就是任何一種「表示資料的方式」，比如 JOSN、HTML 都算是一種 representation。

- **Self-Descriptive Messages**

    Request 與 response 必須說明自己提供的訊息要如何解析。比如 response header 中的 `Content-Type` 就說明了 response body 中的訊息的格式。

- **Hypermedia as the Engine of Application State** ([HATEOAS](https://en.wikipedia.org/wiki/HATEOAS))

    Client 從一個服務的 "initial" URI（比如網站的首頁）拿到的 response，應該要讓 client 知道這個服務所有可用的 URI。

### Client-Server Architecture

Client 與 server 必須分離／獨立，詳見 [Client-Server Model](</System Design/Client-Server Model.canvas>)。

### Statelessness

所有關於 client 的資訊／狀態都由 client 自己提供，在 client 不提供資訊的情況下，server 不會知道這個 client 是誰或者剛剛做了什麼。

這裡是要求 API server 要有 statelessness，所以「API server 到 DB 查詢 client 的完整資料」並沒有違反這個原則。

### Cacheability of Resources

Server 須告訴 client 每個資源是 cacheable 或 non-cacheable，client（或中間的 proxy）再根據這個資訊決定是否將該資源 cache。

### Layered System

Server 收到 client 的 request 後，可能不是單一台 server 完成所有工作，而是多種服務協作而成，而 client 不會也不應該知道 server side 的架構長什麼樣子。

### Code on Demand *(Optional)*

Server 除了回覆純文字資料以外，也可以回覆一些 client-side 可以直接執行的 JavaScript 程式碼，client 就不用自己實作該功能／該部分的程式邏輯。

# E-R Diagram of REST API

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/er-diagram-of-rest-api.png>)

# REST API 範例

以 user 的 CRUD 為例：

```plaintext
# 查詢指定 user 的資料
GET /users/{USER_ID}

# 列出多個 users
GET /users?page={PAGE}&limit={LIMIT}

# 新增 user
POST /users

# 更新指定 user 的資料
PUT /users/{USER_ID}

# 刪除指定 user
DELETE /users/{USER_ID}
```

# REST API 的缺點

在 REST API 中，client 只能透過 server 定義好的 endpoints，搭配指定的 HTTP method，來索取結構固定的資料，這樣會有兩個問題：

### Under Fetching

有可能既有 API 回傳的資料欄位無法滿足 client side 的需求，此時 client 必須透過呼叫多個 API 才能拼湊成完整的資料，有些時候甚至沒辦法用既有 APIs 湊出 client side 要的資料，這時候就須要 server side 另開 API 或調整既有的 API。

### Over Fetching

有可能 API 回傳的資料欄位過多，此時對傳輸速度與 server 計算量都會造成不必要的負面影響。一言以蔽之，REST API 欠缺靈活性。

# 參考資料

- <https://en.wikipedia.org/wiki/REST>
