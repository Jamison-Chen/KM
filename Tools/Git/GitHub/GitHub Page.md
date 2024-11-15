GitHub 有一個可以提供靜態檔案的 server 在 `github.io` 這個 domain，每一個 GitHub user 或 organization 都會獲得一個以自己 username/organization name 為名的 sub-domain，可以拿來當作各個 repo 的 demo 網頁，這就是所謂的 GitHub page。

各個 repo 的 demo 網頁使用 root path 區分 ，比如我的 GitHub 帳號叫 `abc123`，帳號底下有個 repo 叫 `hello-world`，則這個 repo 的 demo 網頁的 URL 就會是 `https://abc123.github.io/hello-world`。

與常見的 web server 預設行為一樣：==GitHub page 的 URL path 對應到的是其所屬的 repo 的 directory path==，每當進到一個 GitHub page 時，無論是在 root 或其它 sub-path，GitHub 的 server 都會自動尋找並提供對應 directory 中的 `index.html`。

# 建立 GitHub Page

各個 repo 並不是一建立就有網頁，詳細的設定步驟請見[官方教學](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

# 特殊意義的 Repo Name

每一個 GitHub 帳號都可以有一個名為 `{USERNAME}.github.io` 的 repo，這個名字的 repo 的特殊之處在於：它的 demo 網頁的網址就是 `https://{USERNAME}.github.io`，沒有 path，所以它可以拿來作為整個 GitHub 帳號的 demo 網頁。

# Custom Domain

前面提到 GitHub page 的網址格式會是 `{USERNAME}.github.io/{REPO-NAME}`，但其實可以設定 custom domain。

詳細的設定步驟如下請見[官方教學](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。

# Host Single-Page App with GitHub Page

由於「GitHub page 的 URL path 對應到的是其所屬的 repo 的 directory path」這個特性，原生的 GitHub page 是不支援 single-page app (SPA) 的，須使用特別的方式繞過。這個方式簡單說就是要在 404 page 埋一段會進行 client-side redirect 的 JavaScript，具體做法可以參考下面這個網站的介紹：

<https://github.com/rafgraph/spa-github-pages/tree/gh-pages>

<iframe src="https://github.com/rafgraph/spa-github-pages/tree/gh-pages" style="aspect-ratio: 4/3" />

# gh-pages

<https://github.com/tschaub/gh-pages>

通常前端網頁開發完後都須要 build code，這個 npm 套件可以幫助你建立出一個快速 build, deploy & configure Github page 的流程：

<iframe src="https://github.com/tschaub/gh-pages" style="aspect-ratio: 4/3" />
