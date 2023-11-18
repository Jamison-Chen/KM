>[!Info] 溫馨提醒
>閱讀本文之前，你必須先瞭解什麼是 [[Client-Server Architecture]]。

---

我們都知道在網頁中主要的三種語言分別是 HTML, CSS 與 JavaScript，我們常常會說，HTML 就像是一個網頁的軀殼，決定了基本結構；CSS 是衣服，讓網頁外表美觀；JavaScript 則像是網頁的靈魂，讓它能根據使用者的行為作出反應。

熟悉 JavaScript 的人應該也知道，雖說使用者所看到的網頁內容是瀏覽器透過解析 HTML 所呈現的，但其實內容並不一定要一開始就寫在 HTML 裡，而是可以用 JavaScript 進行「資料填入」甚至「建立 HTML Element」的動作，而 SSR 與 CSR 正是用來區分這兩種不同網頁渲染流程的名詞。

# Server-Side Rendering (SSR)

在 SSR 的世界裡，當 client 對某網頁發起有效的 request 後，該網站的 web server 會把所有指定網頁中應呈現的東西寫好放在 HTML 中（這個動作就叫做 **Rendering**），然後才回覆給 client，緊接著會回覆 CSS，最後才是回覆 JavaScript，這裡的 JavaScript 只負責事件監聽。

![[server-side-rendering.png]]

# Client-Side Rendering (CSR)

一個完全使用 CSR 技術的專案，通常會被稱作是一個「前後端完全分離」的專案，此時 server 分為前端的 server (Web Server) 與後端的 server (API Server)。

Web Server 負責提供 HTML（幾乎空白）、CSS 以及 JavaScript，這些檔案都是靜態的（內容是固定不變的），其中 JavaScript 負責頁面渲染、資料取得、事件監聽三項工作，因此通常檔案龐大，client 收到後必須使用瀏覽器的引擎執行這些 JavaScript，其中「資料取得」便是向後端 API Server 溝通的過程，API Server 只須專注於回覆資料（通常以 JSON 格式回覆），不須像 SSR 裡的 server 一樣負責 render 整個畫面。

![[client-side-rendering.png]]

# 比較一：Time to Interactive

由於在 SSR 中，JavaScript 只扮演 Event Handler/Listener 的角色（也就是負責根據使用者的行為作出反應），因此通常檔案不會很大，下載不需要花太多時間，所以使用者從「看到網頁」到「可以使用網頁」之間的時間差通常會較小（當然相對地，HTML 檔案大小就會較大，所以從 client「請求網頁」到「看到網頁」之間的時間差會相對較大，詳見 [[#比較二：Experience of Navigation|比較二]]）。

在 CSR 中，一個稍具複雜度的網站通常會有龐大的 JavaScript 來處理頁面渲染、資料取得、事件監聽三項工作，此時不僅需要花較多時間傳輸 JavaScript，從檔案「下載完成」到使用者「看到網頁並且可以使用」之間的時間差也取決於裝置的性能（但頁面重新渲染只會發生在重新整理時，不算太常發生），收發 API 的過程中也可能使得部分元件因資料不足而暫時無法使用。

# 比較二：Experience of Navigation

在 SSR 中，每跳轉到一個新的頁面都必須經歷「client 向 server 請求一整個完整的頁面」的流程，即使網頁中有諸如導覽列、頁尾等不變的元件，在請求新頁面時，server 都會渲染一個新的給 client，在網路速度較慢或 server 太忙時，這其實會帶來較差的 user experience，因為每次跳轉頁面時都會有一段等待 server 回傳頁面的時間。

在 CSR 中，頁面的跳轉會由前端（也就是 client、瀏覽器）完成，也就是說本質上其實他們是 Single-Page App，只是「頁面內容更動時會搭配著 URL 的更動」，使得整個體驗感覺起來像是頁面跳轉。

由於大多數前端框架可以做到「只重新渲染畫面中應該更動的地方」，換句話說就是可以較有效率地進行頁面跳轉，加上渲染的工作現在是交給 client 自己做而不是統一由 server 做，因此跳轉頁面時的等待時間會較短，server 比較不那麼忙。

# 比較三：SEO Result

從 [[SEO]] 一文我們可以知道搜尋引擎要先爬取網頁內容才能為每個網頁評分，在這個情境裡，爬蟲事實上就是 client，所以爬蟲同樣會依序拿到 HTML、CSS 與 JavaScript。通常而言，爬蟲並不會執行 CSS 與 JavaScript，不過這對 SSR 的網頁來說其實無傷大雅，因為評分的重點是網頁的結構以及內容，並不是外觀與互動。

然而，由於 CSR 是透過在 client 端的瀏覽器執行 JavaScript，才能渲染出完整的頁面內容以及填入所有資料，若爬蟲不執行 JavaScript，那麼它讀取到的 HTML 就幾乎是空的，此時該網頁的評分自然不會太高。

# Hybrid Rendering

在 CSR 的段落我們提到：「前後端完全分離時，Web Server 只負責提供靜態的 HTML 空殼, CSS，與龐大的 JavaScript 檔案，由 client 端全權負責呼叫 API Server 與 Rendering 的工作」，如果今天有一部分 JavaScript 可以交由 Web Server 執行，進而使得 client 端拿到的是「部分」已渲染的 HTML，剩下一部份才由 client 自己渲染、自己取得資料，這樣就叫做 Hybrid Rendering。

只是，要能夠在 Web Server 執行 JavaScript 的前提，就是 Web Server 要搭載相關環境（比如 Node.js），且因為 Web Server 多了 send API, rendering page 等工作，所以對 Web Server 設備的要求就會較高，但相對的對 client 設備等級的要求就會較低。

Hybrid Rendering 的開發框架包含 Next.js, Nuxt.js 等。

# 參考資料

- <https://hackmd.io/@spyua/HJDJUaTSO>
- <https://www.section.io/engineering-education/node-vs-nuxt/>
