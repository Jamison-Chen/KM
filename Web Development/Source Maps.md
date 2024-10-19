#WebDevFrontend 

Source maps 是當使用前端框架開發完後，將 production-built code 對應到 source code 的 maps，目的是讓其他人可以透過瀏覽器的開發者工具直接看到 source code，方便開發者 debug。大多數的框架預設都會在 build 時產生 source maps。

大多數瀏覽器都有實作「根據 source maps 將 production-build code 轉換成 source code」的功能，比如 Google Chrome 就將此功能放在開發者工具的 "Sources" 分頁。

# Pros & Cons

- Pros：方便開發者 debug
- Cons
    - 讓有心者更容易逆向工程（白話文就是偷你的 source code）
    - Source maps 會佔用額外的記憶體空間

# 可以不要產生 Source Maps 嗎？

可以。以 [create-react-app](</Web Development/Frontend Frameworks/React/create-react-app.md>) 為例，雖然預設會產生 source maps，但可以在專案根目錄的 .env 檔案中加入 `GENERATE_SOURCEMAP=false` 這行設定，這樣在跑 `npm run build` 時就不會產生 source maps 了。（還有另一個方法是直接跑 `GENERATE_SOURCEMAP=false react-scripts build`）
