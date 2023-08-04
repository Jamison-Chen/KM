npm (Node Package Manager) 是 Node.js 預設的套件管理工具，在安裝 Node.js 時會一併安裝 npm。

### 查看目前的 npm 版本

```bash
npm -v
```

# 開啟一個新的 Node 專案

建立專案的 root directory 後，`cd` 至該 directory，然後執行：

```bash
npm init
```

進行幾項 yse/no 選擇後，系統將建立一個叫做 **package.json** 的檔案，若不想花時間選擇 yes/no 也可以直接：

```bash
npm init -y
```

### 安裝所有基本的 Node packages

```bash
npm install
# or
npm i
```

輸入以上指令後，專案會會出現兩個東西：

1. 根據 package.json 建立另一個叫做 **package-lock.json** 的檔案
2. 建立一個就做 **node_modules** 的 folder，並將下載的套件放在裡面

在 Node.js 中，每個專案都有自己獨立的環境，透過 node_modules folder 來管理，這個 folder 原則上會在專案的 root directory。

# 為既有的專案建置環境

由於 node_modules 通常不會跟著專案一起被納入[[CH1 - Intro to Git|版控]]，所以拿到新專案時要將專案的環境建置起來：

```bash
# Build environment for prod
npm install  # or "npm i"

# Or, build environment for dev
npm install --save-dev  # or "npm i -D"
```

此時是根據 package.json 來重建環境。

# 其他與套件相關的指令

### 安裝新套件

```sh
# For both prod and dev environment
npm install <PACKAGE>

# For dev only
npm install <PACKAGE> --save-dev  # or "npm i <PACKAGE> -D"
```

### 更新指定套件

```sh
npm update <PACKAGE>
```

# package.json

範例：

```json
{
    "name": "hello-world",
    "version": "1.0.0",
    "description": "",
    "main": "./src/Main.js",
    "scripts": {
        "start": "node ./src/Main.ts",
        "test": "echo \"Error: no test specified\" && exit 1",
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "dependencies": {}
}
```

# npm Scripts

其實一個 npm 指令就是若干個套件指令或 shell 指令的 alias，在 package.json 中可以透過 `scripts` 設定這個專案專屬的 npm 指令。

其中有一些保留字，如 `start`、`test`，這些保留字所對應到的指令是 `npm XXX`，若自定了一個「非保留字」的 npm 指令，則執行時應下 `npm run XXX`。

比如在 package.json 中有以下設定時：

```json
...
    "scripts": {
        "start": "node ./src/Main.ts",
        "test": "echo \"Error: no test specified\" && exit 1",
    },
...
```

此時在 terminal 輸入 `npm start` 就等同於輸入 `node ./src/Main.ts`；輸入 `npm test` 則等同於輸入 `echo \"Error: no test specified\" && exit 1`，由 `npm test` 的例子可以看見，npm scripts 可以做到「打包指令」的功能。

有一些保留字因已有特殊功能，因此不能另外在 scripts 中定義，如 `install`（還有所有 `install` 的 alias）、`init`
