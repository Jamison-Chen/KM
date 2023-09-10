在瀏覽器中，Broadcast Channel API 使得具有相同 origin 的各個 "browsing context" (瀏覽器所呈現的 document) 間可以互相傳遞訊息。

某些第三方應用程式的 OAuth 會另開新視窗發送 API 取得 auth token，再使用 broadcast channel API 將 token 傳遞回使用 OAuth 的原視窗，原視窗的網頁再將 token 存進 Cookie storage。

### Constructor

Broadcast channel 必須有名字，只有具有相同名字的 channel 才可以。

```JavaScript
const channel = new BroadcastChannel("hello-world")
```

### 發送 Message

Message 可以是 string 或 object。

```JavaScript
channel.postMessage({
    name: "John",
    age: 20
})
```

### 接收 Message

只有與發送 message 的 channel 具有相同名字的 channel 才可以接收到 message。

```JavaScript
channel.addEventListener("message", <callback>)
```

# 參考資料

- <https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel>
