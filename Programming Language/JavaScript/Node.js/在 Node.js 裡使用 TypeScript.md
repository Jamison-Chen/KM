# 建立新的 Node.js 專案

### Step 1: `npm init`

```bash
npm init -y
```

### Step 2: 安裝必要套件

```bash
npm install typescript ts-node '@types/node'
```

- `typescript`

    負責依照指定規則將 TypeScript compile 成 JavaScript。

- `ts-node`

    若使用 `typescript` package 的 `tsc -w` 指令，會將所有 TypeScript 都 compile 成 JavaScript，並將這些 JavaScript 存成 .js 檔；但若使用 `ts-node` 提供的 `ts-node <your-file-name>.ts` 指令，就可以將即時翻譯出來的 JavaScript 存在 RAM 中，也就不會產生 .js 檔。（詳見[官方文件](https://www.npmjs.com/package/ts-node)）

- `@types/node`

    定義了幾乎所有 Node.js 原生 API 的型別。

### Step3: 修改 npm Script

```json
// package.json
...
    "scripts": {
        "init-ts": "tsc --init"
    },
...
```

`tsc --init` 用來初始化 TypeScript 設定檔，有這個設定檔 package 才知道要以什麼規則將 TypeScript 翻譯成 JavaScript。

>[!Note]
>之所以要特別在 package.json 中定義 npm scripts，而不直接在 terminal 下這些 `tsc` 開頭的指令，是因為若直接在 terminal 下指令，terminal 就會去找 global 的 typescript package 來執行指令，然而並不是所有人都有（想）在 global 環境安裝 typescript，沒有安裝的人若直接在 terminal 使用 `tsc` 開頭的指令，就會無法執行；反之，若寫在 package.json 的 script 中，則 terminal 就會優先從專案中找 typescript package，也就是 step1 安裝的 package。

### Step 4: 初始化 TypeScript 設定檔

```bash
npm run init-ts
```

# 執行

```sh
ts-node <relative/path/to/the/file_to_execute>.ts
```

---

### 沒有 Hot-Reload 機制

若程式碼執行後會一直佔用著 process，那麼執行的過程中對 `.ts` 檔修改並不會反映在執行中的 process 上，必須中斷 process 並重新執行程式碼才行。若希望可以 hot-reload，則必須額外安裝 **nodemon** package：

```sh
npm i -D nodemon
```

且執行的指令就不再是 `ts-node` 而是：

```sh
npx nodmon <relative/path/to/the/file_to_execute>.ts
```
