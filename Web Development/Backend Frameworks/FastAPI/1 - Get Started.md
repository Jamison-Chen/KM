>[!Info] 官方文件
><https://fastapi.tiangolo.com/>

- FastAPI 建構在 [Starlette](https://www.starlette.io/) 與 [Pydantic](https://docs.pydantic.dev/latest/) 上：
    - Starlette: 一個 ASGI framework
    - Pydantic: 一個用來做資料驗證的 library
- FastAPI 支援 WSGI 與 ASGI
    - 若要執行 WSGI framework，就需要一個 [[Backend Web Architecture#WSGI/ASGI Server|WSGI server]]，比如 Gunicorn
    - 若要執行 ASGI framework，就需要一個 ASGI server，比如 Uvicorn 或 Daphne

# Installation

```Python
pip install "fastapi[standard]"
```

# Example

- Synchronous

    ```Python
    from typing import Union
    
    from fastapi import FastAPI
    
    app = FastAPI()
    
    
    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    
    
    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}
    ```

- Asynchronous

    ```Python
    from typing import Union

    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    async def read_root():
        return {"Hello": "World"}


    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}
    ```

# Run the Server

```bash
# dev server
fastapi dev {FILE_NAME}.py

# production server
fastapi run
```

- `fastapi def xxx.py` 預設支援 hot-reload

# 自動生成的 API 文件

- FastAPI 會生成兩種版本的 API 文件（主要差在介面），他們的 URL path 分別是：
    - `/docs`
    - `/redoc`
