### [官方文件](https://docs.gunicorn.org/en/stable/index.html)

Gunicorn 是一款用 Python 寫的 [[Backend Web Architecture#WSGI/ASGI Server|WSGI server]]。

# 安裝

```bash
pip install gunicorn
```

# 啟動

```sh
gunicorn [<WSGI_APP>] [<OPTIONS>]
```

e.g.

```bash
gunicorn myproject.wsgi:app -b 127.0.0.1:8000
```

- `<WSGI_APP>` 的結構為 `<MODULE_NAME>[:<VARIABLE_NAME>]`
    - `<MODULE_NAME>` 是 WSGI module，用 full dotted path 表示，比如上例中的 `myproject.wsgi`
    - `<VARIABLE_NAME>` 則是 WSGI module 中指向 WSGI app 的變數，比如上例中的 `app`
    - 如果 `<VARIABLE_NAME>` 是 `application`，可以不用寫 `:application`，因為 Gunicorn 預設會去找名為 `application` 的變數

### 常用的 Options

- `-b <BIND>` or `--bind=<BIND>`

    指定 server 要使用的 socket，`<BIND>` 的結構為 `<HOST>:<PORT>`。

- `-w <NUM_OF_WORKERS>` or `--workers=<NUM_OF_WORKERS>`

    指定要使用幾個 worker processes，同常會指定 4 到 12 之間的數字。

# Restart

當新版本的程式碼部署完畢時，必須 restart worker process 才會開始運行最新的 code，如果停止跟啟動中間有時間差，這段時間的 requests 的 connections 就會斷掉，因此我們會需要 **graceful restarts** 來避免這個狀況。

### Restart Strategies

|Strategy|Description|
|:-:|:-:|
|Regular Restarts|停止舊的 worker processes → connections lost → 啟動新的 worker processes|
|Hot Restarts|啟動新的 worker processes → 將舊的 worker processes 的 connections 交給新的 worker processes → 停止舊的 worker processes|
|Phased Restarts|啟動新的 worker processes 處理接下來的 requests → 等舊的 wo|rker processes 處理完所有既有的 requests → 停止舊的 worker processes

Hot restarts 與 phased restarts 都屬於 graceful restarts。

# 有了 Gunicorn，還須要 Nginx 嗎？

以下是 ChatGPT 的回答：

Yes, you can use Gunicorn to bind to `0.0.0.0:80` to serve your application over HTTP. Binding to `0.0.0.0` means that Gunicorn will listen on all available network interfaces, allowing it to accept connections from any IP address.

Here's an example command to run Gunicorn and bind it to port 80:

```bash
gunicorn main.wsgi --workers=1 --bind=0.0.0.0:80
```

==However, running a web server on port 80 typically requires elevated privileges (root access) because ports below 1024 are privileged on many systems.== You can use `sudo` to run Gunicorn with elevated privileges, but it's generally recommended to use a reverse proxy like Nginx or Apache in front of Gunicorn for several reasons:

1. **Security:** Running Gunicorn directly with elevated privileges can pose security risks. A reverse proxy provides an additional layer of security.

2. **Flexibility:** A reverse proxy allows you to handle additional tasks, such as SSL termination, load balancing, and serving static files. This offloads some responsibilities from Gunicorn.

3. **Ease of Configuration:** Reverse proxies are often easier to configure for tasks like SSL termination and URL routing.

---

關於 Nginx 的安裝、啟用與設定方法，請見[[Nginx|本文]]。
