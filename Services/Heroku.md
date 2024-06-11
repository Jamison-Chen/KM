Heroku 被歸類為 **PaaS (Platform as a service)**，其它類似的服務還有 [AWS Elastic Beanstalk](https://aws.amazon.com/tw/elasticbeanstalk/) 與 [Render](https://render.com/)。

# Heroku CLI

### 登入

```bash
heroku login
```

#TODO 

# 資料庫備份

### 設定定時備份 Remote Database

e.g.

```bash
heroku pg:backups:schedule DATABASE_URL --at "15:00 Asia/Taipei" --app my-app
# DATABASE_URL 就是 DATABASE_URL，不用動
```

### 手動備份

```sh
heroku pg:backups:capture -a <HEROKU_APP_NAME>
```

### 在 Heroku DB 上 Restore 備份檔

e.g.

```sh
heroku pg:backups:restore b101 DATABASE_URL --app my-app
```

### 下載備份檔至 Local

```sh
heroku pg:backups:download -a <HEROKU_APP_NAME>
```

>[!Note]
>備份檔的檔案類型不是 `.dump` 也不是 `.sql`，而是 compressed binary format，這類檔案的優點是檔案較小，原因是它並不會儲存任何 db index，而是會儲存可以重建 db index 的指令。
### 在 Local DB 上 Restore 備份檔

```sh
pg_restore --verbose --clean --no-acl --no-owner -h <DB_HOST> -U <DB_USER> -d <DB_NAME> <BACKUP_FILE_NAME>
```

>[!Info]
>執行這個指令後通常會冒出幾個 errors，但通常不會怎麼樣。

### 將 Local DB 備份並 Restore 至 Heroku

- Step1 Dump local db：請見[備份與還原#Dump](</Database/PostgreSQL/備份與還原.md#Dump>)
- Step2 Restore to Heroku

    ```sh
    heroku pg:psql -a <HEROKU_APP_NAME> < <DUMP_FILE>.dump
    
    # or

    heroku pg:psql -a <HEROKU_APP_NAME> < <DUMP_FILE>.sql
    ```

### 參考資料

- <https://devcenter.heroku.com/articles/heroku-postgres-backups>
- <https://devcenter.heroku.com/articles/heroku-postgres-import-export>
