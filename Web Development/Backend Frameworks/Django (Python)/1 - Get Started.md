# Installation

```sh
pip install Django[==<VERSION>]
```

### 查詢目前版本

```bash
django-admin --version
```

# 建立新專案

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
> 想了解 project 底下各個檔案的功能，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/2 - Django 的專案架構.draft.md#Project 底下各個檔案的角色>)。

# 建立 App

> [!Note]
> 想了解 app 在一個 Django project 中扮演的角色，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/2 - Django 的專案架構.draft.md#Apps (Components)>)。

在專案根目錄執行下方指令：

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
> 想了解 app 底下各個檔案負責做什麼，請見 [Django 的專案架構](</Web Development/Backend Frameworks/Django (Python)/2 - Django 的專案架構.draft.md#App (component) 底下各個檔案的角色>)。

# 啟動 Dev Server

```sh
python manage.py runserver [<PORT>]
```

若沒有聲明 `<PORT>`，則預設使用 8000。

> [!Note]
> 這個 server 只適用於開發，不適合用在 production，production 要用 gunicorn 這類正式的 web server 才行。

# 設置 Database

Django 預設使用 [SQLite3](</Database/0 - Introduction.md#SQLite3>) 作為 database，如果要更改這個設定，步驟如下：

##### Step1: 安裝該 DB 的 Database Binding

詳見[官方文件](https://docs.djangoproject.com/en/5.0/topics/install/#get-your-database-running)。

##### Step2: 到 `<PROJECT_NAME>`/settings.py 中找到變數 `DATABASE`

`DATABASE` 預設會長得像這樣：

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

##### Step3: 更改 `ENGINE`

根據你要使用的 DB，可以將 `ENGINE` 的值改成 `'django.db.backends.postgresql'`、`'django.db.backends.mysql'`、`'django.db.backends.oracle'` 或[其它](https://docs.djangoproject.com/en/5.0/ref/databases/#third-party-notes)

##### Step4: 更改 `NAME`

若 DB 是 SQLite3，檔案名稱就是資料庫名稱；但當 DB 改成 PostgreSQL、MySQL 或 Oracle 之後，`NAME` 就是 database name。

##### Step5: 填入其它必要參數

當 DB 不是 SQLite3 時，會須要額外填入其它連線該種類 DB 所需要的必要資料，包括 `USER`、`PASSWORD`、`HOST` 與 `PORT`。

Done~

假設我要使用 PostgreSQL 當作專案使用的 DB，則 `DATABASE` 應該會長得像這樣：

```Python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("PORT"),
    }
}
```

# 新增／修改 Database Schema

##### Step1: 在 `<APP>`/models.py 中新增或修改 Class

e.g.

```Python
from django.db import models

class Company(models.Model):
    company_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    business = models.TextField(default="")
```

##### Step2: 建立 Migration Files

```sh
python manage.py makemigrations [<APP_NAME>]
```

- 根據 `<APP_ANEM>`/models.py 中的 class 建立 migration files
- 若沒有指定 `<APP_NAME>`，則代表目標為所有 apps

##### Step3: 更動 Database Schema

```bash
python manage.py migrate
```

這個指令會根據所有 `<APP>`/migrations/ 中尚未被 applied 的 migration files，更動 database schema。

>[!Note]
>關於上面兩個指令的詳細使用說明與 database migration 在 Django 中的運作方式，請看[這篇文章](</Web Development/Backend Frameworks/Django (Python)/3 - Database Migration History Management.draft.md>)。

# 其他常用指令

### 進入專案所使用的 Databaes 的 CLI

```bash
python manage.py dbshell
```

比如若專案使用的 database 是 PostgreSQL，就會進入 psql。

### 開啟 Python Interpreter

```bash
python manage.py shell
```

- 進入點為專案的 root directory
- 不直接使用指令 `python` 進入 interpreter 的原因是 `python manage.py shell` 會幫我們預先設定好環境變數 `DJANGO_SETTINGS_MODULE`（設為 main/settings.py 的 Python import path），這樣才可以 import 專案中的 modules 來使用。
