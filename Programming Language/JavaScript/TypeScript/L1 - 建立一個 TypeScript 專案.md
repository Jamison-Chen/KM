>[!Info]
>本文假設你已經有一個使用 npm 管理 packages 的專案，若還不清楚如何使用 npm 管理專案的 packages，請見 [[npm]]。

### Step1: 安裝 TypeScript

```bash
npm install typescript -D
```

### Step2: 修改 npm Script

```json
// package.json
...
    "scripts": {
        "init-ts": "tsc --init",
        "dev": "tsc -w"
    },
...
```

- `tsc --init` 用來初始化 TypeScript 設定檔，有這個設定檔 package 才知道要以什麼規則將 TypeScript 翻譯成 JavaScript
- `tsc -w` 用來 watch 所有 .ts 檔的變動並將其翻譯為 .js，`w` for "watch"

>[!Note]
>之所以要特別在 package.json 中定義 scripts，而不直接在 terminal 下這些 `tsc` 開頭的指令，是因為若直接在 terminal 下指令，terminal 就會去找 global 的 typescript package 來執行指令，然而並不是所有人都有（想）在 global 環境安裝 typescript，沒有安裝的人若直接在 terminal 使用 `tsc` 開頭的指令，就會無法執行；反之，若寫在 package.json 的 script 中，則 terminal 就會優先從專案中找 typescript package，也就是 step1 安裝的 package。

### Step3: 初始化 TypeScript 設定檔

```bash
npm run init-ts
```

此時專案根目錄會多一個名為 `tsconfig.json` 的 TypeScript 設定檔。

# Routine Commands

- 每次要開始開發前：

    ```bash
    npm run dev
    ```

- 每次要結束開發前使用 `Control C` 停止 watching，或直接關掉 terminal
