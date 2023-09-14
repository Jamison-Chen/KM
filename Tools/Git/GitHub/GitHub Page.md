GitHub 有一個可以提供靜態檔案的 server 在 `github.io` 這個 domain，每一個 GitHub 帳號都會獲得一個以自己 username 為名的 sub-domain，可以拿來當作各個 repository 的展示網頁，此即所謂的 GitHub Page，簡稱 **gh-page**。

各個 repository 的 gh-page 以 root path 作為區分 ，比如我的 GitHub 帳號叫 jamison-chen，我有兩個 repositories 分別叫 blockchain-demo 與 machine-learning-demo，這兩個 repository 的 gh-page 的 URL 分別會是 `jamison-chen.github.io/blockchain-demo` 與 `jamison-chen.github.io/machine-learning-demo`。

# 開啟 gh-page

一個 repository 並不是一建立就有 gh-page，需要手動開啟。

開啟方式為：

1. 點擊該 repository 的 Settings tab
2. 尋找左側選單中的 Pages
3. 設定要以哪個 branch 為 source
4. 選擇要以 repository 的 root directory 或 `/docs` 這個 sub-directory 做為 gh-page 的 root directory

完成。

# 特殊意義的 Repo Name

每一個 GitHub 帳號都可以有一個名為 `<USERNAME>.github.io` 的 repository（恰好與該帳號的 gh-page 的 full domain 同名），這個名字的 repository 的特殊之處在於它的 gh-page 的 root path 為 `/`。

# 自動尋找 `index.html`

gh-page 的 URL 的 path 對應到的是其所屬的 repository 的 directory 結構，每當進到一個 gh-page 時，無論是在 root path 或其他 sub path，GitHub 的 server 都會自動尋找並提供對應 directory 中的 `index.html`。

# Single-Page App for gh-page

<iframe src="https://github.com/rafgraph/spa-github-pages/tree/gh-pages" style="aspect-ratio: 16/9" />
