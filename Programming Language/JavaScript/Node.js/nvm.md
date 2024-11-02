#package

nvm 是 Node Version Manager 的縮寫，讓我們可以透過 CLI 在同一台電腦的全域環境中切換不同版本的 Node.js。

# 在 MacOS 上安裝 nvm

### Step1: 打開 terminal 使用 `curl` 安裝

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

### Step2: 重啟 terminal

透過以下指令檢查是否成功安裝 nvm：

```bash
command -v nvm
```

# 常用指令

### 查看 nvm 的版本

```bash
nvm --version
```

### 安裝 Node.js

- 安裝最新版本的 Node.js

    ```bash
    nvm install node
    ```

- 安裝指定版本的 Node.js

    範例：

    ```bash
    nvm install v18.16.1
    ```

### 切換全域環境使用的 Node.js 版本（須先安裝）

```bash
nvm use {VERSION}
```

### 查看有哪些版本可以下載

```bash
nvm ls-remote
```

通常會選擇安裝 long-term support (LTS) 的版本：

```bash
nvm ls-remote --lts
```

### 查看已經下載了哪些版本

```bash
nvm ls
```

### 查看目前使用的版本

```bash
nvm current
```

### 進入 Node.js 互動介面

- 使用目前使用的 Node.js 版本

    ```bash
    nvm run node
    ```

- 使用指定的 Node.js 版本（須先安裝）

    ```bash
    nvm exec {VERSION} node
    ```

### 查看 Node.js 安裝在哪裡

```bash
nvm which {VERSION}
# or
nvm which current
```

# GitHub Repositories

- [For MacOS and Linux](<https://github.com/nvm-sh/nvm>)
- [For Windows](<https://github.com/coreybutler/nvm-windows>)

# 參考資料

- <https://titangene.github.io/article/nvm.html>
