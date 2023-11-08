- [文件 1](https://paper.dropbox.com/doc/Python-3---B1Nt4b8m9ercJm3gSz3eXQ4oAg-vppbyr3tvi9pgr6BSx8tk)
- [文件 2](https://sites.google.com/pinkoi.com/epd-wiki/home/dev-guide/for-backend-engineers/%E9%96%8B%E7%99%BC%E6%B5%81%E7%A8%8B/%E6%B8%AC%E8%A9%A6%E7%92%B0%E5%A2%83-make-%E9%96%8B%E7%99%BC%E6%8C%87%E4%BB%A4)

# 與 Gunicorn 相關

### `make web-start` / `make web-stop`

開啟／停止 Gunicorn。

### `make web-logs`

顯示 Gunicorn 的 log，在 Gunicorn 啟動狀態下才有用。

### `make web-debug`

- 等於 `make web-start` + `make web-logs`
- 會讓 Gunicorn 在 terminal 前景執行，可用鍵盤快捷鍵發送訊號 (e.g. `Control` + `c`)

### `make web-status`

顯示目前 Gunicorn 的狀態。

# 與 Shell 相關

### `make shell`

開啟一個 bash shell，裡面有設定好的 Python3 環境，通常用於執行 script。

### `make poetry-shell`

- 開啟可以使用 poetry 指令的 Python3 的 shell
- ==請不要在這個 shell 下進行 poetry 之外的操作==

### `make node-shell`

開啟一個 bash shell，裡面有設定好的 Node.js 環境。

# 與 Celery 相關

### `make celery-start` / `make celery-stop`

開啟／停止 Python3 Celery gunicorn，開啟時會順便停止 Python2 的 Celery。

### `make celery-reload`

如果 Celery 已開啟，則進行 reload；如果 Celery 沒開就會報錯。

### `make celery-logs`

顯示 Python3 Celery 的 log，必需在 Celery 啟動狀態下才有用。

### `make celery-debug`

等於 `make celery-start` → `make celery-logs`。會讓 Celery 在前景 (foreground) 執行，並且有可操作的 tty 可以用鍵盤輸入進行互動 (e.g. `ctrl` + `c` 中斷)。

### `make celery-status`

顯示目前 Python3 Celery 的啟動狀態。

# 與前端相關

### `make admin-assets`

使用 Node.js container build 出 admin tool 的前端 (`.js` + `.css`) 檔案。

### `make dev-assets`

使用 Node.js container build 出 dev 環境的前端 (`.js` + `.css`) 檔案。

### `make watch-website`

進入 Webpack 的 watch mode (開發 buyer site 使用)。

### `make watch-panel`

進入 Webpack 的 watch mode (開發設計師後台使用)。

### `make watch-admin`

進入 Webpack 的 watch mode (開發 admin tool 使用)。

# 與 Docker Image 相關

### `make pull-local-registry`

從 local registry 更新最新的 Docker images。

### `make python-container`

- 重新依據 `pyproject.toml` / `poetry.lock` 建立新的 Python Docker image
- 會建立目前所在的 branch 專屬的 Python Docker image
- 所有的 `web-xxx` / `celery-xxx` 等 Python 相關 `make` 指令都會自動優先選擇目前所在 branch 的專屬 Python Docker image

### `make node-conatiner`

- 重新依據 `package.json` / `package.lock.json` 建立新的 Node.js Docker image
- 會建立目前所在的 branch 專屬的 Node.js Docker image
- 所有的 Node.js 相關 `make` 指令都會自動優先選擇目前所在 branch 的專屬 Node.js Docker image

### `make admin-container`

建立新的 admin tool 的 Docker image。

>[!Note]
>發現有 container 沒有成功啟動且 `make local-down` → `make local-up` 也沒有用時，可以試試先下這個指令，再 `make local-down` → `make local-up`。

# 與 Python 相關

### `make ipython`

開啟設定好 Python3 環境的 ipython 介面，會比 `make shell` → `python` 好用。

### `make py-test`

執行 pytest。

# 與 VS Code 相關

### `make vscode-remote-env`

產生給 remote VS Code 使用的設定檔。

### `make vscode-local-env`

產生給 local VS Code 使用的設定檔。

# 其它

### `make tunnel` / `make stop-tunnel`

- 啟動／停止 local 開發用的 ssh tunnel
- 網路中斷後重新連上時，需要重新 `make tunnel`

### `make local-up` / `make local-down`

#TODO 

### `make extract-intl` / `make compile-intl`

c.f. [[翻譯]]

### `make sync-local-cert`

- 更新 local 的 SSL 憑證
- 更新完後要重啟 container

### `make local-proxy`

打開 local proxy，可將 local 開發的 server 透過 proxy share 給本機以外的使用者。
