#HTTP


HSTS 是 HTTP Strict-Transport-Security 的縮寫，其中 `Strict-Transport-Security` 是一個 HTTP response headers 的 key，server 透過提供這個 header，告訴 client 記得以後送 request 到這個網域時，如果發現 scheme (protocol) 是 http，要自動先把 http 轉成 https 再送。Client 則會自己維護一個 HSTS list，記錄當訪問哪些網域時要把 http 轉成 https。

>[!Note]
>在 Google Chrome 中，搜尋 `chrome://net-internals/#hsts` 就可以查詢／管理目前這個瀏覽器的 HSTS list。

# Response Header Syntax

```plaintext
Strict-Transport-Security: max-age=<EXPIRE_TIME>

// or

Strict-Transport-Security: max-age=<EXPIRE_TIME>; includeSubDomains

// or

Strict-Transport-Security: max-age=<EXPIRE_TIME>; includeSubDomains; preload
```

### `max-age`

給一個整數 n，告訴 client「未來 n 秒內」要記得將對這個網域發起的 http request 轉成 https request。

Client 每次收到 HSTS header 時，都會更新 `max-age`，所以 server 將 `max-age` 設為 0，就等同於關閉 HSTS。

### `includeSubDomains`

HSTS 預設是只會讓 client 記得要把「目前訪問的 domain」的 request 的 http 轉 https。但若 server 在 HSTS header 中設定 `includeSubDomains`，則 client 就會把「目前訪問的 domain，以及其所有 sub domains」的 request 的 http 都轉成 https。

### `preload`

詳見[官方文件](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#preload)

# HSTS 的限制

大多 client（現在大多數的瀏覽器）只會對「有曾經以 https 訪問過且沒有 certificate error」的網域所回覆的 `Strict-Transport-Security` header 有反應，否則這個 header 會被 browser 忽略。

# HSTS vs. Server-Side Redirect

使用 HSTS 會比單純在 server 上設定將 http redirect to https 還要來得更安全，因為若只採用 server-side redirect，那 client 並不會知道以後都要改用 https，所以當使用者下次又使用 http 訪問同一個網域時，client 還是會對 server 送出 http request，然後拿到 status code `30x`，這段溝通過程是以 plaintext 傳輸的！這時攻擊者可以趁虛而入，攔截這個 plaintext request（如果這個 request 中有使用者的機敏資料就糟了），並假裝自己是使用者要訪問的網站，將 redirect 至攻擊者的網站。

由於 HSTS 有 `max-age`，且 client 通常只會對曾經有以 https 成功訪問過的網域的 HSTS 有反應，所以 HSTS 與 server-side redirect 並用才會是最安全的。

# 參考資料

- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security>
