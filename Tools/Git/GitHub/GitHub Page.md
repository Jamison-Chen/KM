GitHub 有一個可以提供靜態檔案的 server 在 `github.io` 這個 domain，每一個 GitHub 帳號都會獲得一個以自己 username 為名的 sub-domain，可以拿來當作各個 repo 的展示網頁，此即所謂的 GitHub page。

各個 repo 的展示網頁使用 root path 區分 ，比如我的 GitHub 帳號叫 `jamison-chen`，帳號底下有兩個 repo 分別叫 `blockchain-demo` 與 `machine-learning-demo`，則這兩個 repo 的展示網頁的 URL 會分別是 `jamison-chen.github.io/blockchain-demo` 與 `jamison-chen.github.io/machine-learning-demo`。

# 開啟 GitHub Page

GitHub 上的 repo 並不是一建立就有展示網頁，須要手動開啟。

開啟的步驟如下：

1. 點擊該 repo 的 **Settings** tab
2. 尋找左側選單中的 **Pages**
3. 設定要以哪個 branch 為 source
4. 選擇要以哪個 path 做為 repo 網頁的 root directory，有 `/` 與 `/docs` 兩個選項

完成。

# 特殊意義的 Repo Name

每一個 GitHub 帳號都可以有一個名為 `<USERNAME>.github.io` 的 repo，這個名字的 repo 的特殊之處在於：它的展示網頁的網址就是 `https://<USERNAME>.github.io`，沒有 path，所以它可以拿來作為整個 GitHub 帳號的展示網頁。

# 自動尋找 `index.html`

==GitHub page 的 URL 的 path 對應到的是其所屬的 repo 的 directory 結構==，每當進到一個 GitHub page 時，無論是在 root 或其他 sub-path，GitHub 的 server 都會自動尋找並提供對應 directory 中的 `index.html`。

# Host Single-Page App with GitHub Page

由於「GitHub page 的 URL 的 path 對應到的是其所屬的 repo 的 directory 結構」這個特性，GitHub 本來是不支援 single-page app 的，須使用特別的方式繞過。這個方式簡單說就是要在 404 page 埋一段會進行 redirect 的 JavaScript，具體做法可以參考下面這個網站：

https://github.com/rafgraph/spa-github-pages/tree/gh-pages

<iframe src="https://github.com/rafgraph/spa-github-pages/tree/gh-pages" style="aspect-ratio: 4/3" />

# gh-pages

https://github.com/tschaub/gh-pages

<iframe src="https://github.com/tschaub/gh-pages" style="aspect-ratio: 4/3" />
