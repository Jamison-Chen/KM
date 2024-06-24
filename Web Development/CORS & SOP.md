#HTTP #WebDevBackend #WebDevFrontend

CORS 為 Cross-Origin Resource Sharing 的縮寫，是一種建立在 HTTP response header 上的機制。

Response 中與 CORS 相關的 header keys 包含：

- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Expose-Headers`
- `Access-Control-Allow-Credentials`

這些 headers 的主要用途是 server 要讓 client 知道「request 應符合什麼規格」，有些時候 browser 會透過 [Preflight Request](</Network/Preflight Request.md>) 來取得這些資訊，然後核對「真正要送出的 request」是否符合這些規格，符合才會送出真正的 request。

針對不需要 preflight request 的 request，browser 雖無法預先核對規格，但還是會去檢查 response 裡是否有 `Access-Control-Allow-Origin`  header，這個 header 的值須等於 request 的 `Origin` header，==若發現兩者的 scheme (protocol)、IP address/domain、port 任一項不相等，則即使收到 response 也不可以打開來看裡面的內容==。

# Same-Origin Policy (SOP)

Browser 之所以會那麼雞婆，就是為了要遵循 same-origin policy。

須注意的是，在不需要 preflight request 的情境中（詳見[這裡](</Network/Preflight Request.md#Simple Request>)），==SOP 並沒辦法阻止 request 對 server 的 data state 進行存取與改動==，因為 request 實際上是成功的，只是 browser 不給你看 response 而已。

==SOP 也不能用來阻擋 [CSRF Attack](</Network/CSRF Attack & XSS Attack.md#CSRF Attack>)==，因為只要攻擊者意圖送出的是 [Simple Request](</Network/Preflight Request.md#Simple Request>)，那就還是可以送出真正的 request，[Cookies](</Web Development/Cookies/Cookies 的存取.md>) 也就還是會被夾帶其中。

# CORS 流程圖

```mermaid
flowchart TD
    id1([JavaScript attepts to make a cross-origin request])
    id1-->id2
    id2{Is it a GET or HEAD?}
    id3{Is it a POST?}
    id4{Are there custom\nHTTP headers?}
    id5{Is the content-type standard?}
    id6(Make preflight/OPTIONS request to server)
    id7(Make actual request)
    id8{Are Access-Control-* in\nresponse appropriate?}
    id9([CORS error])
    id10{Did server allow the origin?}
    id11(Server responds)
    id12([OK])
    id2-- Yes -->id4
    id2-- No -->id3
    id3-- Yes -->id5
    id5-- Yes -->id4
    id4-- No -->id7
    id6-->id8
    id3-- No -->id6
    id5-- No -->id6
    id4-- Yes -->id6
    id8-- Yes -->id7
    id8-- No -->id9
    id7-->id11
    id11-->id10
    id10-- No -->id9
    id10-- Yes -->id12
```

# CORS Errors

- Method 不被 Server 接受時

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cors-error-access-control-allow-methods.png>)

    解決方法：調整 `Access-Control-Allow-Methods` header。

- Origin 不被 Server 接受時

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cors-error-access-control-allow-origin.png>)

    解決方法：調整 `Access-Control-Allow-Origin` header，看是要設為 `*` 或設為 request 的 `Origin`。

- Request 中包含不被 Server 接受的 Header 時

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cors-error-access-control-allow-headers.png>)

    解決方法：調整 `Access-Control-Allow-Headers` header。

- Response 中包含自定義的 Header 時

    這種情況下不會有 CORS Error，只會發現使用 JavaScript 讀取該 header 時，總是讀到 `null`。

    解決方法：調整 `Access-Control-Expose-Headers` header。

- Request 的 `credentials: include`，同時 Response 的 `Access-Control-Allow-Origin: *` 時

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cors-error-access-control-allow-origin-wildcard.png>)

    解決方法：將 `Access-Control-Allow-Origin` header 設為與 Request 的 `Origin` header 相同的值。

    >[!Note]
    >這個規則的用意是，因為 `Access-Control-Allow-Origin: *` 代表所有 origin 的 clients 都可以呼叫 API 並打開 response，是一個相對不安全的設定；而 `credential: include` 代表 client 送出該 request 時會攜帶 cookies、收到 response 時也會接受並設置 cookies（若 response 上有 `Set-cookie` header），是一個會洩漏 client 隱私的設定，兩個不安全的設定不能同時存在！

- Request 的 `credentials: include`，但 Response 的 `Access-Control-Allow-Credentials: false` 時

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cors-error-access-control-allow-credentials.png>)

    解決方法：調整 `Access-Control-Allow-Credentials` header。

# 使用 Proxy Server 解決 CORS Error

如果後端是自己開發的，那是否要進行上述 response header 的調整是由自己掌控的，但若現在是想向 google.com 或 wikipedia.org 這樣的第三方網站要求資料，那 response header 就不是我們能控制的了。此時我們必須另外架一個自己的 backend service，透過這個 service 向第三方網站要資料，再將要來的資料轉交給自己的前端，而這個另外架的 backend service 就是所謂的 [proxy](</System Design/Forward Proxy & Reverse Proxy.md>)。因為 proxy 是自己架的，所以 response header 又掌握在自己手中了～

```mermaid
sequenceDiagram
    participant Client
    participant Proxy Server
    participant Third Party Server
    Note over Client: myfrontend.com
    Note over Proxy Server: mybackend.com
    Note over Third Party Server: www.google.com
    Client->>Proxy Server: Send a request to <br/> mybackend.com
    Note right of Client: {"uri": <br/> "https://www.google.com", <br/>"method": "get", ...}
    Proxy Server->>Third Party Server: Send a request to <br/> www.google.com
    Third Party Server->>Proxy Server: Response
    Proxy Server->>Proxy Server: Configure headers
    Note left of Proxy Server: Access-Control-Allow-Origin: * <br/> ...
    Proxy Server->>Client: Response
```

# 參考資料

- <https://github.com/aszx87410/blog/issues/68>
- <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>
