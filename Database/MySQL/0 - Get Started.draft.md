# Installation

### On MacOS

- Step1: 安裝

    ```bash
    brew update
    brew install mysql
    ```

- Step2: 啟動 MySQL Server

    ```bash
    brew services start mysql
    ```

    - MySQL 使用 port 3306

# MySQL CLI

### 進入 MySQL CLI

```bash
mysql {DB_NAME}
# or
mysql --user={USERNAME} --password {DB_NAME}
# or
mysql {DB_NAME} -u {USERNAME} -p
```

- 若要使用的 user 不需要密碼即可登入，則不須加上 `--password/-p`
- 輸入有 `--password/-p` 的指令後，會被要求輸入 `{USERNAME}` 的密碼
- 剛安裝 MySQL 時，只會有一個名為 `root` 的 user、一個名為 `mysql` 的 database

### 離開 MySQL CLI

```bash
\q
# or
quit
# or
exit
```
