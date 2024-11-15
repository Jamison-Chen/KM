# 安裝 pyenv

### On MacOS

```bash
brew install pyenv
```

>[!Note]
>執行這個指令時，若出現 `command not found: brew`，代表你的電腦中沒有 Homebrew，此時你須要先[安裝 Homebrew](</Tools/Mac/Homebrew.md#安裝>)。

### On Ubuntu

```bash
# Step1: Install dependencies
sudo apt-get update; sudo apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Step2: Clone repo from GitHub
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

# 為 pyenv 設定環境變數

### For zsh

```zsh
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

### For bash

```bash
# First, add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Then, add to ~/.profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
```

>[!Note]
>無論使用哪個 shell，在更改完 path 後都要 reload shell，新的 path 才會生效：
>
>```bash
>exec "$SHELL"
>```

# 使用 pyenv 安裝 Python

假設我現在要下載 Python 3.11.2：

```bash
pyenv install 3.11.2
```

# 更新 pyenv 的版本

### On MacOS

```bash
brew update && brew upgrade pyenv
```

# 其它常用指令

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
  3.11.2 (set by /Users/{USERNAME}/.pyenv/version)
```

打星號的代表目前全域環境所使用的版本。

### 切換全域環境使用的 Python 版本

假設要使用剛安裝好的 Python 3.11.2：

```bash
pyenv global 3.11.2
```

# 參考資料

- <https://www.newline.co/courses/create-a-serverless-slackbot-with-aws-lambda-and-python/installing-python-3-and-pyenv-on-macos-windows-and-linux>
