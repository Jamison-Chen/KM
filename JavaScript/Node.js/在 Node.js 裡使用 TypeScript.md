# 建立新的 Node.js 專案

### Step 1: `npm init`

```bash
npm init -y
```

### Step 2: 安裝必要套件

```bash
npm install ts-node typescript '@types/node'
```

- `ts-node`

    Instead of using the command `tsc -w` provided by `typescript` itself, which will compile TypeScript code to JavaSctipt and write it to disk, `ts-node` is used to compile TypeScript code **on the fly** and run it through Node using the command `ts-node <your-file-name>.ts`. ([Official Documentation](https://www.npmjs.com/package/ts-node))

- `@types/node`

    This package contains type definitions for Node.js.

### Step 3: 初始化 TypeScript 設定檔

```bash
tsc --init
```

# 執行

```sh
ts-node <relative/path/to/the/file_to_execute>.ts
```

---

>[!Note] 沒有 Hot-Reload 機制
>若程式碼執行後會一直佔用著 process，那麼執行的過程中對 `.ts` 檔修改並不會反映在執行中的 process 上，必須中斷 process 並重新執行程式碼才行。若希望可以 hot-reload，則必須安裝 package `nodemon`：
>
>```sh
>npm i -D nodemon
>```
>
>執行：
>
>```sh
>npx nodmon <relative/path/to/the/file_to_execute>.ts
>```
