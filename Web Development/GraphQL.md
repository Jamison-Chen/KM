### REST API 的缺點

在 [[REST API]] 中，client 只能透過 server 定義好的 **endpoints** 索取結構固定的資料，這樣會有兩個風險：

- **Under Fetching**

    若 API 回傳的資料欄位過少，則須在 server side 另開 API 或調整既有的 API，或者 client 必須透過多個 API 才能拼湊成完整的資料。

- **Over Fetching**

    若 API 回傳的資料欄位過多，則會對傳輸速度與處理速度造成不必要的負面影響。

透過 GraphQL 索取資料時，只有一個 endpoint，client 可以透過 **query** 自由決定 server 要回傳哪些資料的哪些欄位。

- GraphQL 與 REST API 一樣使用 [[HTTP]] 作為 [[The OSI Model#Application Layer (Layer 7)|application layer]]
- GraphQL 不是 framework 也不是 library，而是一個 application layer 之上的 protocol，可以用不同的程式語言實作
- Response 為 JSON 格式
- GraphQL 只有一個 endpoint

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/graphql.png>)

#TODO

# 參考資料

- <https://www.youtube.com/watch?v=5199E50O7SI>
- <https://www.apollographql.com/blog/backend/how-do-i-graphql-2fcabfc94a01/>
