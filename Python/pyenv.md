# 安裝 pyenv

### On MacOS

```bash
brew install pyenv
```

>[!Note]
>執行這個指令時，若出現 `command not found: brew`，代表你的電腦中沒有 Homebrew，此時你須要先[[Homebrew#安裝|安裝 Homebrew]]。

# 使用 pyenv 安裝 Python

假設我現在要下載 Python 3.11.2：

```bash
pyenv install 3.11.2
```

# 其他常用指令

### 查看全域環境目前使用的 Python 版本

```bash
pyenv version
```

### 列出本機已下載的 Python 版本

```bash
pyenv versions
```

Example output:

```plaintext
* system
  3.11.2 (set by /Users/<username>/.pyenv/version)
```

打星號的代表目前全域環境所使用的版本。

### 切換全域環境使用的 Python 版本

假設要使用剛安裝好的 Python 3.11.2：

```bash
pyenv global 3.11.2
```

# 參考資料

- <https://www.newline.co/courses/create-a-serverless-slackbot-with-aws-lambda-and-python/installing-python-3-and-pyenv-on-macos-windows-and-linux>
