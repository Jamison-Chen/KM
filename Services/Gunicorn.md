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

- `<WSGI_APP>` 的結構為 `<MODULE_NAME>:<VARIABLE_NAME>`
    - `<MODULE_NAME>` 是 WSGI module，用 full dotted path 表示，比如上例中的 `myproject.wsgi`
    - `<VARIABLE_NAME>` 則是 WSGI module 中指向 WSGI app 的變數，比如上例中的 `app`
    - 如果 `<VARIABLE_NAME>` 是 `application`，可以不用寫 `:application`，因為 Gunicorn 預設會去找名為 `application` 的變數

### 常用的 Options

- `-b <BIND>` or `--bind=<BIND>`

    指定 server 要使用的 socket，`<BIND>` 的結構為 `<HOST>:<PORT>`。

- `-w <NUM_OF_WORKERS>` or `--workers=<NUM_OF_WORKERS>`

    指定要使用幾個 worker processes。

#TODO 
