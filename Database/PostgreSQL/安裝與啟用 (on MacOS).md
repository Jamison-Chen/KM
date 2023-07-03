### 使用 CLI 安裝

**Step0: 先確認 Mac 上有 homebrew**

```bash
brew --version
```

若出現 `zsh: command not found: brew` 代表你的電腦中沒有沒有 homebrew，此時你需要先[[Homebrew#^afeaf9|安裝 homebrew]]。

**Step1: 安裝 PostgreSQL**

```bash
brew install PostgreSQL@15.2
```

---

### 在背景執行 PostgreSQL Server

```bash
brew service postgresql start
```

---

### [[psql (PostgreSQL CLI)#進入 psql|進入 PostgreSQL CLI]]

---

### 關閉背景執行的 PostgreSQL Server

^0a8583

```bash
brew service postgresql stop
```

# 參考資料

- [這個網站](https://adamtheautomator.com/install-postgresql-on-mac/)提供使用 installer 安裝以及使用 CLI 安裝的教學
