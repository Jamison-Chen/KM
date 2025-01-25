#WebDevFrontend #WebDevBackend

# SSE vs. WebSocket

#TODO 

# Server 傳送 SSE

```plaintext
Content-Type: text/event-stream
```

# Client 接收 SSE

### 方法一：使用傳統的 `fetch` API

==不推薦使用這個方法==。

```TypeScript
function sendRequest(): Promise<void> {
    let header = new Headers();
    let body = new URLSearchParams();
    
    // Configure the header and body.
    // ...
    
    let options: RequestInit = {
        method: "post",
        headers: header,
        body: body,
        credentials: "include",
    };
    await fetch(`endpoint`, options).then(this.handleResponse);
}

function handleResponse = (res: Response) => {
    let reader = (res.body as ReadableStream<Uint8Array>).getReader();
    return new ReadableStream(
        new MyUnderlyingSource(reader, this.onmessage)
    );
};

function onmessage = (message: any): void => {
    // Do whatever you want to received messages.
    // ...
};

class MyUnderlyingSource implements UnderlyingSource {
    private reader: ReadableStreamDefaultReader<Uint8Array>;
    private onmessage: Function;
    public constructor(
        reader: ReadableStreamDefaultReader<Uint8Array>,
        onmessage: Function
    ) {
        this.reader = reader;
        this.onmessage = onmessage;
    }
    
    public start(controller: ReadableStreamDefaultController) {
        return this.pump(controller);
    }
    
    private pump(controller: ReadableStreamDefaultController): any {
        return this.reader.read().then(({ done, value }) => {
            if (done) {
                controller.close();
                return;
            }
            
            controller.enqueue(value);
            
            try {
                this.onmessage(value);
            } catch {
                // ...
            }
            
            return this.pump(controller);
        });
    }
}
```

### 方法二：使用 `EventSource` API

==這個方法比較推薦==。

```TypeScript
function sendRequest(): Promise<void> {
    const eventSource = new EventSource(`endpoint`);
    eventSource.onmessage = (event: MessageEvent) => {
        let message = event.data;
        
        // Do whatever you want to received messages.
        // ...
    };
}
```

# Event Stream Format

一連串 event stream 中的每個 event 間必須用空行來隔開，沒有用空行隔開的多行會被視為同一個 event，一個 event 的每一行的格式必須為 `<FIELD_NAME>: <VALUE>`，可用的 fields 如下：

### Fields

- `id` (Optional)
- `event` (Optional)
    - Event 的類型，client side 可以使用 `addEventListener` 來針對不同類型的 event 做不同的動作；如果一個 event 沒有 `event` field，那就是由 `onmessage` handler 處理。
- `data` (Required)
    - 連續多行的 data 會被 client side 自動串接起來。
    - `data` 的值除了可以是 plain text 外也可以是一個 JSON 格式的資料。
- `retry` (Optional)
    - 斷線多久 (ms) 後，client 要嘗試 reconnect。這個 field 的值必須是一個整數。

>[!Note]
>Field 只有上面這些，除了上述 field 外，其它自定義的 fields 都會直接被忽略。

**Example**

```plaintext
event: message
data: Hi

event: message
data: Hello,
data: world!
```

# 參考資料

- <https://web.dev/articles/eventsource-basics>
- <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events>
