### Simple Request

^7ff6aa

當一個 request 的 method 符合下列所有條件時，我們稱這樣的 request 為一個**簡單的 request**：

1. Method 為以下三者任一：
    1. `GET`
    2. `HEAD`
    3. `POST`
2. 只包含以下四個 headers：
    1. `Accept`
    2. `Accept-Language`
    3. `Content-Language`
    4. `content-type`
3. `content-type` 為以下三者任一：
    1. `application/x-www-form-urlencoded`
    2. `multipart/form-data`
    3. `text/plain`

簡單的 request 可以直接被 JavaScript 送出，相反地，其他 requests 要被送出前，都會先送出一個 preflight request，其目的為向 server 詢問他接受什麼樣規格的 requests，拿到規格後回來檢查準備送出的正式 request 是否有合規，若沒有則不會將該 request 送出，並且跳出 CORS error。

### 如何辨識 Preflight Request

Preflight Request 有兩個主要特色：

1. HTTP method 必為 `OPTIONS`
2. 必會出現 `Access-Control-Request-Method` 或 `Access-Control-Request-Headers` header

可以透過這兩個特色來判斷一個 request 是否為 Preflight Request

### 在 Chrome 中查看 Preflight Requests

打開開發人員工具的 Network tab 後，篩選 Other 可以看到 Preflight Request，篩選 Fetch/XHR 可以看到正式的 request：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Screen Shot 2023-01-08 at 4.26.00 PM.png>)

### Caching 機制

Preflight Request 所要來的「規格書」會被 browser cache 住，在 cache 還存在的情況下，下次準備對同一個 endpoint 送出的 Preflight Request 就不會被送出，browser 此時會直接拿 cache 中的資料來看，可以在 server side 透過 `Access-Control-Max-Age` 來控制 cache 時間的長短。如果想要讓每次的 Preflight Request 都被送出，則可以在 client side 將開發人員工具中 Disable cache 這個選項打勾。
