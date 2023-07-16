**Step 0: 確認 Node.js 版本**

```bash
node -v
```

**Step 1: 安裝套件 `n`**

`n` 的用途是拿來切換 Node.js 版本。

```bash
npm i -g n
```

**Step 2: 先設置環境變數，再將 Node.js 切換至 stable 版本**

```bash
N_PREFIX=$HOME/.local n stable
```

---

你也可以選擇使用 [[nvm]] 全域安裝多個不同 Node 版本，並進行切換。

# 參考資料

<https://guillermo.at/update-node-proper-way>

<https://chat.openai.com/chat/eb3f3649-da00-4b8c-a187-7d239619bf80>
