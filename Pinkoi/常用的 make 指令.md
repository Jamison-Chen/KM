- [文件 1](https://paper.dropbox.com/doc/Python-3---B1Nt4b8m9ercJm3gSz3eXQ4oAg-vppbyr3tvi9pgr6BSx8tk)
- [文件 2](https://sites.google.com/pinkoi.com/epd-wiki/home/dev-guide/for-backend-engineers/%E9%96%8B%E7%99%BC%E6%B5%81%E7%A8%8B/%E6%B8%AC%E8%A9%A6%E7%92%B0%E5%A2%83-make-%E9%96%8B%E7%99%BC%E6%8C%87%E4%BB%A4)

### `make local-up` / `make local-down`

#TODO 

### `make web-start` / `make web-stop`

開啟／停止 Python3 web gunicorn。

### `make web-logs`

顯示 Python3 gunicorn 的 log，必需在 gunicorn 啟動狀態下才有用。

### `make web-debug`

等於 `make web-start` + `make web-logs`。會讓 gunicorn 在前景 (foreground) 執行，並且有可操作的 tty 可以用鍵盤輸入進行互動 (e.g. `Control` + `C` 中斷/pdb)。

### `make web-status`

顯示目前 Python3 gunicorn 的啟動狀態。

### `make tunnel` / `make stop-tunnel`

啟動／停止 local 開發用的 ssh tunnel。

### `make shell`

開啟一個 bash shell，裡面有設定好的 Python3 環境，通常用於執行 script。

### `make ipython`

開啟設定好 Python3 環境的 ipython 介面，會比 `make shell` + `python` 好用。

### `make poetry-shell`

開啟可以使用 poetry 指令的 Python3 的 shell，請不要在這個 shell 下進行 poetry 之外的操作。

### `make node-shell`

開啟一個 bash shell，裡面有設定好的 Node.js 環境。

# 與 Celery 相關的指令

### `make celery-start` / `make celery-stop`

開啟／停止 Python3 Celery gunicorn，開啟時會順便停止 Python2 的 Celery。

### `make celery-reload`

如果 Celery 已開啟，則進行 reload；如果 Celery 沒開就會報錯。

### `make celery-logs`

顯示 Python3 Celery 的 log，必需在 Celery 啟動狀態下才有用。

### `make celery-debug`

等於 `make celery-start` + `make celery-logs`。會讓 Celery 在前景 (foreground) 執行，並且有可操作的 tty 可以用鍵盤輸入進行互動 (e.g. `ctrl` + `c` 中斷)。

### `make celery-status`

顯示目前 Python3 Celery 的啟動狀態。

---

### `make admin-assets`

使用 Node.js container build 出 admin tool 的前端 (`.js` + `.css`) 檔案。

### `make dev-assets`

使用 Node.js container build 出 dev 環境的前端 (`.js` + `.css`) 檔案。

### `make production-assets`

使用 Node.js container build 出 production 環境的前端 (`.js` + `.css`) 檔案。

### `make watch-website`

進入 Webpack 的 watch mode (開發 buyer site 使用)。

### `make watch-panel`

進入 Webpack 的 watch mode (開發設計師後台使用)。

### `make admin-container`

建立新的 Admin Tool Docker image。

>[!Note]
>發現有 container 沒有成功啟動且 `make local-down` + `make local-up` 也沒有用時，可以試試先下這個指令，再 `make local-down` + `make local-up`。

### `make python-container`

重新依據 `pyproject.toml` 以及 `poetry.lock` 建立新的 Python Docker image。

如果在非 dev 的 branch 下執行，會建立出該 branch 專屬的 Python Docker image。

所有的 `web-xxx` / `celery-xxx` 等 Python 相關 `make` command 都會自動優先選擇目前所在 branch 的專屬 Python Docker image。

### `make node-conatiner`

重新依據 `package.json` / `package.lock.json` 建立新的 Node.js Docker image。

如果在非 dev 的 branch 下執行，會建立出該 branch 專屬的 node Docker image。

所有的 Node.js 相關 `make` command 都會自動優先選擇目前所在 branch 的專屬 node Docker image。

### `make vscode-remote-env`

產生給 remote VS Code 使用的設定檔案 (for Python)。

### `make vscode-local-env`

產生給 vscode 進行 local 開發的設定檔案 (for Python)。

### `make py-test`

執行 pytest。

### `make extract-intl` / `make compile-intl`

c.f. [[翻譯]]

### `make pull-local-registry`

從 local registry 更新最新的 Docker images。

### `make sync-local-cert`

更新 local 開發 SSL 憑證。

### `make local-proxy`

打開 local proxy，可將 local 開發的 server 透過 proxy share 給本機以外的使用者。
