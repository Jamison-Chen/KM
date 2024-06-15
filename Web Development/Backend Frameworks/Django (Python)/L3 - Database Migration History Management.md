# Introduction

#TODO 

- migration files
- db table: `django_migrations`

# 修改 Database Schema

#TODO 

- `python manage.py makemigrations`
- `python manage.py migrate`

# Rollback 至指定的 Migration File

一般如果我們要透過 Django 改動資料庫 schema，流程會是 `改動 models.py` → `makemigrations` → `migrate`。但如果我們只是要將資料庫的 schema 回復到某個之前曾經使用過的版本，可以直接 rollback 回去。指令為：

```sh
python manage.py migrate <APP_NAME> <TARGET_MIGRATION_FILE>
```

- Migration file 的名稱格式會是 `<編號>_<名稱>.py`，但在 `<TARGET_MIGRATION_FILE>` 可以只寫編號，比如 `python manage.py migrate myapp 0003`
- 會一個版本接著一個版本 rollback 回去

    當你現在在編號 n 的 migration file，要 rollback 到編號 m，資料庫的 schema 會先變成版本 n - 1，再變成版本 n - 2、...、直到變成版本 m
- Rollback 完成後，被 rollback 的 migration 紀錄會從資料庫的 `django_migrations` 這張表中消失
- Rollback 完成後，如果確定被 rollback 的版本不會再用到，就可以將那些 migration files 刪除了

### Rollback All Migrations

使用上方指令的話，最多只能 rollback 到第一個 migration file，如果要連第一個 migration 都 rollback，則須在 `<TARGET_MIGRATION_FILE>` 的位置寫 `zero`：

```sh
python manage.py migrate <APP_NAME> zero
```

---

>[!Note]
>因為 rollback 是一個版本接著一個版本進行的，所以有可能會因為現存資料與某個版本的 schema 不相容而沒辦法繼續下去。

# 保留 DB Schema 但刪除 Migration 紀錄

##### Step1：確認現在的 DB Schema 與 models.py 定義的相同

```bash
python manage.py makemigrations

# No changes detected
```

##### Step2：將 DB 中指定 App 的所有 Migration 紀錄刪除

```sh
python manage.py migrate --fake <APP_NAME> zero
```

- 這個指令會將 `django_migrations` 這張表中關於 `<APP_NAME>` 的 migration 紀錄全部刪除
- 一定要記得加上 `--fake` option，才不會真的改動到 DB schema

##### Step3：手動將指定 App 的 Migration Files 刪除

migrations/\_\_init\_\_.py 要留著！

##### Step4：重新根據目前的 models.py 生成一個 Migration File

```bash
python manage.py makemigrations
```

此時生成的 migration file 就會是一步到位的 migration file。

##### Step5：在不實際更動 DB Schema 的情況下新增 Migration 紀錄

```bash
python manage.py migrate --fake-initial
```

這個指令只會在 `django_migrations` 這張表中新增一筆紀錄，因為我們從頭到尾都沒有動到 DB schema 與 models.py，所以這個步驟當然也不用實際更動 DB schema。

Done!

>[!Note] 什麼時候須要刪除 Migration 紀錄？
>在一個 multi-tenant 的服務中，我們可能會給每個租戶一個獨立的 database（在 PostgreSQL 裡叫 schema），這種情境下每多一個租戶就須要多建立一個 database。由於每次建立新的 database 時都必須從第一個 migration file 開始對 DB schema 進行 migration，此時 migration files 的數量就會影響到建立新 database 的速度。這可能是一個我們會想要刪除 migration 紀錄的理由。

# 參考資料

- <https://docs.djangoproject.com/en/5.0/topics/migrations/>
- <https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html>
