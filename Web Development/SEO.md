SEO 就是一個讓網頁在搜尋結果中排名上升的過程。

一個網頁如何被搜尋引擎列在搜尋結果中？以 Google Search 為例，Google 首先會在公開網路上盡可能地爬取各個網頁，針對每個網頁進行多面向的評分，並且決定是否該給各個網頁 "**index**"，只有拿到 index 的網頁會被列在搜尋結果中。

# SEO 的種類

- [[#On-Site SEO]]
- [[#Off-Site SEO]]
- [[#Technical SEO]]

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Onpage-vs-Offpage-vs-Technische-SEO.webp>)

# On-Site SEO

On-site SEO 關注的是網站本身的內容，包括：

- URL path
- 關鍵字
- 內文
- 善用 `h1` ~ `h4` 標籤區隔段落
- `title` 標籤要簡潔且明確
- 圖片

### URL path

1. 每一階層的 path 盡量都包含該階層的關鍵字
2. 盡量不要使用 id, hash，或其他不具語意的文字
3. 盡量使用英文單字或短句
4. 使用 `-` 來間隔一層 path 內的多個單字

### 關鍵字

關鍵字指的是 user 可能會在搜尋引擎輸入的關鍵字，建議如下：

1. 首先思考：「如果我是 user，我希望當我搜尋哪些關鍵字的時候讓這個網頁出現在前面？」
2. 文章中應合理地出現關鍵字，不要為了提升排名而故意頻繁地提到關鍵字 (keyword stuffing)，或者甚至使用 CSS 將那些故意重複的關鍵字隱藏，這並不會提升排名
3. 關鍵字出現在 `h1` ~ `h4` 標籤以及 `title` 標籤中，會比出現在段落內的效果更顯著

### `title` 標籤要簡潔且明確

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/GoogleSearchResult.png>)

- `title` 不僅用於顯示在 browser 的 tab 上，同時也是顯示在搜尋結果中的文字
- 不要超過 70 字，多的字不會顯示在搜尋結果中
- 盡量不要跟別人一樣
- 盡量包含關鍵字
- 較詳細的內容可以寫在下面三種  `meta` tag：

    - `<meta name="description" content="...">`

        盡量不要超過 120 字，多的字不會顯示在搜尋結果中。
    
    - `<meta name="keywords" content="A, B, ...">`

    - `<meta name="author" content="...">`

### 內文

1. 可以先搜尋看看你預期這篇文章的應該被搜尋到的關鍵字，看看目前排前幾名的搜尋結果的內容
2. 當內文包含「某個問題的解答」時，更容易使排名上升
3. 放在第一段的內容最重要，最好能夠描述整篇文章的概要
4. 善用 `h1` ~ `h4` 描繪整篇文章的結構

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Help-Readers-by-Using-Visual-Hierarchy.webp>)

    不只對爬蟲來說，放在 `h1` ~ `h4` 代表其重要性較高，`h1` ~ `h4` 如果外觀較一般內文顯眼，也較容易抓住讀者的眼睛。

5. 網頁的主結構盡量使用 **HTML 結構標籤**，不要都用 `div`

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/web_structure.webp>)

### 圖文並茂

- 除了裝飾用的圖片以外，其他 `img` 標籤最好都有 `alt` attribute，並且應利用它來告訴爬蟲這張圖片是什麼
- `alt` 盡量不要超過 125 字
- 除非有必要，否則圖片檔案大小不要太大，會使載入變慢進而影響使用者體驗

### 連結

###### 內部連結

內部連結的意思是在網頁內文中的「指向同一個網域的其他網頁的 `a` 標籤」，使用內部連結不僅可以幫助這些被提及的網頁也被搜尋引擎爬取到，也會促使 user 繼續留在目前的網站中。

###### 外部連結

內文中適當地提供「可信度高的外部網站的連結」雖然不能直接影響排名，但可以讓 user 的搜尋體驗更好。

### 網頁載入速度

網頁載入速度是其中一個 Google 對網頁的評分項目，速度越快分數越高，Google 有提供一個官方的 [網頁載入速度檢驗工具](https://pagespeed.web.dev/)，不止會對多個面向進行評分，也會針對得分較低的項目提供改善建議。

### User 停留越久越好

User 在一個網頁的停留時間是 Google 對網頁的評分項目，停留越久分數越高，如果 Google 觀察到有很多使用者進入某個網站後馬上就跳出來，就會開始懷疑這個網站是否有問題，進而給予其較低的評分。

通常如果使用者進入一個網頁後映入眼簾的不是他想要找的答案，他就會馬上離開跑去其他搜尋結果，因此，盡量避免網頁一載入就出現大篇幅的廣告，或者其他與 `title` 無關的資訊。

另一方面，如果網站有良好的導覽列設計，則可以促使使用者在網站中「到處逛逛」，進而拉長他的停留時間：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/nav.png>)

除了導覽列以外，也可以提供 breadcrumbs (麵包屑)，讓使用者清楚目前的網頁與網站首頁的相對位置：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/breadcrumbs-bestbuy-location-based.jpeg>)

# Off-Site SEO

所有不更動網站本身內容的 SEO 都叫做 Off-site SEO。

### Link Building

在其他具有公信力的網站上（比如社群平台）為自己的網站上建立反向連結。

# Technical SEO

### Sitemap

Sitemap 的格式可以是 `.xml` 或者 `.txt`，將 sitemap 交給 Google 可以確保 sitemap 內的網頁都被 Google index

- [Google 官方文件](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap)
- [Sitemap Generator](https://www.mysitemapgenerator.com/)

### Microdata

- [教學](<https://blog.user.today/html5-semantic-tag-and-microdata-seo/>)
- [Schema.org](https://schema.org/docs/full.html)
- [Structure Data 測試工具 - Google](https://developers.google.com/search/docs/appearance/structured-data)

# SEO 評量

### 工具統整

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Tools-You-Need-for-an-SEO-Audit.webp>)

- [Google Search Console](https://search.google.com/search-console)
- [Google PageSpeed Insight](https://pagespeed.web.dev/)
- [Google Schema Markup Testing Tool](https://developers.google.com/search/docs/appearance/structured-data)

# 參考資料

- <https://www.semrush.com/blog/learn-seo/>
- <https://www.semrush.com/blog/on-page-seo/>
- <https://www.semrush.com/blog/off-page-seo/>
- <https://www.semrush.com/blog/learning-technical-seo/>
- <https://www.semrush.com/blog/seo-audit/>
- <https://developers.google.com/search/docs>
- <https://www.astralweb.com.tw/the-best-seo-practices-for-front-end-coding/>
