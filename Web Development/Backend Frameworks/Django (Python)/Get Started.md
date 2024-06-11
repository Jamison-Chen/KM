# Installation

### 安裝最新版本

```bash
pip install Django
```

### 已有舊版本，將其更新至最新版

```bash
pip install -U Django
```

### 確認版本

```bash
django-admin --version
```

# 使用 CLI 建立一個新專案

```sh
django-admin startproject <PROJECT_NAME>
```

使用此指令建立的 project 結構如下：

```plaintext
PROJECT_NAME
├── PROJECT_NAME
│   ├── __init__.py
│   ├── settings.py
│   ├── asgi.py
│   └── wsgi.py
└── manage.py
```

> [!Note]
> 關於 Project 底下各個檔案負責做什麼，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/Django 的專案架構.md#Project 底下各個檔案的角色>)。

# 使用 CLI 建立一個 App

> [!Note]
> 關於 app 在一個 Django project 中扮演的角色，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/Django 的專案架構.md#Project 底下各個檔案的角色>)。

在「專案根目錄」執行下方指令：

```sh
python manage.py startapp <APP_NAME>
```

專案結構會變成下面這樣：

```plaintext
PROJECT_NAME
├── PROJECT_NAME
│   ├── APP_NAME
│   |   ├── __init__.py
│   |   ├── admin.py
│   |   ├── apps.py
│   |   ├── models.py
│   |   ├── tests.py
│   |   ├── views.py
│   |   └── migrations.py
│   |       └── __init__.py
│   ├── __init__.py
│   ├── settings.py
│   ├── asgi.py
│   └── wsgi.py
└── manage.py
```

> [!Note]
> 關於 app 底下各個檔案負責做什麼，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/Django 的專案架構.md#App (component) 底下各個檔案的角色>)。

# 啟動 Dev Server

```sh
python manage.py runserver [<PORT>]
```

若沒有聲明 `<PORT>`，則預設使用 8000。

> [!Note]
> 這個 server 只適用於開發，不適合用在 production，production 還是要用 gunicorn 這類的 web server 才行。

# 新增／修改 Database Schema

- Step1: 在各 apps 底下的 models.py 中建立資料模型
- Step2: 根據所有 `APP`/models.py 中的資料模型建立 migration files

    ```bash
    python manage.py makemigrations
    ```

- Step3: 根據所有 `APP`/migrations/ 中的 migration files 更動 db schema

    ```bash
    python manage.py migrate
    ```

>[!Note]
>關於上面兩個指令的詳細使用說明與 database migration 在 Django 中的運作方式，請看[這篇文章](</Web Development/Backend Frameworks/Django (Python)/Database Migration in Django.md>)。

# 其他常用指令

- 進入專案所使用的 db 的 CLI

    ```bash
    python manage.py dbshell
    ```

    比如若專案使用的 db 是 PostgreSQL，就會進入 psql。

- 開啟 Python interpreter

    ```bash
    python manage.py shell
    ```

    進入點為專案的 root directory。

    不直接使用指令 `python` 進入 interpreter 的原因是 `python manage.py shell` 會幫我們預先設定好環境變數 `DJANGO_SETTINGS_MODULE`（設為 main/settings.py 的 Python import path），這樣才可以 import 專案中的 modules 來使用。
