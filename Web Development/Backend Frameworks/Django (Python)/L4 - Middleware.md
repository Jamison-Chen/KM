### [官方文件](https://docs.djangoproject.com/en/5.0/topics/http/middleware/)

# 重點摘要

- 所有 request 會先經過所有 middleware 後，才進入 view function；view function returns response 後，會再經過一次所有 middleware，才真正回傳給 client
    - 可以把 middleware 想像成一種 ==applied 在所有 view functions 上的 decorator==
- 「要經過哪些 middleware」這件事定義在 settings.py 中的 `MIDDLEWARE` 變數

    ```Python
    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "csp.middleware.CSPMiddleware",
        "main.account.middleware.check_login_status_middleware", # Custom middleware
    ]
    ```

- Middleware 的順序可能會影響結果，middleware 被經過的順序為「由上而下」

#TODO 
