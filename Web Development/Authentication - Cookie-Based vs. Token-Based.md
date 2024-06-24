#Authentication #WebDevBackend #WebDevFrontend #Cookie

# Cookie-Based Authentication

Cookie-based authentication 最原始的意思是「將使用者的資訊（狀態）全部塞進 `Cookie` header」，但由於以下兩個原因：

1. Cookie 有大小上限（4 KB）
2. Request 若被攔截，放在 `Cookie` header 裡的使用者資訊就洩露了

因此後來慢慢演變為只攜帶 **Session ID** 在 `Cookie` header 中，server 再根據 session ID 找到對應的使用者，必要時再查詢該使用者的資訊並回傳。

由於整個 Authentication 的過程分別在 client-side 與 server-side 用到了 cookie 與 session 兩個技術，因此又叫做 ==**Cookie/Session Authentication**==，這也是本段主要想探討的。

Cookie/session authentication 的流程如下圖：

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Login (with login credentials)
    Server->>Server: Create a session (stored in memory) <br/> along with a session id.
    Server->>Client: Add the Set-Cookie header to the response
    Note left of Server: Set-Cookie: session_id=a1234
    Client->>Client: Store the session_id <br/> in the Cookie storage.
    Client->>+Server: Send requests with Session ID <br/> in the Cookie header.
    Note right of Client: Cookie: session_id=a1234
    Server->>Server: Recognize the cookie
    Server->>-Client: Respond data exclusive to a1234
```

- Server-side session 的功能是紀錄那些原本想塞進 cookie 的使用者基本資訊
- Session 通常會具有時效性
- Session 通常是 key-value pair
- 因為存取頻繁且為了存取快速，session 通常會存在 memory cache 裡（比如存 Redis）
- 「Server 使用 session 來紀錄使用者的登入狀態」違反 [REST API 的 stateless 原則](</Web Development/REST API.md#Statelessness>)

### 優點

搭配上 [HttpOnly](</Web Development/Cookies/Cookies 的存取.md#HttpOnly>) 以及 [Secure](</Web Development/Cookies/Cookies 的存取.md#Secure>) 的 session id/auth cookie，可以防止受到 [XSS attack](</Network/CSRF Attack & XSS Attack.md#XSS Attack>)，且即使被駭客竊聽，cookie 的 plaintext 也不會被竊聽者取得。

### 缺點

- 只有在「server 與 client 的網域相同」時才能運作，因為如果 server 與 client 的網域不同，那麼 client 就不會自動攜帶 cookie 了。
- 因為 cookies 會自動被 request 帶上，所以 cookie-based authentication 容易受到 [CSRF Attack](</Network/CSRF Attack & XSS Attack.md#CSRF Attack>)，但其實還是有以下兩種方式可以預防：
    - 將 session ID 這個 cookie 的 [SameSite](</Web Development/Cookies/Cookies 的存取.md#SameSite>) attribute 設為 `Lax`，搭配上 server-side 使用「GET method **以外**的 API」
    - 將 session ID 這個 cookie 的 `SameSite` attribute 設為 `Strict`
    - CSRF token
- 如果有些每次溝通都必須夾帶的基本資料，但又不想直接存在 cookie，就等於每次都要進 Session 所使用的資料庫查詢該基本資料，這顯得有點蠢。

### 其實也不一定要用 Cookie

從 [瀏覽器中的儲存空間](</Network/瀏覽器中的儲存空間.md>) 一文我們已經知道，client side 儲存資料的地方至少有三種，因此其實廣義來說，session ID 可以存在這三個地方中的任意處，只要在送出 request 時記得帶上，那就算是 cookie/session authentication 了。

唯一要注意的就是，若不把 session ID 存在 cookie（儲存空間），就無法利用「request 會自動帶上 cookie」這個特質，必須另外寫一段 JavaScript 來將 session ID 塞進 request 的任一部份，至於是哪一部份，則須由前後端自行約定，比如：

- HTTP request 的 `Authorization` header
- POST method 的 request body
- GET method 的 query string

### 不使用 Cookie 會有什麼優點？

事實上儲存空間有了 cookie 以外的選擇後，等同於解決了[#缺點](</./Web Development/Cookie-Based Authentication vs. Token-Based Authentication.md#缺點>)中的前兩點：

1. 若前後端所在的網域不同，還是可以主動用 JavaScript 將 session ID 塞進 request
2. 若採用 JavaScript 主動將 session ID 塞進 request 的方式，就意味著不像 cookies 一樣會被自動攜帶，也就不會有 [CSRF Attack](</Network/CSRF Attack & XSS Attack.md#CSRF Attack>) 的問題

### 不使用 Cookie 會有什麼缺點？

**Vulnerable to XSS Attack**

由於須採用 JavaScript 主動將 session ID 塞進 request，就意味著 JavaScript 可以存取到存在瀏覽器中的 session ID，也就意味著 [XSS Attack](</Network/CSRF Attack & XSS Attack.md#XSS Attack>) 是有效的。

# Token-Based Authentication

在條列 cookie-based authentication 的缺點時，我們最後一點提到：

>如果有些每次溝通都必須夾帶的基本資料，但又不想直接存在 cookie，就等於每次都要進 session 所使用的資料庫查詢該基本資料，這顯得有點蠢

其實 token-based authentication 可以說正是針對這個痛點而生，這裡的 token 通常須具備下列幾個特點：

- 夾帶部分使用者資訊
- 須經過加密
- 具唯一性
- 具時效性

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Login (with login credentials)
    Server->>Server: Generate a token with the private key.
    Server->>Client: Send a response along with the token.
    Note left of Server: {"token": a1234}
    Client->>Client: Store the token in the browser.
    Client->>+Server: Send requests along with the token.
    Note right of Client: Authorization: Bearer a1234
    Server->>Server: Decrypt the token with the private key.
    Server->>-Client: Respond data exclusive to a1234
```

與 cookie-based authentication 相同的是，token 也可以存在[瀏覽器的任一種儲存空間](</Network/瀏覽器中的儲存空間.md>)，當 client 對 server 送出 request 時，再使用 JavaScript 將 token 塞進 request 的[任一部份](</./Web Development/Cookie-Based Authentication vs. Token-Based Authentication.md#其實也不一定要用 Cookie>)即可。

最常見的 token-based authentication 為 [JWT](</Web Development/JWT.md>)。

### 優點

- 針對那些每次溝通都必須夾帶的基本資料，可以直接夾帶在 token 裡，如此一來就不用每次都進 session 所用的資料庫查。
- 只要不是放在 cookie 裡，就沒有受到 [CSRF attack](</Network/CSRF Attack & XSS Attack.md#CSRF Attack>) 的風險，事實上通常採用 token-based authentication 時都不會選擇存在  cookie 然後讓 request 自動帶上，所以有時候你會看到 ==**Cookieless Authentication**== 這個名詞。

### 缺點

- 與 cookie-based authentication 中[#不使用 Cookie 的缺點](</./Web Development/Cookie-Based Authentication vs. Token-Based Authentication.md#不使用 Cookie 的缺點>)相同，因為可以用 JavaScript 存取瀏覽器裡的 token，所以有受到 XSS attack 的風險。
- 隨著 token 裡夾帶著資訊越多，token 的大小就越大，進而拉長傳輸時間。

>[!Note]
>雖說 token 有經過加密，但還是不要放入機敏資訊（比如密碼，沒事把密碼放在 token 裡幹嘛？）。

# Token/Session ID 存哪比較好？

假如你已經讀過[瀏覽器中的儲存空間](</Network/瀏覽器中的儲存空間.md>)這篇文章，你應該對各種儲存位置的特性已經相當了解，下表是將 token 存在不同位置的特色或優缺點：

| |Session Storage|Local Storage|Cookies|
|---|---|---|---|
|清除機制|在 browser 關閉後便會被清空／登出|須手動清除／登出|若有設置 `max-age` 或 `expire` 則會在時間到時自動清除／登出，否則須手動清除／登出（詳見[本文](</Web Development/Cookies/Cookies 的存取.md#expires>)）|
|同一個 Domain 的分頁間是否共享 token？|❌|✅|✅|

# 參考資料

- <https://stackoverflow.com/questions/17000835/token-authentication-vs-cookies>
- <https://stackoverflow.com/questions/26340275/where-to-save-a-jwt-in-a-browser-based-application-and-how-to-use-it>
- <https://blog.loginradius.com/engineering/cookie-based-vs-cookieless-authentication/>
