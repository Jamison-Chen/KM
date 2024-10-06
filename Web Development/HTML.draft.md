# `<script>`

### `async` & `defer` Attributes

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/script-loading-legend.png>)

- 沒有 `async` 與 `defer`

    當執行到 `<script>` 這行時，就會開始下載 JavaScript，且下載完後直接執行，這段過程中 HTML parsing 會被擋住，所以寫在 `<script>` 後面的 HTML 必須等到下載 + 執行完 JavaScript 後才會繼續被 parsing。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/script-loading-script.png>)

- `async`

    與什麼 attribute 都沒有的差別在於「下載」JavaScript 的時候可以同時 parse HTML，下載完後會馬上開始執行，開始執行 JavaScript 時 HTML parsing 才會被擋住。但這也意味著每次 HTML parsing 被暫停的地方會因為下載速度不同而有差異。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/script-loading-async.png>)

- `defer`

    「下載」JavaScript 的時候可以同時 parse HTML，且下載完後不會馬上開始執行，會等到 HTML parsing 完全結束後才開始執行。

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/script-loading-defer.png>)

參考資料｜[Growing with the Web](https://www.growingwiththeweb.com/2014/02/async-vs-defer-attributes.html)

# `<link>`

#TODO 

# `<meta>`
