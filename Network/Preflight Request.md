Preflight request 的中文叫做預檢請求。

# Simple Request

當一個 request 符合下列所有條件時，我們稱這樣的 request 為一個 "simple request"：

- HTTP method 為以下三者任一：
    1. `GET`
    2. `HEAD`
    3. `POST`
- 只包含以下四個 headers：
    1. `Accept`
    2. `Accept-Language`
    3. `Content-Language`
    4. `content-type`
- `content-type` 的值為以下三者任一：
    1. `application/x-www-form-urlencoded`
    2. `multipart/form-data`
    3. `text/plain`

"Simple request" 可以直接被 JavaScript 送出；相反地，其它 requests 要被送出前，browser 都會先送出一個 preflight request，其目的為向 server 詢問他接受什麼樣規格的 requests，拿到規格後回來檢查準備送出的正式 request 是否有合規，若沒有則不會將該 request 送出，並且跳出 [[CORS & SOP|CORS]] error。

# 如何辨識 Preflight Request

Preflight request 有兩個主要特色：

1. HTTP method 為 `OPTIONS`
2. 必會出現 `Access-Control-Request-Method` 或 `Access-Control-Request-Headers` header

可以透過這兩個特色來判斷一個 request 是否為 preflight request。

# Caching Mechanism

Preflight request 所要來的「規格書」會被 browser cache 住，在 cache 還存在的情況下，下次準備對同一個 endpoint 送出的 preflight request 就不會被送出，browser 此時會直接拿 cache 中的資料來看。

Server side 可以透過 `Access-Control-Max-Age` header 來控制 client cache 的時長。

如果想要讓每次的 preflight request 都被送出，則可以在 client side 將開發人員工具中 "Disable cache" 這個選項打勾。

# 在 Chrome 中查看 Preflight Requests

打開開發人員工具的 Network tab 後，篩選 Other 可以看到 preflight requests；篩選 Fetch/XHR 則會看到正式的 requests：

![[how-to-see-preflight-request.png]]
