#CyberSecurity 

# CSRF Attack

CSRF 是 Cross-Site Request Forgery 的縮寫，又稱為 one-click attack 或 session riding。

### 攻擊方式

若 A 網站的[身份驗證機制](</Web Development/Authentication - Cookie-Based vs. Token-Based.md>)是將 token 存在 cookie storage，那麼攻擊者可以在 B 網站（攻擊者的網站）或者寄給使用者的 email 中的設置一些惡意的按鈕，當使用者點擊按鈕時，JavaScript 就會向 A 網站發送一些並非使用者本意的 requests（比如一個把你銀行的錢轉給他的 request），若使用者不久前剛好登入過 A 網站且未登出，此時 A 網站的 cookies 就會自動夾帶在 requests 的 `Cookie` header 中（其中就包含確認登入狀態用的 token/sessionID），因此 A 網站會認為使用者還未登出，於是就不疑有它地執行該 request。

### 防範方法

- Server 設定 authentication token 時使用 `SameSite=Strict` 的 cookies（詳見[這篇](</Web Development/Cookies/Cookies 的存取.md#SameSite>)），基本上這個方法就可以防治大多數的 CSRF attack 了。
- 檢查 `Referer` header

    Server 檢查 request 的 `Referer` header，若不在白名單內則視同攻擊，不予理會。這個做法只適用於非公開的 API，因為公開的 API 無法預測會有誰來合法地呼叫，自然不會將那些來呼叫 API 的 clients 的 domain (referer) 都列在白名單內。

    >[!Note] 冷知識
    >其實英文字典中並沒有 `Referer` 這個單字，當初定義此 header 的人其實是要把它叫做 referrer，但他拼錯了🙂

- 使用 **CSRF Token**

    由 server 產生一串具有時效性的亂碼（假設是`xxxx`）交給 client，同時約定一個 custom header（比如叫 `X-CSRF-Token`），當 client 送出 GET 以外的 HTTP method 時，必須在 request header 中放入：`X-CSRF-Token: xxxx`。

### CSRF Token 要怎麼交到 Client 手中？

##### 透過 Set-Cookie 設定

在一個 user session 開始時，server 可以透過 API response 裡的 `Set-Cookie` header 將 CSRF token 設定在 client 的 cookie storage 中。

- 請注意這個 cookie 必須是 `SameSite=Strict`，否則一樣無法防禦 CSRF attack。
- 這個 cookie 必須「不能是」`HttpOnly`，因為 client 會須要用 JavaScript 將 cookie storage 中的 CSRF token 讀取出來放進 request header（但這樣就會變成 XSS vulnerable，下一段會介紹 XSS attack）。

##### Embed in the Initial Page

若網站使用是前後端分離的，那可以在使用者拿取前端資源時（通常只有上站的第一個 request）將 CSRF token 放在 HTML `<meta>` tag 中，client 接收到後再使用 JavaScript 將 token 存在 browser 中（但這樣就會變成 XSS vulnerable，下一段會介紹 XSS attack）。

>[!Info]
>更詳細的 CSRF 防範方式請參考[這篇文章](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)。

# XSS Attack

XSS 是 Cross-Site Scripting 的縮寫，之所以不縮寫為 CSS，是為了與 cascading style sheet 的縮寫區隔。

### 攻擊方式

- 在 client side 植入「可以讀取儲存在 browser 的使用者敏感資料並回傳給攻擊者」的惡意程式碼。
- 在 client side 植入「可以代替使用者進行某些操作」的惡意程式碼。

### 種類

- Stored (Persistent) XSS

    當網站中有讓使用者輸入的欄位（如回覆留言）時，攻擊者可以藉此進行 JavaScript injection，以達到攻擊的目的，這種攻擊成功後會==同時使很多用戶都受到影響，且若沒有人從後端刪除該留言，這個攻擊就會一直被觸發==。

    如：攻擊者可以在社群網站回覆留言時輸入 `<script>惡意程式碼</script>` ，若網站在沒有做任何 XSS 防禦的情況下就試圖顯示留言，則所有看到此則留言的使用者的 browser 都會執行這段惡意程式碼。

- Reflected XSS

    此種攻擊會以釣魚郵件或者其它類似的方式引誘使用者點擊某個會執行惡意 JavaScript 的連結。普通一點的攻擊者可能是直接傳一個自己架設的網站的連結；厲害一點的攻擊者會使用一個使用者本來就信任的網站（只是有安全漏洞他不知道），然後將 GET request 中的 query string 換成惡意程式碼，如果該網站在某種情況下會直接呈現這個 query string 的內容，那就會執行惡意程式。

    如：某社群網站的個人頁面網址為 `https://vulnerablewebsite/profile/<id>`，若攻擊者在 `<id>` 的位置輸入 `<script>惡意程式碼</script>`，而網站在找不到指定 id 的情況下會顯示「`<id>` 不存在」的頁面給使用者，在沒有做任何 XSS 防禦的情況下， `<script>` 內的惡意程式就會被執行。

- DOM-base XSS

    攻擊者透過 Stored XSS 或 reflected XSS 在使用者信任（但其實有安全漏洞）的網站中 render 出一個會往攻擊者自己的後端發 request 的表單，誘導使用者填入他的敏感資料。

### 防範方法

- 表單送出前先檢查內容
- 呈現任何 dynamic content 前，先檢查其型別，該轉為純文字的就先轉為純文字
- 在 request header 中敘明 `Content-Type` ([查看所有 Content-Type](https://www.iana.org/assignments/media-types/media-types.xhtml))
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

# 參考資料

- <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>
- <https://en.wikipedia.org/wiki/Cross-site_scripting>
- <https://en.wikipedia.org/wiki/Cross-site_request_forgery>
