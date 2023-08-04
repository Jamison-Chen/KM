# 在 MacOS 上安裝 pyenv

### Step0: 先確認 Mac 上有 homebrew

```bash
brew --version
```

若出現 `zsh: command not found: brew` 代表你的電腦中沒有沒有 homebrew，此時你需要先[[Homebrew#安裝|安裝 homebrew]]。

### Step1: 安裝 pyenv

```bash
brew install pyenv
```

# 使用 pyenv 安裝 Python

假設我現在要下載 Python 3.11.2：

```bash
pyenv install 3.11.2
```

# 其他常用指令

### `pyenv version`

查看全域環境目前正在使用哪個版本的 Python。

### `pyenv versions`

查看本機目前已經下載哪些版本的 Python。

Output 會長的像下面這樣：

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

<https://www.newline.co/courses/create-a-serverless-slackbot-with-aws-lambda-and-python/installing-python-3-and-pyenv-on-macos-windows-and-linux>
