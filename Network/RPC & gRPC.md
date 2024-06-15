# RPC (Remote Procedure Call)

與 RPC 相對的是 LPC (Local Procedure Call)，LPC 並不是什麼新的概念，你寫好的一包專案程式碼在 server 上運行起來後，裡面的某個 module 內的某行程式碼做了一個 call function 的動作（無論是同一個 module 內的或者是其他 module 的 function），就算是 LPC。

如果你可以理解什麼是 LPC，那 RPC 其實就是「call function 的程式與提供 function 的程式現在運行在不同 servers 上」而已，這些 servers 因為連線上互通的 network 所以可以互相傳遞資訊。

### RPC 與 API 的關係是什麼？

[API](</Web Development/API.canvas>) 是比 RPC 更廣泛的概念性名詞，API 泛指「定義 client 與 server 間要使用什麼 protocol、使用什麼格式的資料來相互溝通的一系列規則」，而 RPC 只是其中一種規則，所以與 RPC 同層級的名詞應該是 [REST API](</Web Development/REST API.md>)、[GraphQL](</Web Development/GraphQL/L1 - Introduction.canvas>) 等。

### RPC vs. REST

| |RPC|REST|
|:-:|:-:|:-:|
|耦合度|高|低👍|
|資料格式|binary, thrift, protobuf, Avro|text, XML, JSON|
|傳輸效能|高👍|低|
|IDL|thrift, protobuf|Swagger|
|Framework|gRPC, thrift|SpringMVC, JAX-RS|
|使用難度|not human readable, 難 debug|human readable, 較好 debug👍|

# gRPC

RPC 只是一個概念，而 gRPC 是一個由 Google 所實作的 RPC framework。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/grpc.jpg>)

### Protocol Buffers

gRPC 使用 protocol buffers 作為傳遞資料的格式，這個概念就有如 REST API 規定以 JSON、(url-encoded) form data… 等作為 [網頁應用程式傳遞資料的格式](</Web Development/網頁應用程式傳遞資料的格式.md>)。

統計顯示，使用 protocol buffers 編碼過的 data，其傳輸速度比使用 JSON 快了將近 5 倍，這是 protocol buffers 的其中一個優點。

下面是一個「被 encode 前」的 protocol buffer data 範例：

```protobuf
message Author {
    string name = 1;
    int32 id = 2;
}
```

### Protofile

gRPC 使用 protofile（通常以 `.proto` 結尾）定義所有可傳送的 data **schema**。

此外，protofile 也被用來定義 gRPC service，一個 gRPC 的定義檔大概會長得像下面這樣：

```protobuf
service Publisher {
 rpc SignBook (SignRequest) returns (SignReply) {}
}

message SignRequest {
    string name = 1;
}

message SignReply {
    string signature = 1;
}
```

使用同一套工具，可以針對這樣子的 protofile 產生==指定程式語言==的 client-side code 與 server-side code，因此即使 client 與 server 使用不同語言，也可以透過 gRPC 溝通。

### gRPC 架構於 HTTP/2 之上

這麼做可以享受許多 [HTTP/2](</Network/HTTP.md#HTTP 與 HTTP/2>) 的好處，包括：

- Multiplexing
- Stream Prioritization
- Binary Protocol
- Server Push

### gRPC 適用的場景

gRPC 適用於 microservices 之間的溝通。

>[!Question] gRPC 看起來好處多多，為何沒有被廣泛應用於 Web？
>因為至今所有 browser 都沒有支援。

#TODO 

# 參考資料

- <https://www.youtube.com/watch?v=gnchfOojMk4>
