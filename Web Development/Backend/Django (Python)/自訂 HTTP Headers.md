若前後端溝通時想要有標準 HTTP headers 以外的自訂 headers，則 Django 後端必須額外做設定，後端才不會因為看見陌生的 header 而將前端的 `GET` 或 `POST` method 歸類為 `OPTION` method。

以下假設你的 Django Framework 有安裝 `django-cors-headers` 這個套件。

比如現在前後端想制定一個名為 "identity" 的 header，後端設定的方法很簡單，只要在 `settings.py` 中做以下設定即可：

```Python
# settings.py

CORS_ALLOW_HEADERS = list(default_headers) + ["identity"]
```

需注意的是，在 Django 若要讀取 identity header 的值，則實際上要讀取的是 HTTP_IDENTITY:

```Python
request.META.get("HTTP_IDENTITY")
```
