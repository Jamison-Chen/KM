# 方法一：使用傳統的 `fetch` API

==不推薦==

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

# 方法二：使用 `EventSource` API

==**推薦**==

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
