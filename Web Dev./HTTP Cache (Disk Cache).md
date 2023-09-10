#Caching

之所以被叫做 disk cache 是因為這類的 cache 是存在 disk；之所以又叫做 HTTP cache，是因為這類的 cache 是 server 透過某些 HTTP response headers 來控制 client 發送 HTTP request 的行為。

這些 headers 包括：

- `Expires`
- `Cache-Control`
- `Last-Modified`
- `ETag`

# `Expires`

==不推薦使用==

可以簡單理解成 data 的「有效日期」。Server 透過 `Expires: <day-of-week>, <day> <month> <year> <hour>:<minute>:<second> GMT`，使得 client 對某 endpoint 發起 request 並取得 response 後，會存一份在 client 自己的 disk，直到指定時間之前，若再次對同一個 endpoint 發起 request，都會直接使用 disk cache，不會送出 request。

為什麼不推薦使用？主要原因是 client 判斷是否送出 request 的準則是比對 `Expires` 的時間與「client 自己的主機時間」，因此 client 可以透過「將主機時間調至未來」來使得所有資料都被判定為已過期。

# `Cache-Control`

可以簡單理解成 data 的「有效期限」。Server 透過 `Cache-Control: max-age=<n>`，使得 client 對某 endpoint 發起 request 並取得 response 後，會存一份在 client 自己的 disk，接下來的 n 秒內若對同一個 endpoint 再次發起 request，則直接使用 disk cache，不送出 request。

# `Last-Modified`

==不推薦使用==

Server 透過 `Last-Modified: <day-of-week>, <day> <month> <year> <hour>:<minute>:<second> GMT` 可以讓 client 知道從這個 endpoint 要來的資料上次被更改的時間點。

不推薦使用的原因主要有二：

- 要自己實作

    Client side 須在 request 中攜帶 `If-Modified-Since` 或 `If-Unmodified-Since` header，server side 則須讓資料有一個「可以表示 `Last-Modified` 的欄位」。

- 只能省下「下載」時間，無法省下「溝通」時間，server load 下降幅度也有限

    Request 還是會被送往 server，當 server 收到 request 後也還是會進 database，只是這次進 database 是先查看指定資料的「可以表示 `Last-Modified` 的欄位值」是否早於 `If-Modified-Since`，若是，就直接回覆 `304 Not Modified`，不回傳資料，client 收到 `304` 後會到自己的 disk cache 拿資料。

# `ETag`

Server 透過 `ETag: <token>` 讓 client 下次對同一個 endpoint 發起 request 時也攜帶 `<token>` 在 `If-None-Match` header 上，當 server 看到 request 中有 `If-None-Match` 時，會檢查它的值與 server-side 的這個 endpoint 目前的 `ETag` 是否相同，若相同則直接回覆 `304 Not Modified`，不回傳資料。

- 優缺點

    與 `Last-Modified` 的邏輯類似，但少一個缺點，client 會自動帶上 `If-None-Match` header，無需另外寫程式攜帶。

    `ETag` 也有「只能省下下載時間，無法省下溝通時間，server load 的下降幅度也有限」的缺點。

- `ETag` 的值

    事實上並沒有人規定應該如何產生 ETag value (token)，只要該 token 在一定時間內具有唯一性可以代表某個 requested resource 即可。常見的產生 ETag value 的方法包括：

    - 將準備回傳的資料 hash
    - 將資料的「可以表示 `Last-Modified` 的欄位值」hash
    - 一個每次修改就會遞增的數字

`ETag` 也可以用來解決 Mid-air Collision，情境如下：

>有 A, B 兩個人同時在修改同一篇維基百科的文章，A 率先修改好並送出 Update 的 request 並且成功，一段時間後 B 也修改好並送出 Update request，但此時 server「不應」該讓 B 成功修改文章，因為 B 的文章並沒有包含 A 所做的修改，如果讓 B 成功修改，那 A 就等於做了白工。

如果 client 在送出 request 時將 ETag value 加在 `If-Modified` header 上，且 server 在處理 POST requests 前都會先檢查 `If-Modified` 是否等於目前的 `ETag`，不等於就不處理並回傳 `412 Precondition Failed`，如此一來就可以在 application level 預防 **mid-air collision**。

# 只有部分 HTTP Methods 會被導向 Disk Cache

理論上而言，client 要送出各種 HTTP method 的 request 前，皆可以到 disk cache 去看看有沒有還沒過期的資料可用，然而==大多數 browser 預設都只會讓 HEAD 與 GET 有機會使用 disk cache==。

原因是其他 methods 通常都是用來做「新增」、「修改」、「刪除」等功能，使用者理應會期待這些操作的 requests 「送出了就要等真的執行成功，才會收到成功的 response」，如果 browser 沒有實際送出 request 而是直接拿之前的結果給使用者，使用者將會被誤導。再者，==browser 在決定是否使用 disk cache 時並不會檢查 request 的 payload 或者 body==，也就是說如果 browser 連 POST 這類的 request 都會試著去拿 disk cache 來用，那麼只要是同一個 endpoint，無論使用者 payload 放什麼值，都會符合 browser 使用 disk cache 的標準。

這個特性雖然合理，然而它卻使得 [[GraphQL]] 無法直接受惠於 disk cache，因為 GraphQL 的 requests 預設是使用 POST method。（關於 GraphQL 如何才能觸發 caching mechanism，詳見 [[Caching for GraphQL]]）

# 組合技：`Cache-Control` + `ETag`

用 `Cache-Control: max-age=<n>` 可以控制 client 是否送出 request，但有時候雖然有效期限過了但資料其實沒有被更改，此時 server 可以比對 request 的 `If-None-Match` Header 與自己計算出來的 `ETag`，若相同就回覆 `304 Not Modified` 來通知 client：「可以繼續沿用 cache data，並請更新有效期限」。

# 參考資料

- <https://blog.huli.tw/2017/08/27/http-cache/>
- <https://stellate.co/blog/deep-dive-into-caching-rest-apis>
- <https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/Cache-Control>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Last-Modified>
- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag>
