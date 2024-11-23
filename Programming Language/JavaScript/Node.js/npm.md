#package

npm (Node Package Manager) 是 Node.js 預設的套件管理工具，==在安裝 Node.js 時會一併安裝 npm==。

### 查看目前的 npm 版本

```bash
npm -v
```

# 建立一個新的 Node.js 專案

### Step0: 建立專案的根目錄

### Step1: 導入 npm

在根目錄執行：

```bash
npm init
```

做幾個 yse/no 選擇後，npm 會幫你建立一個叫 **package.json** 的檔案，這些 yes/no 選擇只會影響到 package.json 的內容，所以也可以先全部都選 yes，之後再手動改 package.json。

若想要全部都選 yes，直接跳過問問題的階段，那就改用這個指令：

```bash
npm init -y
```

### Step2: 安裝所有基本的 Node.js Dependencies

```bash
npm install
# or
npm i
```

輸入以上指令後，專案會出現兩個東西：

1. 根據 package.json 建立另一個叫 **package-lock.json** 的檔案
2. 建立一個叫 **node_modules** 的 directory，並將下載的套件放在裡面

在 Node.js 中，每個專案都有自己獨立的「環境」，這個環境指的其實就是 node_modules/。

# 為既有的專案建置開發環境

由於 node_modules/ 通常不會跟著專案一起被納入[版控](</Tools/Git/1 - Introduction.md>)，所以從遠端把一個專案 clone 下來後，第一件事就是要將專案的開發環境建置起來：

```bash
npm install
# or
npm i
```

此時 npm 會根據 package-lock.json 來重建環境 (node_modules/)，如果專案本來沒有 package-lock.json，只有 package.json，那 npm 就會先根據 package.json 建立出 package-lock.json，再根據 package-lock.json 建立環境。

# 其它常用指令

### 安裝新套件

```bash
# For both prod and dev environment
npm install {PACKAGE}

# For dev only
npm install {PACKAGE} --save-dev  # or "npm i {PACKAGE} -D"
```

### 更新指定套件到最新版本

```bash
npm install {PACKAGE}@latest
```

# package.json vs. package-lock.json

#TODO

package.json 範例：

```json
{
    "name": "hello-world",
    "version": "1.0.0",
    "description": "",
    "main": "./src/Main.js",
    "scripts": {
        "start": "node ./src/Main.ts",
        "test": "echo \"Error: no test specified\" && exit 1",
        "dev": "tsc -w"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "dependencies": {},
    "devDependencies": {}
}
```

# npm Scripts

其實一個 npm 指令就是若干個套件指令或 Shell 指令的 alias，在 package.json 中可以透過 `scripts` 設定這個專案專屬的 npm 指令。

其中有一些保留字，如 `start`、`test`，這些保留字所對應到的指令是 `npm XXX`，若自定了一個「非保留字」的 npm 指令，則執行時應下 `npm run XXX`。

比如在 package.json 中有以下設定時：

```json
...
    "scripts": {
        "start": "node ./src/Main.ts",
        "test": "echo \"Error: no test specified\" && exit 1",
        "dev": "tsc -w"
    },
...
```

此時在 terminal 輸入 `npm start` 就等同於輸入 `node ./src/Main.ts`；輸入 `npm test` 則等同於輸入 `echo \"Error: no test specified\" && exit 1`；輸入 `npm run dev` 則等同於輸入 `tsc -w`。

>[!Note]
>有一些保留字因已有特殊功能，因此不能另外在 scripts 中定義，如 `install`（還有所有 `install` 的 alias）、`init`。

### 為什麼要使用 npm Script？

使用 npm script 的其中一個好處是「簡潔」，以上方的 `npm test` 為例，它取代了冗長的 `echo \"Error: no test specified\" && exit 1`。

「簡潔」這個好處或許無法說服你額外將指令包裝成 npm script，但下面這個問題可能就會讓你心甘情願的使用 npm script 了：

以 `"dev": "tsc -w"` 這行設定為例，它告訴我們 `npm run dev` 就等於 `tsc -w`，你可能會想包裝後的指令反而變長了，但如果你試著直接在 terminal 執行 `tsc -w`，高機率會出現下面這個錯誤訊息：

```plaintext
zsh: command not found: tsc
```

這是因為 `tsc` 這個指令是 Node.js 的 `typescript` 這個套件的指令，但你沒有在 global environment 安裝這個套件（`npm install` 是把這個套件安裝在專案的根目錄）所以你的 Shell 找不到指令。而 npm script 幫我們解決了這個問題，使用 npm script 時，npm 會在執行指令前先把 node_modules/.bin/ 載入 `PATH` 這個[[Operating System/Shell/1 - Introduction#系統層級的環境變數|環境變數]]。
