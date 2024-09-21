# On MacOS

### Step1: 安裝

```bash
brew update
brew install mysql
```

安裝過程中會被要求設定 `root` user 的密碼。

### Step2: 啟動 MySQL Server

```bash
brew services start mysql
```

# 進入 MySQL CLI

```sh
mysql <DB_NAME> --user=<USERNAME> --password
# or
mysql <DB_NAME> -u <USERNAME> -p
```

- 輸入這個指令後，會被要求輸入 `<USERNAME>` 的密碼
- 剛安裝 MySQL 時只會有 `root` user
