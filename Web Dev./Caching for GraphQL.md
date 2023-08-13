#Caching 

>[!Info] 溫馨提醒
>在閱讀本文之前，我們預期你已經對 [[Caching Mechanism]] 以及 [[GraphQL]] 有基本的了解。

# HTTP Cache for GraphQL

首先，我們要釐清一件事情，GraphQL 是否可以搭配 GET method 來要資料？

答案是「可以」，Facebook Graph API 就是一個實務上的例子，但現行的套件很多都預設使用 POST，並且要求 client 將 GraphQL 的 Query 放在 request 的 body。

本文的重點並不在討論如何將你的 GraphQL 服務改造成可以接受 GET method request 的樣子，因此這裡只列出幾個與 POST 的差別，以及注意事項：

- 最好是只讓 `query` 使用 GET，`mutation` 則維持使用 POST
- 因為使用 GET method，所以 GraphQL Query 會被放在 URL 的 query string 裡

你可能會有疑問：「既然現行的 GraphQL 套件大都預設使用 POST，那就用 POST 就好啦，為什麼會想要改成 GET？」

主要的原因是 GET 與 HEAD 以外的 HTTP method 無法使用 HTTP Cache，因此每一個 request 都必定會需要 client 執行「溝通」與「下載」兩個動作，即使相同的 request 在幾秒前才剛送過一次。

會有上述機制其實也合理，因為「新增」、「修改」、「刪除」這些動作本來就不能省略並使用之前的執行結果來充當這次的結果，然而 GraphQL 中當然也存在 `query` 這種「讀取」的動作，「讀取」是應該受惠於 Caching Mechanism 的，而將 `query` 改造成使用 GET method 是第一步。

雖說改成 GET 就可以讓 GraphQL Query 受惠於 HTTP Cache，但由於 browser 是透過 URL 來判斷是否送出 request 的，因此只要 query string 有任何不一樣，都會發生 Cache Miss。比如 `/my-endpoint?field=id,name` 與 `/my-endpoint?field=name,id` 雖然其實是在要一樣的資料，但卻會被 browser 視為兩個不一樣的 requests。

>High Customization, Low Cacheability.

#TODO

# 參考資料

<https://stellate.co/blog/caching-rest-vs-graphql>

<https://www.apollographql.com/blog/backend/caching/graphql-caching-the-elephant-in-the-room/>

<https://phil.tech/2017/a-happy-compromise-between-customization-and-cacheability/>
