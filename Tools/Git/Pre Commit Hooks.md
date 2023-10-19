### [pre-commit 官方網站](https://pre-commit.com/)

### 安裝 pre-commit

```bash
pip install pre-commit
```

### 產生設定檔

pre-commit 使用 .pre-commit-config.yaml 作為設定檔，可以使用以下指令生成範例設定檔：

```bash
pre-commit sample-config > .pre-commit-config.yaml
```

### 安裝 Hooks 至 .git File

根據 .pre-commit-config.yaml 的內容建立 hooks 至 .git/hooks 中。

```bash
pre-commit install --install-hooks
```

# 參考資料

- <https://www.mropengate.com/2019/08/pre-commit-git-hooks_4.html>
- <https://myapollo.com.tw/blog/pre-commit-the-best-friend-before-commit/>