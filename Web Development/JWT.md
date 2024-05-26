#Authentication

>[!Info] 溫馨提醒
>閱讀本文前，你必須先了解什麼是 [Token-Based Authentication](</Web Development/Cookie-Based Authentication vs. Token-Based Authentication.md#Token-Based Authentication>)。

---

JWT 為 JSON Web Token 的縮寫，主要的功能是將 JSON 格式的資料==加密==為一個不定長度的字串，增加資料傳輸時的安全性。

# JWT 的種類

依照加密方式，可以將 JWT 分為兩大類：

1. 使用單一金鑰加密的 JWT，通常被應用在==身份驗證==。
2. 使用公私鑰加密的 JWT，通常被應用在==資料交換==。

# JWT 的結構

JWT 分為三個部分：

1. Header
2. Payload
3. Signature

三個部分以 `.` 連接，因此一個 JWT 看起來會像：`xxxxxxx.yyyyyyy.zzzzzzz`

### Header

#TODO

### Payload

#TODO

### Signature

#TODO

# 參考資料

- <https://jwt.io/introduction>
